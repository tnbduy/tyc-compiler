"""
Utility classes for code generation.
"""

from ..utils.nodes import Type


class FunctionType(Type):
    """Function type node for code generation."""
    
    def __init__(self, param_types, return_type):
        super().__init__()
        self.param_types = param_types
        self.return_type = return_type

    def accept(self, visitor, o=None):
        return visitor.visit_function_type(self, o)


class StructType(Type):
    """Struct type node for code generation (represents struct type names)."""
    
    def __init__(self, struct_name):
        super().__init__()
        self.struct_name = struct_name

    def accept(self, visitor, o=None):
        return visitor.visit_struct_type(self, o)


class Value:
    """Base class for symbol values."""
    pass


class Index(Value):
    """Value representing a local variable index."""
    def __init__(self, value: int):
        self.value = value


class CName(Value):
    """Value representing a class name (for static methods)."""
    def __init__(self, value: str):
        self.value = value


class Symbol:
    """Symbol entry for symbol table."""
    def __init__(self, name: str, _type: Type, value: Value):
        self.name = name
        self.type = _type
        self.value = value


class Access:
    """Access object for expression evaluation."""
    def __init__(
        self,
        frame,
        sym: list["Symbol"],
        is_left: bool = False,
        is_first: bool = False,
    ):
        self.frame = frame
        self.sym = sym
        self.is_left = is_left
        self.is_first = is_first


class SubBody:
    """SubBody object for statement processing."""
    def __init__(self, frame, sym: list["Symbol"]):
        self.frame = frame
        self.sym = sym
