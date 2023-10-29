# This file is generated by the BAML compiler.
# Do not edit this file directly.
# Instead, edit the BAML files and recompile.
#
# BAML version: 0.0.1
# Generated Date: 2023-10-29 14:09:43.844017 -07:00
# Generated by: vbv

from ..._impl.functions import BaseBAMLFunction
from ..types.classes.cls_type1 import Type1
from ..types.classes.cls_type2 import Type2
from typing import Protocol, runtime_checkable


@runtime_checkable
class IFunctionOne(Protocol):
    """
    This is the interface for a function.

    Args:
        arg: Type1

    Returns:
        Type2
    """

    async def __call__(self, arg: Type1, /) -> Type2:
        ...


class IBAMLFunctionOne(BaseBAMLFunction[Type2]):
    def __init__(self) -> None:
        super().__init__(
            "FunctionOne",
            IFunctionOne,
            [],
        )

BAMLFunctionOne = IBAMLFunctionOne()

__all__ = [ "BAMLFunctionOne" ]
