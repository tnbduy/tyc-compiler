"""
AST Node classes for TyC programming language.
This module defines all the AST node types used to represent
the abstract syntax tree for TyC programs.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .visitor import ASTVisitor


class ASTNode(ABC):
    """Base class for all AST nodes."""

    def __init__(self):
        self.line = None
        self.column = None

    @abstractmethod
    def accept(self, visitor: "ASTVisitor", o: Any = None):
        """Accept a visitor for the Visitor pattern."""
        pass

    def __str__(self):
        """Default string representation."""
        return f"{self.__class__.__name__}()"

    def __repr__(self):
        """Use same as __str__ so nodes inside list/tuple display correctly.

        Python's str(list) uses repr() on elements; without __repr__, nodes
        fall back to default object repr (<Class at 0x...>).
        """
        return self.__str__()


# ============================================================================
# Program and Top-level Declarations
# ============================================================================


class Program(ASTNode):
    """Root node representing the entire TyC program."""

    def __init__(self, decls: List["Decl"]):
        super().__init__()
        self.decls = decls

    def accept(self, visitor, o=None):
        return visitor.visit_program(self, o)

    def __str__(self):
        decls_str = ", ".join(str(d) for d in self.decls) if self.decls else ""
        return f"Program([{decls_str}])"


class Decl(ASTNode):
    """Base class for declarations (struct or function)."""

    pass


class StructDecl(Decl):
    """Struct declaration node."""

    def __init__(self, name: str, members: List["MemberDecl"]):
        super().__init__()
        self.name = name
        self.members = members

    def accept(self, visitor, o=None):
        return visitor.visit_struct_decl(self, o)

    def __str__(self):
        members_str = ", ".join(str(m) for m in self.members) if self.members else ""
        return f"StructDecl({self.name}, [{members_str}])"


class MemberDecl(ASTNode):
    """Struct member declaration node."""

    def __init__(self, member_type: "Type", name: str):
        super().__init__()
        self.member_type = member_type
        self.name = name

    def accept(self, visitor, o=None):
        return visitor.visit_member_decl(self, o)

    def __str__(self):
        return f"MemberDecl({self.member_type}, {self.name})"


class FuncDecl(Decl):
    """Function declaration node."""

    def __init__(
        self,
        return_type: Optional["Type"],
        name: str,
        params: List["Param"],
        body: "BlockStmt",
    ):
        super().__init__()
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor, o=None):
        return visitor.visit_func_decl(self, o)

    def __str__(self):
        return_type_str = str(self.return_type) if self.return_type else "auto"
        params_str = ", ".join(str(p) for p in self.params) if self.params else ""
        if isinstance(self.body, BlockStmt):
            stmts = self.body.statements
        elif isinstance(self.body, list):
            stmts = self.body
        else:
            body_str = str(self.body)
            return (
                f"FuncDecl({return_type_str}, {self.name}, [{params_str}], {body_str})"
            )
        stmts_str = ", ".join(str(s) for s in stmts) if stmts else ""
        body_str = f"[{stmts_str}]"
        return f"FuncDecl({return_type_str}, {self.name}, [{params_str}], {body_str})"


class Param(ASTNode):
    """Function parameter node."""

    def __init__(self, param_type: "Type", name: str):
        super().__init__()
        self.param_type = param_type
        self.name = name

    def accept(self, visitor, o=None):
        return visitor.visit_param(self, o)

    def __str__(self):
        return f"Param({self.param_type}, {self.name})"


# ============================================================================
# Type System
# ============================================================================


class Type(ASTNode):
    """Base class for type annotations."""

    pass


class IntType(Type):
    """Integer type node."""

    def __init__(self):
        super().__init__()

    def accept(self, visitor, o=None):
        return visitor.visit_int_type(self, o)

    def __str__(self):
        return "IntType()"


class FloatType(Type):
    """Float type node."""

    def __init__(self):
        super().__init__()

    def accept(self, visitor, o=None):
        return visitor.visit_float_type(self, o)

    def __str__(self):
        return "FloatType()"


class StringType(Type):
    """String type node."""

    def __init__(self):
        super().__init__()

    def accept(self, visitor, o=None):
        return visitor.visit_string_type(self, o)

    def __str__(self):
        return "StringType()"


class VoidType(Type):
    """Void type node."""

    def __init__(self):
        super().__init__()

    def accept(self, visitor, o=None):
        return visitor.visit_void_type(self, o)

    def __str__(self):
        return "VoidType()"


class StructType(Type):
    """Struct type node."""

    def __init__(self, struct_name: str):
        super().__init__()
        self.struct_name = struct_name

    def accept(self, visitor, o=None):
        return visitor.visit_struct_type(self, o)

    def __str__(self):
        return f"StructType({self.struct_name})"


# ============================================================================
# Statements
# ============================================================================


class Stmt(ASTNode):
    """Base class for all statement nodes."""

    pass


class BlockStmt(Stmt):
    """Block statement containing statements."""

    def __init__(self, statements: List[Stmt]):
        super().__init__()
        self.statements = statements

    def accept(self, visitor, o=None):
        return visitor.visit_block_stmt(self, o)

    def __str__(self):
        stmts_str = (
            ", ".join(str(s) for s in self.statements) if self.statements else ""
        )
        return f"BlockStmt([{stmts_str}])"


class VarDecl(Stmt):
    """Variable declaration statement.
    If var_type is None, it means 'auto' (type inference).
    """

    def __init__(
        self,
        var_type: Optional["Type"],
        name: str,
        init_value: Optional["Expr"] = None,
    ):
        super().__init__()
        self.var_type = var_type  # None means 'auto'
        self.name = name
        self.init_value = init_value

    def accept(self, visitor, o=None):
        return visitor.visit_var_decl(self, o)

    def __str__(self):
        type_str = "auto" if self.var_type is None else str(self.var_type)
        init_str = f" = {self.init_value}" if self.init_value else ""
        return f"VarDecl({type_str}, {self.name}{init_str})"


class IfStmt(Stmt):
    """If statement."""

    def __init__(
        self, condition: "Expr", then_stmt: Stmt, else_stmt: Optional[Stmt] = None
    ):
        super().__init__()
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

    def accept(self, visitor, o=None):
        return visitor.visit_if_stmt(self, o)

    def __str__(self):
        else_str = f", else {self.else_stmt}" if self.else_stmt else ""
        return f"IfStmt(if {self.condition} then {self.then_stmt}{else_str})"


class WhileStmt(Stmt):
    """While statement."""

    def __init__(self, condition: "Expr", body: Stmt):
        super().__init__()
        self.condition = condition
        self.body = body

    def accept(self, visitor, o=None):
        return visitor.visit_while_stmt(self, o)

    def __str__(self):
        return f"WhileStmt(while {self.condition} do {self.body})"


class ForStmt(Stmt):
    """For statement."""

    def __init__(
        self,
        init: Optional[Union["VarDecl", "ExprStmt"]],
        condition: Optional["Expr"],
        update: Optional["Expr"],
        body: Stmt,
    ):
        super().__init__()
        self.init = init  # VarDecl, ExprStmt, or None
        self.condition = condition
        self.update = update  # Expr or None (PrefixOp, PostfixOp, or AssignExpr)
        self.body = body

    def accept(self, visitor, o=None):
        return visitor.visit_for_stmt(self, o)

    def __str__(self):
        init_str = str(self.init) if self.init else "None"
        cond_str = str(self.condition) if self.condition else "None"
        update_str = str(self.update) if self.update else "None"
        return f"ForStmt(for {init_str}; {cond_str}; {update_str} do {self.body})"


class SwitchStmt(Stmt):
    """Switch statement."""

    def __init__(
        self,
        expr: "Expr",
        cases: List["CaseStmt"],
        default_case: Optional["DefaultStmt"] = None,
    ):
        super().__init__()
        self.expr = expr
        self.cases = cases
        self.default_case = default_case

    def accept(self, visitor, o=None):
        return visitor.visit_switch_stmt(self, o)

    def __str__(self):
        cases_str = ", ".join(str(c) for c in self.cases) if self.cases else ""
        default_str = f", default {self.default_case}" if self.default_case else ""
        return f"SwitchStmt(switch {self.expr} cases [{cases_str}]{default_str})"


class CaseStmt(ASTNode):
    """Case statement in switch."""

    def __init__(self, expr: "Expr", statements: List[Stmt]):
        super().__init__()
        self.expr = expr
        self.statements = statements

    def accept(self, visitor, o=None):
        return visitor.visit_case_stmt(self, o)

    def __str__(self):
        stmts_str = (
            ", ".join(str(s) for s in self.statements) if self.statements else ""
        )
        return f"CaseStmt(case {self.expr}: [{stmts_str}])"


class DefaultStmt(ASTNode):
    """Default statement in switch."""

    def __init__(self, statements: List[Stmt]):
        super().__init__()
        self.statements = statements

    def accept(self, visitor, o=None):
        return visitor.visit_default_stmt(self, o)

    def __str__(self):
        stmts_str = (
            ", ".join(str(s) for s in self.statements) if self.statements else ""
        )
        return f"DefaultStmt(default: [{stmts_str}])"


class BreakStmt(Stmt):
    """Break statement."""

    def __init__(self):
        super().__init__()

    def accept(self, visitor, o=None):
        return visitor.visit_break_stmt(self, o)

    def __str__(self):
        return "BreakStmt()"


class ContinueStmt(Stmt):
    """Continue statement."""

    def __init__(self):
        super().__init__()

    def accept(self, visitor, o=None):
        return visitor.visit_continue_stmt(self, o)

    def __str__(self):
        return "ContinueStmt()"


class ReturnStmt(Stmt):
    """Return statement."""

    def __init__(self, expr: Optional["Expr"] = None):
        super().__init__()
        self.expr = expr

    def accept(self, visitor, o=None):
        return visitor.visit_return_stmt(self, o)

    def __str__(self):
        expr_str = f" {self.expr}" if self.expr else ""
        return f"ReturnStmt(return{expr_str})"


class ExprStmt(Stmt):
    """Expression statement."""

    def __init__(self, expr: "Expr"):
        super().__init__()
        self.expr = expr

    def accept(self, visitor, o=None):
        return visitor.visit_expr_stmt(self, o)

    def __str__(self):
        return f"ExprStmt({self.expr})"


# ============================================================================
# Expressions
# ============================================================================


class Expr(ASTNode):
    """Base class for all expression nodes."""

    pass


class BinaryOp(Expr):
    """Binary operation expression."""

    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor, o=None):
        return visitor.visit_binary_op(self, o)

    def __str__(self):
        return f"BinaryOp({self.left}, {self.operator}, {self.right})"


class PrefixOp(Expr):
    """Prefix unary operation expression (++x, --x, +x, -x, !x)."""

    def __init__(self, operator: str, operand: Expr):
        super().__init__()
        self.operator = operator  # '++', '--', '+', '-', '!'
        self.operand = operand

    def accept(self, visitor, o=None):
        return visitor.visit_prefix_op(self, o)

    def __str__(self):
        return f"PrefixOp({self.operator}{self.operand})"


class PostfixOp(Expr):
    """Postfix unary operation expression (x++, x--)."""

    def __init__(self, operator: str, operand: Expr):
        super().__init__()
        self.operator = operator  # '++', '--'
        self.operand = operand

    def accept(self, visitor, o=None):
        return visitor.visit_postfix_op(self, o)

    def __str__(self):
        return f"PostfixOp({self.operand}{self.operator})"


class AssignExpr(Expr):
    """Assignment expression (can be used in expressions like (a = 5) + 7).
    lhs can be Identifier or MemberAccess.
    """

    def __init__(self, lhs: "Expr", rhs: "Expr"):
        super().__init__()
        self.lhs = lhs  # Identifier or MemberAccess
        self.rhs = rhs

    def accept(self, visitor, o=None):
        return visitor.visit_assign_expr(self, o)

    def __str__(self):
        return f"AssignExpr({self.lhs} = {self.rhs})"


class MemberAccess(Expr):
    """Member access expression (struct member access).
    This is written directly in AST, not using PostfixExpression.
    Can be nested: MemberAccess(MemberAccess(obj, "member1"), "member2")
    """

    def __init__(self, obj: Expr, member: str):
        super().__init__()
        self.obj = obj
        self.member = member

    def accept(self, visitor, o=None):
        return visitor.visit_member_access(self, o)

    def __str__(self):
        return f"MemberAccess({self.obj}.{self.member})"


class FuncCall(Expr):
    """Function call expression."""

    def __init__(self, name: str, args: List[Expr]):
        super().__init__()
        self.name = name
        self.args = args

    def accept(self, visitor, o=None):
        return visitor.visit_func_call(self, o)

    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.args) if self.args else ""
        return f"FuncCall({self.name}, [{args_str}])"


class Identifier(Expr):
    """Identifier expression."""

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def accept(self, visitor, o=None):
        return visitor.visit_identifier(self, o)

    def __str__(self):
        return f"Identifier({self.name})"


class StructLiteral(Expr):
    """Struct literal expression (initialization with {})."""

    def __init__(self, values: List[Expr]):
        super().__init__()
        self.values = values

    def accept(self, visitor, o=None):
        return visitor.visit_struct_literal(self, o)

    def __str__(self):
        values_str = ", ".join(str(v) for v in self.values) if self.values else ""
        return f"StructLiteral({{{values_str}}})"


# ============================================================================
# Literal Expressions
# ============================================================================


class Literal(Expr):
    """Base class for literal expressions."""

    def __init__(self, value: Any):
        super().__init__()
        self.value = value


class IntLiteral(Literal):
    """Integer literal expression."""

    def __init__(self, value: int):
        super().__init__(value)

    def accept(self, visitor, o=None):
        return visitor.visit_int_literal(self, o)

    def __str__(self):
        return f"IntLiteral({self.value})"


class FloatLiteral(Literal):
    """Float literal expression."""

    def __init__(self, value: float):
        super().__init__(value)

    def accept(self, visitor, o=None):
        return visitor.visit_float_literal(self, o)

    def __str__(self):
        return f"FloatLiteral({self.value})"


class StringLiteral(Literal):
    """String literal expression."""

    def __init__(self, value: str):
        super().__init__(value)

    def accept(self, visitor, o=None):
        return visitor.visit_string_literal(self, o)

    def __str__(self):
        return f"StringLiteral({self.value!r})"
