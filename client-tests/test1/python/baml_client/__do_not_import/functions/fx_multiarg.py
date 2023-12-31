# This file is generated by the BAML compiler.
# Do not edit this file directly.
# Instead, edit the BAML files and recompile.

# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

from ..types.classes.cls_conversation import Conversation
from ..types.classes.cls_message import Message
from ..types.classes.cls_proposedmessage import ProposedMessage
from ..types.enums.enm_messagesender import MessageSender
from baml_lib._impl.functions import BaseBAMLFunction
from typing import Protocol, runtime_checkable


IMultiArgOutput = str

@runtime_checkable
class IMultiArg(Protocol):
    """
    This is the interface for a function.

    Args:
        convo: ProposedMessage
        thing: str

    Returns:
        str
    """

    async def __call__(self, *, convo: ProposedMessage, thing: str) -> str:
        ...


class IBAMLMultiArg(BaseBAMLFunction[str]):
    def __init__(self) -> None:
        super().__init__(
            "MultiArg",
            IMultiArg,
            ["v1"],
        )

    async def __call__(self, *args, **kwargs) -> str:
        return await self.get_impl("v1").run(*args, **kwargs)

BAMLMultiArg = IBAMLMultiArg()

__all__ = [ "BAMLMultiArg" ]
