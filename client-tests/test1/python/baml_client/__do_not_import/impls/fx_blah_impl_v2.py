# This file is generated by the BAML compiler.
# Do not edit this file directly.
# Instead, edit the BAML files and recompile.

# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

from ..clients.client_resilientgpt4 import ResilientGPT4
from ..functions.fx_blah import BAMLBlah
from baml_lib._impl.deserializer import Deserializer


# Impl: v2
# Client: ResilientGPT4
# An implementation of .


__prompt_template = """\
whats your name {arg}\
"""

__input_replacers = {
    "{arg}"
}


# We ignore the type here because baml does some type magic to make this work
# for inline SpecialForms like Optional, Union, List.
__deserializer = Deserializer[str](str)  # type: ignore






@BAMLBlah.register_impl("v2")
async def v2(arg: str, /) -> str:
    response = await ResilientGPT4.run_prompt_template(template=__prompt_template, replacers=__input_replacers, params=dict(arg=arg))
    deserialized = __deserializer.from_string(response.generated)
    return deserialized