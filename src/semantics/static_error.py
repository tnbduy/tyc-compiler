"""
Static Error Classes for TyC Semantic Analysis

This module defines all the exception classes that can be raised during 
static semantic checking of TyC programs according to the language specification.
"""


class StaticError(Exception):
    """Base class for all static semantic errors in TyC"""
    pass


class Redeclared(StaticError):
    """
    Raised when an identifier is declared more than once in the same scope.
    
    Args:
        kind (str): The kind of redeclared entity
                   ('Variable', 'Function', 'Struct', 'Parameter', 'Member')
        name (str): The name of the redeclared identifier
    """
    def __init__(self, kind, name):
        self.kind = kind
        self.name = name
        super().__init__(f"Redeclared({kind}, {name})")


class UndeclaredIdentifier(StaticError):
    """
    Raised when a variable or parameter is used but not declared.
    
    Args:
        name (str): The name of the undeclared identifier
    """
    def __init__(self, name):
        self.name = name
        super().__init__(f"UndeclaredIdentifier({name})")


class UndeclaredFunction(StaticError):
    """
    Raised when a function is called but not declared.
    
    Args:
        name (str): The name of the undeclared function
    """
    def __init__(self, name):
        self.name = name
        super().__init__(f"UndeclaredFunction({name})")


class UndeclaredStruct(StaticError):
    """
    Raised when a struct type is used but not declared.
    
    Args:
        name (str): The name of the undeclared struct
    """
    def __init__(self, name):
        self.name = name
        super().__init__(f"UndeclaredStruct({name})")


class TypeCannotBeInferred(StaticError):
    """
    Raised when a variable declared with `auto` cannot have its type inferred.

    Args:
        ctx: A single AST node that identifies the failure site.
    """
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__(f"TypeCannotBeInferred({ctx})")


class TypeMismatchInStatement(StaticError):
    """
    Raised when there's a type mismatch in a statement context.
    
    Args:
        stmt: The statement node where the type mismatch occurred
    """
    def __init__(self, stmt):
        self.stmt = stmt
        super().__init__(f"TypeMismatchInStatement({stmt})")


class TypeMismatchInExpression(StaticError):
    """
    Raised when there's a type mismatch in an expression context.
    
    Args:
        expr: The expression node where the type mismatch occurred
    """
    def __init__(self, expr):
        self.expr = expr
        super().__init__(f"TypeMismatchInExpression({expr})")


class MustInLoop(StaticError):
    """
    Raised when break/continue statements appear outside of loop constructs.
    
    Args:
        stmt: The break/continue statement node
    """
    def __init__(self, stmt):
        self.stmt = stmt
        super().__init__(f"MustInLoop({stmt})")
