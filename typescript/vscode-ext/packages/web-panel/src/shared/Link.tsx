import { vscode } from '@/utils/vscode'
import { StringSpan } from '@baml/common'
import { VSCodeLink } from '@vscode/webview-ui-toolkit/react'

const Link: React.FC<{ item: StringSpan; display?: string }> = ({ item, display }) => (
  <VSCodeLink
    onClick={() => {
      vscode.postMessage({ command: 'jumpToFile', data: item })
    }}
  >
    {display ?? item.value}
  </VSCodeLink>
)

export default Link
