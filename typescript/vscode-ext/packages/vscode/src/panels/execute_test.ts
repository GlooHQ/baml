import * as vscode from 'vscode'
import net from 'net'
import * as path from 'path'
import * as fs from 'fs'
import * as os from 'os'
import { exec } from 'child_process'
import {
  ClientEventLog,
  TestRequest,
  TestResult,
  TestStatus,
  clientEventLogSchema,
  getFullTestName,
  TestState as TestStateType,
} from '@baml/common'
import { generateTestRequest } from '../plugins/language-server'
import { bamlPath, bamlTestShell } from '../util'

const outputChannel = vscode.window.createOutputChannel('baml-test-runner')

function __initServer(messageHandler: (data: Buffer) => void) {
  let server = net.createServer((socket) => {
    console.log('Python script connected')

    socket.on('data', messageHandler)

    socket.on('end', () => {
      console.log('Python script disconnected')
    })
  })

  server.listen(0, '127.0.0.1')

  return server
}

interface UpdateTestCaseEvent {
  project_id: string
  test_cycle_id: string
  test_dataset_name: string
  test_case_definition_name: string
  test_case_arg_name: string // the full test case name we need
  status: TestStatus
  error_data: null | any
}

class TestState {
  private test_results: TestStateType
  private testStateListener: ((testResults: TestStateType) => void) | undefined = undefined

  constructor() {
    this.handleMessage = this.handleMessage.bind(this)
    this.handleLog = this.handleLog.bind(this)
    this.test_results = {
      results: [],
      test_url: null,
    }
  }

  public setTestStateListener(listener: (testResults: TestStateType) => void) {
    this.testStateListener = listener
  }

  public resetTestCases(tests: TestRequest) {
    this.test_results = {
      results: tests.functions.flatMap((fn) =>
        fn.tests.flatMap((test) =>
          test.impls.map((impl) => ({
            fullTestName: getFullTestName(test.name, impl, fn.name),
            functionName: fn.name,
            testName: test.name,
            implName: impl,
            status: TestStatus.Compiling,
            output: {},
          })),
        ),
      ),
      test_url: null,
    }
    this.testStateListener?.(this.test_results)
  }

  public handleMessage(data: Buffer) {
    try {
      // Data may be inadvertently concatenated together, but we actually send a \n delimiter between messages to be able to split msgs properly.
      const delimitedData = data.toString().split('<END_MSG>\n')
      delimitedData.forEach((data) => {
        if (data) {
          this.handleMessageLine(data)
        }
      })
    } catch (e) {
      console.error(e)

      outputChannel.appendLine(JSON.stringify(e, null, 2))
    }
  }

  private handleMessageLine(data: string) {
    const payload = JSON.parse(data.toString()) as {
      name: string
      data: any
    }

    switch (payload.name) {
      case 'test_url':
        this.setTestUrl(payload.data)
        break
      case 'update_test_case':
        this.handleUpdateTestCase(payload.data)
        break
      case 'log':
        let res = clientEventLogSchema.safeParse(payload.data)
        if (!res.success) {
          // console.error(res.error)
        } else {
          this.handleLog(payload.data)
        }
        break
    }
  }

  public setExitCode(code: number | null) {
    this.test_results.exit_code = code ?? 5
    this.testStateListener?.(this.test_results)
  }

  public getTestResults() {
    return this.test_results
  }

  private setTestUrl(testUrl: { dashboard_url: string }) {
    this.test_results.test_url = testUrl.dashboard_url
    this.test_results.results.forEach((test) => {
      test.status = TestStatus.Queued
    })
    this.testStateListener?.(this.test_results)
  }

  private handleUpdateTestCase(data: UpdateTestCaseEvent) {
    const testResult = this.test_results.results.find((test) => test.fullTestName === data.test_case_arg_name)

    http: if (testResult) {
      testResult.status = data.status
      if (data.error_data) {
        testResult.output = {
          error: JSON.stringify(data.error_data),
        }
      }
      this.testStateListener?.(this.test_results)
    }
  }

  private handleLog(data: ClientEventLog) {
    const fullTestName = data.context.tags?.['test_case_arg_name']
    const testResult = this.test_results.results.find((test) => test.fullTestName === fullTestName)
    if (testResult && data.event_type === 'func_llm') {
      if (this.test_results.test_url) {
        http: testResult.url = `${this.test_results.test_url}&s_eid=${data.event_id}&eid=${data.root_event_id}`
      }
      testResult.output = {
        error: data.error?.message ?? testResult.output.error,
        parsed: data.io.output?.value ?? testResult.output.parsed,
        raw: data.metadata?.output?.raw_text ?? testResult.output.raw,
      }
      this.testStateListener?.(this.test_results)
    }
  }
}

class TestExecutor {
  private static pythonPath: string | undefined = undefined
  private server: net.Server | undefined
  private testState: TestState
  private stdoutListener: ((data: string) => void) | undefined = undefined

  constructor() {
    this.server = undefined
    this.testState = new TestState()
  }

  public getTestResults() {
    return this.testState.getTestResults()
  }

  public setTestStateListener(listener: (testResults: TestStateType) => void) {
    this.testState.setTestStateListener(listener)
  }

  public setStdoutListener(listener: (data: string) => void) {
    this.stdoutListener = listener
  }

  public start() {
    if (this.server !== undefined) {
      return
    }
    this.server = __initServer(this.testState.handleMessage)
  }

  private get port_arg() {
    if (this.server !== undefined) {
      let addr = this.server.address()
      // vscode.window.showInformationMessage(`Server address: ${JSON.stringify(addr)}`)
      if (typeof addr === 'string') {
        return `--playground-port ${addr}`
      } else if (addr) {
        return `--playground-port ${addr.port}`
      }
    }

    vscode.window.showErrorMessage('Server not initialized')
    return ''
  }

  public async getPythonPath() {
    if (TestExecutor.pythonPath === undefined) {
      // Check if we should use python3 by seeing if shell has python3
      TestExecutor.pythonPath = await new Promise((resolve, reject) => {
        let res = exec('python3 -s --version')
        res.stdout?.on('data', (data) => {
          console.log(`stdout: ${data}`)
        })
        res.on('exit', (code, signal) => {
          console.log(`exit: ${code}`)
          if (code === 0) {
            resolve('python3')
          } else {
            resolve('python')
          }
        })
      })
    }

    console.log(`Using python path: ${TestExecutor.pythonPath}`)
    return TestExecutor.pythonPath!
  }

  public async runTest({ root_path, tests }: { root_path: string; tests: TestRequest }) {
    // root_path is the path to baml_src, so go up one level to get to the root of the project
    root_path = path.join(root_path, '../')
    this.testState.resetTestCases(tests)

    // Add filters.
    const selectedTests = tests.functions.flatMap((fn) =>
      fn.tests.flatMap((test) => test.impls.map((impl) => `-i ${fn.name}:${impl}:${test.name}`)),
    )
    const test_filter = selectedTests.join(' ')

    // Run the Python script in a child process
    const command = `${bamlPath({ for_test: true })} test ${test_filter} run ${this.port_arg}`

    // Run the Python script in a child process
    // const process = spawn(pythonExecutable, [tempFilePath]);
    // Run the Python script using exec
    this.stdoutListener?.('<BAML_RESTART>')
    this.stdoutListener?.(`Command: ${command}\n`)
    const cp = exec(command, {
      cwd: root_path,
      shell: bamlTestShell(),
      env: {
        ...process.env,
        CLICOLOR_FORCE: '1',
      },
    })

    cp.stdout?.on('data', (data) => {
      outputChannel.appendLine(data)
      this.stdoutListener?.(data)
    })
    cp.stderr?.on('data', (data) => {
      outputChannel.appendLine(data)
      this.stdoutListener?.(data)
    })

    cp.on('exit', (code, signal) => {
      this.testState.setExitCode(code ?? (signal ? 3 : 5))
    })
  }

  close() {
    if (this.server) {
      this.server.close()
    }
  }
}

const testExecutor = new TestExecutor()

export default testExecutor
