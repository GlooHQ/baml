<div align="center">
  <a href="https://app.trygloo.com?utm_source=github" target="_blank" rel="noopener noreferrer">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://www.trygloo.com/gloo-ai-square-256.png">
      <img src="https://www.trygloo.com/gloo-ai-square-256.png" height="64">
    </picture>
  </a>
  <h1>BAML</h1>
  <h2>A programming language to build fully type-safe LLM-based Functions<h2>
  <a href="https://discord.gg/ENtBB6kkXH"><img src="https://img.shields.io/discord/1119368998161752075.svg?logo=discord" /></a>
  <a href="https://twitter.com/intent/follow?screen_name=tryGloo"><img src="https://img.shields.io/twitter/follow/tryGloo?style=social"></a>
  <!-- <a href="https://docs.boundaryml.com"><img src="https://img.shields.io/badge/documentation-gloo-brightgreen.svg"></a> -->
  <br /> 
  <a href="https://docs.boundaryml.com">Documentation</a>
 • <a href="https://app.trygloo.com">Dashboard</a>
   <h4>Made by Boundary (formerly Gloo)</h4>
</div>

## Introduction

In the LLM-world, all inputs and outputs are strings, and that sucks.

A lot of applications actually want to get structured data from LLMs, but devs have to do a lot of work to define types, serialize those types into prompts, and parse the string outputs. Then when you want to analyze your LLM requests in your dashboard all you see is LLM output strings when there is actual structured data in there.

The typical LLM prompt to get structured data out:

```text
Given the following input:
Input: "I want to buy a car"

Output the following information in this JSON format:
{
  "sentiment": one of "happy", "sad", "neutral"
}
```

LLM Output:

````
Based on the text, this is the likely output:
```json
{
  "sentiment": "happy"
}
```
But as an AI language model, yadda-yadda yadda...
````

If you're using this approach, you may need to add more logic to detect the JSON blocks, even if you are using Pydantic. This is only one of many problems (what if I want to rename a property?) with current approaches. A deep dive on all problems with structured prompting is coming soon!

## Enter BAML (Basically, A Made-up Language)

**BAML is a lightweight language to get fully typed responses from LLMs.**

Rather than starting out writing an AI function with a prompt, in BAML you first decide what types your AI function should have as inputs and outputs, and helps you build prompts that work for those types.

BAML is a language that compiles down to Python and Typescript clients that you can plug-and-play into your codebase -- **without any parsing boilerplate**. It comes out-of-the-box with an **integrated VSCodePlayground** and **resilience features like retries, tracing, and testing capabilities**.

It takes **< 10 minutes** to learn, works with any LLM, and runs locally on your machine.

### How it works

<img src="docs/images/v3/generating_baml_clients.png" />

#### 1. Install the baml compiler and BAML VSCode extension.

Define an AI function and its types in a .baml file.

```rust
class ProductInfo {
  price float
  name string
  width int @description("width in inches")
  height int @description("height in inches")
}

function ExtractProductInfo {
  input string // can also be more complex, like an Email type
  output ProductInfo
}

```

We support complex types like optionals, unions, nested types!

#### 2. Build a prompt for that function that works for those input/output types.

```rust
client<llm> GPT4 {
  provider baml-openai-chat // or add your own
  retry_policy DefaultRetry
  options {
    temperature 0.1
    model "gpt-4"
  }
}

impl<llm, ExtractProductInfo> version1 {
  client GPT4
  prompt #"
    Given the following input:
    ---
    {#input}
    ---
    Extract the following info in JSON:
    {#print_type(output)}
  "#
}
```

#### 3. Test your function with the BAML VSCode Playground

![](https://player.cloudinary.com/embed/?public_id=baml-playground&cloud_name=dn7wj4mr5)

#### 5. Call your functions in Python or Typescript

```python
from baml_client import baml as b

async def my_code():
  productInfo = await b.ExtractProductInfo("Hello, we are selling a Vacuum XYZ at $40...")
  if result.price > 80:
    print("That seems kinda expensive")

```

- the only import you'll ever need is baml. No need to dig through any code to figure out what other abstractions you need.

BAML is part of the **Boundary Toolchain,** which encompasses other tools like the VSCode Playground, and Boundary Studio — which enables request tracing, analytics, and labeling capabilities.

**BAML and the VSCode Playground are 100% free to use.** For Boundary Studio we offer a free tier!

[Join our discord, and see what the community is up to!](https://discord.gg/BTNBeXGuaS)

## Getting started

Follow the [installation instructions](/v3/home/installation) to get started with BAML.

## Why build a language?

Building a language and owning the compiler allows us to build an entire ecosystem vs a building a Python library or framework.

Here's some examples of powerful features only a compiler-backed toolchain can provide:

1. **VSCode Playground** -
   If your prompt takes in a complex set of variables, you can create a test and fill in the input with an actual form that matches your input type schema. No more copying around JSON files for quick one-off tests. The Playground _understands_ your AI functions
2. **Boundary Studio** -
   Rather than showing you strings on the dashboard, you get actual type information. The dashboard **knows** what the desired function signature was for your LLM call.
   As a sidenote, BAML studio also offers analytics, and commenting and labeling capabilities for each of your historical requests.

<div className="flex items-center justify-center w-full">
 <img src="docs/images/v3/boundary_studio_pipeline.png" width="400px"/>
</div>

1. **And coming soon** -
   Autogenerate a fully type-safe client from your .baml functions to query your historical data in a type-safe way to train new models. Inspired by [Prisma](https://www.prisma.io/)! :).

Feel free to submit a new request in our [Github repository](https://github.com/gloohq/baml) if you have a language or platform feature you’d like to see.

## Design Goals

Our goal is to make the easiest-to-use platform to build LLM applications. Here's our core principles:

**Type-safety first.** Type completion and compile-time linting make teams much more productive. Devs shouldn't have to write out output schemas manually in a prompt ever again. We want to be what Typescript did for Javascript but for LLMs.

**Your AI Logic should live in your codebase.** The more co-located everything is, the faster it is to iterate. This includes your tests, the playground itself, and the prompts. Tracking prompt versions should be as easy as commiting a new change.

**Reduce abstractions, increase transparency.** At the end of the day you should be able to see the whole string going into an LLM call, and the full string coming out of it. We don't do anything fancy with your prompts, other than provide helper utilities to help you build them using your type info as the base. Our Playground allows you to see what your actual prompt will look like before you even run the code.

### [Documentation](https://docs.boundaryml.com)

See more at [our docs page](https://docs.boundaryml.com)

### Resources

- [Discord](https://discord.gg/ENtBB6kkXH)

## Security

Please do not file GitHub issues or post on our public forum for security vulnerabilities, as they are public!

Boundary takes security issues very seriously. If you have any concerns about BAML or believe you have uncovered a vulnerability, please get in touch via the e-mail address contact@boundaryml.com. In the message, try to provide a description of the issue and ideally a way of reproducing it. The security team will get back to you as soon as possible.

Note that this security address should be used only for undisclosed vulnerabilities. Please report any security problems to us before disclosing it publicly.
