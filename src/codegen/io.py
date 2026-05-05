"""
I/O symbol definitions for built-in functions.
"""

from ..utils.nodes import IntType, FloatType, StringType, VoidType
from .utils import FunctionType, Symbol, CName


LIB_NAME = "io"

# Built-in functions for TyC:
# readInt() -> int
# readFloat() -> float
# readString() -> string
# printInt(int) -> void
# printFloat(float) -> void
# printString(string) -> void

IO_SYMBOL_LIST = [
    # Integer I/O
    Symbol("readInt", FunctionType([], IntType()), CName(LIB_NAME)),
    Symbol("printInt", FunctionType([IntType()], VoidType()), CName(LIB_NAME)),
    
    # Float I/O
    Symbol("readFloat", FunctionType([], FloatType()), CName(LIB_NAME)),
    Symbol("printFloat", FunctionType([FloatType()], VoidType()), CName(LIB_NAME)),
    
    # String I/O
    Symbol("readString", FunctionType([], StringType()), CName(LIB_NAME)),
    Symbol("printString", FunctionType([StringType()], VoidType()), CName(LIB_NAME)),
]
