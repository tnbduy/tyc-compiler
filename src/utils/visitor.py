"""
Visitor interface for AST traversal in TyC programming language.
This module defines the abstract visitor pattern interface for traversing
and processing AST nodes.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .nodes import *


class ASTVisitor(ABC):
    """Abstract base class for AST visitors."""

    def visit(self, node: "ASTNode", o: Any = None):
        """Visit a node using the visitor pattern."""
        return node.accept(self, o)

    # Program and declarations
    @abstractmethod
    def visit_program(self, node: "Program", o: Any = None):
        pass

    @abstractmethod
    def visit_struct_decl(self, node: "StructDecl", o: Any = None):
        pass

    @abstractmethod
    def visit_member_decl(self, node: "MemberDecl", o: Any = None):
        pass

    @abstractmethod
    def visit_func_decl(self, node: "FuncDecl", o: Any = None):
        pass

    @abstractmethod
    def visit_param(self, node: "Param", o: Any = None):
        pass

    # Type system
    @abstractmethod
    def visit_int_type(self, node: "IntType", o: Any = None):
        pass

    @abstractmethod
    def visit_float_type(self, node: "FloatType", o: Any = None):
        pass

    @abstractmethod
    def visit_string_type(self, node: "StringType", o: Any = None):
        pass

    @abstractmethod
    def visit_void_type(self, node: "VoidType", o: Any = None):
        pass

    @abstractmethod
    def visit_struct_type(self, node: "StructType", o: Any = None):
        pass

    # Statements
    @abstractmethod
    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_var_decl(self, node: "VarDecl", o: Any = None):
        pass

    @abstractmethod
    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_switch_stmt(self, node: "SwitchStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_case_stmt(self, node: "CaseStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_default_stmt(self, node: "DefaultStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        pass

    # Expressions
    @abstractmethod
    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        pass

    @abstractmethod
    def visit_prefix_op(self, node: "PrefixOp", o: Any = None):
        pass

    @abstractmethod
    def visit_postfix_op(self, node: "PostfixOp", o: Any = None):
        pass

    @abstractmethod
    def visit_assign_expr(self, node: "AssignExpr", o: Any = None):
        pass

    @abstractmethod
    def visit_member_access(self, node: "MemberAccess", o: Any = None):
        pass

    @abstractmethod
    def visit_func_call(self, node: "FuncCall", o: Any = None):
        pass

    @abstractmethod
    def visit_identifier(self, node: "Identifier", o: Any = None):
        pass

    @abstractmethod
    def visit_struct_literal(self, node: "StructLiteral", o: Any = None):
        pass

    # Literals
    @abstractmethod
    def visit_int_literal(self, node: "IntLiteral", o: Any = None):
        pass

    @abstractmethod
    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        pass

    @abstractmethod
    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        pass


class BaseVisitor(ASTVisitor):
    """Base visitor that provides default implementations for all visit methods.
    Subclasses can override only the methods they need to customize."""

    def visit_program(self, node: "Program", o: Any = None):
        for decl in node.decls:
            self.visit(decl, o)

    def visit_struct_decl(self, node: "StructDecl", o: Any = None):
        for member in node.members:
            self.visit(member, o)

    def visit_member_decl(self, node: "MemberDecl", o: Any = None):
        self.visit(node.member_type, o)

    def visit_func_decl(self, node: "FuncDecl", o: Any = None):
        if node.return_type:
            self.visit(node.return_type, o)
        for param in node.params:
            self.visit(param, o)
        self.visit(node.body, o)

    def visit_param(self, node: "Param", o: Any = None):
        self.visit(node.param_type, o)

    def visit_int_type(self, node: "IntType", o: Any = None):
        pass

    def visit_float_type(self, node: "FloatType", o: Any = None):
        pass

    def visit_string_type(self, node: "StringType", o: Any = None):
        pass

    def visit_void_type(self, node: "VoidType", o: Any = None):
        pass

    def visit_struct_type(self, node: "StructType", o: Any = None):
        pass

    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_var_decl(self, node: "VarDecl", o: Any = None):
        if node.var_type:
            self.visit(node.var_type, o)
        if node.init_value:
            self.visit(node.init_value, o)

    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        self.visit(node.condition, o)
        self.visit(node.then_stmt, o)
        if node.else_stmt:
            self.visit(node.else_stmt, o)

    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        self.visit(node.condition, o)
        self.visit(node.body, o)

    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        if node.init:
            self.visit(node.init, o)  # init is VarDecl
        if node.condition:
            self.visit(node.condition, o)
        if node.update:
            self.visit(node.update, o)  # update is Expr
        self.visit(node.body, o)

    def visit_switch_stmt(self, node: "SwitchStmt", o: Any = None):
        self.visit(node.expr, o)
        for case in node.cases:
            self.visit(case, o)
        if node.default_case:
            self.visit(node.default_case, o)

    def visit_case_stmt(self, node: "CaseStmt", o: Any = None):
        self.visit(node.expr, o)
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_default_stmt(self, node: "DefaultStmt", o: Any = None):
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        pass

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        pass

    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        if node.expr:
            self.visit(node.expr, o)

    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        self.visit(node.expr, o)

    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        self.visit(node.left, o)
        self.visit(node.right, o)

    def visit_prefix_op(self, node: "PrefixOp", o: Any = None):
        self.visit(node.operand, o)

    def visit_postfix_op(self, node: "PostfixOp", o: Any = None):
        self.visit(node.operand, o)

    def visit_assign_expr(self, node: "AssignExpr", o: Any = None):
        self.visit(node.lhs, o)
        self.visit(node.rhs, o)

    def visit_member_access(self, node: "MemberAccess", o: Any = None):
        self.visit(node.obj, o)

    def visit_func_call(self, node: "FuncCall", o: Any = None):
        for arg in node.args:
            self.visit(arg, o)

    def visit_identifier(self, node: "Identifier", o: Any = None):
        pass

    def visit_struct_literal(self, node: "StructLiteral", o: Any = None):
        for value in node.values:
            self.visit(value, o)

    def visit_int_literal(self, node: "IntLiteral", o: Any = None):
        pass

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        pass

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        pass
