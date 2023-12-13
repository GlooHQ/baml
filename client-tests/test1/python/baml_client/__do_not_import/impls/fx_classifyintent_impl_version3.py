# This file is generated by the BAML compiler.
# Do not edit this file directly.
# Instead, edit the BAML files and recompile.

# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

from ..clients.client_gpt4 import GPT4
from ..functions.fx_classifyintent import BAMLClassifyIntent
from ..types.classes.cls_intentwithreasoning import IntentWithReasoning
from ..types.enums.enm_intent import Intent
from baml_lib._impl.deserializer import Deserializer


# Impl: version3
# Client: GPT4
# An implementation of .


__prompt_template = """\
Classify the following INPUT into ONE
of the following Intents: 

Intent
---
k1: Customer wants to return a product
k2: Customer wants to cancel an order
k3: Customer needs help with a technical issue unrelated to account creation or login
k4: Specifically relates to account-login or account-creation
k5: Customer has a question

INPUT: {arg}

Response JSON:
{
  "reasoning_steps": string,
  "intent": "Intent as string"
}\
"""

__input_replacers = {
    "{arg}"
}


# We ignore the type here because baml does some type magic to make this work
# for inline SpecialForms like Optional, Union, List.
__deserializer = Deserializer[IntentWithReasoning](IntentWithReasoning)  # type: ignore


def output_adapter(output: IntentWithReasoning) -> Intent:
    # output is a special variable that contains the output of the LLM that is of type IntentOutputWithCoT. We need to return just the intent to abide by the original function signature.
    return output.intent



@BAMLClassifyIntent.register_impl("version3")
async def version3(arg: str, /) -> Intent:
    response = await GPT4.run_prompt_template(template=__prompt_template, replacers=__input_replacers, params=dict(arg=arg))
    deserialized = __deserializer.from_string(response.generated)
    return output_adapter(deserialized)
