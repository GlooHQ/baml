# This file is generated by the BAML compiler.
# Do not edit this file directly.
# Instead, edit the BAML files and recompile.
#
# BAML version: 0.1.1-canary.7
# Generated Date: __DATE__
# Generated by: __USER__

# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

from ..clients.client_azure_gpt4 import AZURE_GPT4
from ..functions.fx_classifytool import BAMLClassifyTool
from ..types.classes.cls_classifyresponse import ClassifyResponse
from ..types.classes.cls_userinfo import UserInfo
from ..types.enums.enm_tool import Tool
from baml_lib._impl.deserializer import Deserializer


# Impl: v1
# Client: AZURE_GPT4
# An implementation of .


__prompt_template = """\
Given a conversation with a user, classify the user's intent and generate a response.

Userinfo:
{arg.query}

UserContext:
{arg.context}

Tool
---
CodeInterpreter
DrawImage
GenerateText


Use this output format:
{
  "tool": "Tool as string",
  "assistant_response": string
}

JSON:\
"""

__input_replacers = {
    "{arg.query}",
    "{arg.context}"
}


# We ignore the type here because baml does some type magic to make this work
# for inline SpecialForms like Optional, Union, List.
__deserializer = Deserializer[ClassifyResponse](ClassifyResponse)  # type: ignore
__deserializer.overload("ImprovedResponse", {"ShouldImprove": "should_improve"})

@BAMLClassifyTool.register_impl("v1")
async def v1(arg: UserInfo, /) -> ClassifyResponse:
    response = await AZURE_GPT4.run_prompt_template(template=__prompt_template, replacers=__input_replacers, params=dict(arg=arg))
    return __deserializer.from_string(response.generated)