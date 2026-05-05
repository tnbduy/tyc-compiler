"""
Semantic analysis module for TyC programming language.

This module provides static semantic checking capabilities including
type inference, scope management, and error detection.
"""

from .static_error import (
    StaticError,
    Redeclared,
    UndeclaredIdentifier,
    UndeclaredFunction,
    UndeclaredStruct,
    TypeCannotBeInferred,
    TypeMismatchInStatement,
    TypeMismatchInExpression,
    MustInLoop,
)

from .static_checker import StaticChecker

__all__ = [
    "StaticError",
    "Redeclared",
    "UndeclaredIdentifier",
    "UndeclaredFunction",
    "UndeclaredStruct",
    "TypeCannotBeInferred",
    "TypeMismatchInStatement",
    "TypeMismatchInExpression",
    "MustInLoop",
    "StaticChecker",
]
