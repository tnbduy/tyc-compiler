"""
Static Semantic Checker for TyC Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the TyC procedural programming language. It performs type checking,
scope management, type inference, and detects all semantic errors as
specified in the TyC language specification.
"""

from functools import reduce
from typing import (
    Dict,
    List,
    Set,
    Optional,
    Any,
    Tuple,
    NamedTuple,
    Union,
    TYPE_CHECKING,
)
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode,
    Program,
    StructDecl,
    MemberDecl,
    FuncDecl,
    Param,
    VarDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    BlockStmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    Type,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    BinaryOp,
    PrefixOp,
    PostfixOp,
    AssignExpr,
    MemberAccess,
    FuncCall,
    Identifier,
    StructLiteral,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    ExprStmt,
    Expr,
    Stmt,
    Decl,
)

# Type aliases for better type hints
TyCType = Union[IntType, FloatType, StringType, VoidType, StructType]
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

## TODO Có thể viết thêm class/method nếu cần
class InferredError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class SymType:
    pass

class SymInt(SymType):
    pass

class SymFloat(SymType):
    pass

class SymString(SymType):
    pass

class SymAuto(SymType):
    pass

class SymVoid(SymType):
    pass

class SymFunc(SymType):
    def __init__(self, params : list[tuple[str, SymType]] = [], return_type : SymType = VoidType()):
        self.params = params
        self.return_type = return_type

class SymStruct(SymType):
    def __init__(self,members : list[tuple[str,SymType]] = []):
        self.members = members

class SymStructLiteral(SymType):
    def __init__(self, values : list[SymType]):
        self.values = values

class Block:
    def __init__(self):
        self.symbols : list[tuple[str,SymType]] = []
        
        # function
        self.function_context : SymFunc | None = None

        # loop
        self.in_loop = False

        # switch
        self.in_switch = False

class BindingContext:
    def __init__(self):
        self.blocks : list[Block] = []
        self.blocks.append(Block())
        self.blocks[0].symbols = [
            ("readInt" ,  SymFunc([],SymInt())),
            ("printInt" , SymFunc([("x",SymInt())],SymVoid())),
            ("readFloat" , SymFunc([],SymFloat())),
            ("printFloat", SymFunc([("x",SymFloat())],SymVoid())),
            ("readString" , SymFunc([],SymString())),
            ("printString", SymFunc([("x",SymString())],SymVoid()))
        ]

    def enter_scope(self):
        new_block = Block()
        new_block.function_context = self.blocks[-1].function_context
        new_block.in_loop = self.blocks[-1].in_loop
        new_block.in_switch = self.blocks[-1].in_switch

        self.blocks.append(new_block)

    def enter_function(self, sym_func : SymFunc):
        new_block = Block()
        new_block.function_context = sym_func
        new_block.in_loop = self.blocks[-1].in_loop
        new_block.in_switch = self.blocks[-1].in_switch

        self.blocks.append(new_block)

    def enter_switch(self):
        new_block = Block()
        new_block.function_context = self.blocks[-1].function_context
        new_block.in_loop = self.blocks[-1].in_loop
        new_block.in_switch = True

        self.blocks.append(new_block)

    def enter_loop(self):
        new_block = Block()
        new_block.function_context = self.blocks[-1].function_context
        new_block.in_loop = True
        new_block.in_switch = self.blocks[-1].in_switch

        self.blocks.append(new_block)

    def add_symbol(self, name : str, typ : SymType):
        self.blocks[-1].symbols.append((name,typ))

    def try_find_symbol_type(self, name : str):
        reversed_blocks = reversed(self.blocks)
        for block in reversed_blocks:
            for symbol in block.symbols:
                if symbol[0] == name:
                    return True, symbol[1]
            
        return False, None
    
    def try_update_symbol_type(self, name : str, sym_type : SymType):
        reversed_blocks = reversed(self.blocks)
        for block in reversed_blocks:
            for i in range(len(block.symbols)):
                if block.symbols[i][0] == name:
                    block.symbols[i] = (name, sym_type)
                    return True
            
        return False

    def try_get_struct(self, struct_name : str):
        reversed_blocks = reversed(self.blocks)
        for block in reversed_blocks:
            for sym in block.symbols:
                if sym[0] == struct_name and isinstance(sym[1], SymStruct):
                    return True, sym[1]
            
        return False, None

    def try_get_function(self, function_name : str):
        reversed_blocks = reversed(self.blocks)
        for block in reversed_blocks:
            for sym in block.symbols:
                if sym[0] == function_name and isinstance(sym[1], SymFunc):
                    return True, sym[1]
            
        return False, None
    
    def try_get_identifier(self, id_name : str):
        reversed_blocks = reversed(self.blocks)
        for block in reversed_blocks:
            for sym in block.symbols:
                if sym[0] == id_name and not isinstance(sym[1], (SymVoid, SymFunc)):
                    return True, sym[1]
            
        return False, None

    def check_redeclared(self, name : str):
        for symbol in self.blocks[-1].symbols:
            if symbol[0] == name:
                return True
            
        return False
    
    def check_shadow_function_param(self, name : str):
        if not self.blocks[-1].function_context:
            return False
        
        func_params = self.blocks[-1].function_context.params

        for param in func_params:
            if param[0] == name:
                return True
            
        return False

    def exit_scope(self, node : ASTNode = None):
        deleted_block = self.blocks.pop()
        for sym in deleted_block.symbols:
            if isinstance(sym[1], SymAuto):
                raise TypeCannotBeInferred(node)

    def exit_function(self):
        deleted_block = self.blocks.pop()
        if isinstance(deleted_block.function_context.return_type, SymAuto):
            deleted_block.function_context.return_type = VoidType()

    def get_all_struct(self):
        return [sym for block in self.blocks for sym in block.symbols if isinstance(sym[1], SymStruct)]

class StaticChecker(ASTVisitor):

    def __init__(self):
        pass

    def check_program(self, node: "Program"):
        self.visit_program(node, None)

    def visit_program(self, node: "Program", bc: BindingContext = None):
        bc = BindingContext()
        bc.enter_scope()
        for decl in node.decls:
            decl.accept(self,bc)
        bc.exit_scope(node)

    def visit_struct_decl(self, node: "StructDecl", bc: BindingContext = None):
        found,sym_type = bc.try_find_symbol_type(node.name)

        if found and isinstance(sym_type, SymStruct):
            raise Redeclared("Struct", node.name)

        new_struct = SymStruct()
        new_struct.members = []

        bc.enter_scope()
        for member in node.members:
            member.accept(self,bc)
            # new_struct.members[member.name] = member.member_type.accept(self,bc)
            new_struct.members.append((member.name, member.member_type.accept(self,bc)))
        bc.exit_scope(node)

        bc.add_symbol(node.name, new_struct)

    def visit_member_decl(self, node: "MemberDecl", bc: BindingContext = None):
        if bc.check_redeclared(node.name):
            raise Redeclared("Member", node.name)

        bc.add_symbol(node.name, node.member_type.accept(self,bc))

    def visit_func_decl(self, node: "FuncDecl", bc: BindingContext = None):
        found,sym_type = bc.try_find_symbol_type(node.name)

        if found and isinstance(sym_type, SymFunc):
            raise Redeclared("Function", node.name)
        
        new_func = SymFunc()
        new_func.params = []
        new_func.return_type = node.return_type.accept(self,bc) if node.return_type else SymAuto()

        if node.params:
            for param in node.params:
                new_ele = (param.name,param.param_type.accept(self,bc))
                new_func.params.append(new_ele)

        bc.add_symbol(node.name, new_func)
        
        bc.enter_function(new_func)
        if node.params:
            for param in node.params:
                param.accept(self,bc)

        node.body.accept(self,bc)
        bc.exit_function()

    def visit_param(self, node: "Param", bc: BindingContext = None):
        if bc.check_redeclared(node.name):
            raise Redeclared("Parameter", node.name)
        
        bc.add_symbol(node.name, node.param_type.accept(self,bc))

    # Type system
    def visit_int_type(self, node: "IntType", bc: BindingContext = None) -> SymType:
        return SymInt()

    def visit_float_type(self, node: "FloatType", bc: BindingContext = None) -> SymType:
        return SymFloat()

    def visit_string_type(self, node: "StringType", bc: BindingContext = None) -> SymType:
        return SymString()

    def visit_void_type(self, node: "VoidType", bc: BindingContext = None) -> SymType:
        return SymVoid()

    def visit_struct_type(self, node: "StructType", bc: BindingContext = None) -> SymType:
        found, struct_typ = bc.try_get_struct(node.struct_name)
        
        if not found:
            raise UndeclaredStruct(node.struct_name)
        
        return struct_typ

    # Statements
    def visit_block_stmt(self, node: "BlockStmt", bc: BindingContext = None):
        bc.enter_scope()
        if node.statements:
            for stmt in node.statements:
                stmt.accept(self,bc)
        bc.exit_scope(node)

    def visit_var_decl(self, node: "VarDecl", bc: BindingContext = None):
        if bc.check_redeclared(node.name) or bc.check_shadow_function_param(node.name):
            raise Redeclared("Variable", node.name)
        
        var_type : SymType = node.var_type.accept(self,bc) if node.var_type else SymAuto()

        if node.init_value:
            init_type : SymType = node.init_value.accept(self,bc)
            if isinstance(var_type, SymAuto):
                if isinstance(init_type, SymStructLiteral):
                    raise TypeMismatchInStatement(node)
                var_type = init_type
            elif isinstance(var_type, SymStruct) and isinstance(init_type, SymStruct):
                if var_type != init_type:
                    raise TypeMismatchInStatement(node)
            elif type(var_type) != type(init_type):
                if isinstance(var_type,SymStruct) and isinstance(init_type, SymStructLiteral):
                    self.update_auto_in_struct_literal(node.init_value, var_type, bc)
                elif isinstance(init_type, SymAuto):
                    self.update_auto_in_expr(node.init_value, var_type, bc)
                else:
                    raise TypeMismatchInStatement(node)   
            
        bc.add_symbol(node.name, var_type)

    def visit_if_stmt(self, node: "IfStmt", bc: BindingContext = None):
        condition_type = node.condition.accept(self,bc)

        if isinstance(condition_type, SymAuto):
            self.update_auto_in_expr(node.condition, SymInt(), bc)

        if not isinstance(node.condition.accept(self,bc),SymInt):
            raise TypeMismatchInStatement(node)
        
        bc.enter_scope()
        node.then_stmt.accept(self,bc)
        bc.exit_scope(node)

        bc.enter_scope()
        if node.else_stmt:
            node.else_stmt.accept(self,bc)
        bc.exit_scope(node)

    def visit_while_stmt(self, node: "WhileStmt", bc: BindingContext = None):
        condition_type = node.condition.accept(self,bc)

        if isinstance(condition_type, SymAuto):
            self.update_auto_in_expr(node.condition, SymInt(), bc)

        if not isinstance(node.condition.accept(self,bc),SymInt):
            raise TypeMismatchInStatement(node)
        
        bc.enter_loop()
        node.body.accept(self,bc)
        bc.exit_scope(node)

    def visit_for_stmt(self, node: "ForStmt", bc: BindingContext = None):
        if node.init:
            node.init.accept(self,bc)

        if node.condition:
            condition_type = node.condition.accept(self,bc)
            if isinstance(condition_type, SymAuto):
                self.update_auto_in_expr(node.condition, SymInt(), bc)
                condition_type = node.condition.accept(self,bc)

            if not isinstance(condition_type, SymInt):
                raise TypeMismatchInStatement(node)

        if node.update:
            node.update.accept(self,bc)

        bc.enter_loop()
        node.body.accept(self,bc)
        bc.exit_scope(node)

    def visit_switch_stmt(self, node: "SwitchStmt", bc: BindingContext = None):
        if isinstance(node.expr, FuncCall):
            raise TypeMismatchInStatement(node)
        
        if isinstance(node.expr.accept(self,bc), SymAuto):
            self.update_auto_in_expr(node.expr, SymInt(), bc)

        if not isinstance(node.expr.accept(self,bc), SymInt):
            raise TypeMismatchInStatement(node)

        bc.enter_switch()
        try:
            for case in node.cases:
                case.accept(self,bc)

            if node.default_case:
                node.default_case.accept(self,bc)
        except TypeMismatchInStatement as e:
            if isinstance(e.stmt, CaseStmt):
                raise TypeMismatchInStatement(node)
            else: raise e
        bc.exit_scope(node)

    def visit_case_stmt(self, node: "CaseStmt", bc: BindingContext = None):
        if not isinstance(node.expr.accept(self,bc), SymInt):
            raise TypeMismatchInStatement(node)

        if self.check_id_in_expr(node.expr):
            raise TypeMismatchInStatement(node)

        for stmt in node.statements:
            stmt.accept(self,bc)

    def visit_default_stmt(self, node: "DefaultStmt", bc: BindingContext = None):
        for stmt in node.statements:
            stmt.accept(self,bc)

    def visit_break_stmt(self, node: "BreakStmt", bc: BindingContext = None):
        if not bc.blocks[-1].in_switch and not bc.blocks[-1].in_loop:
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: "ContinueStmt", bc: BindingContext = None):
        if not bc.blocks[-1].in_loop:
            raise MustInLoop(node)

    def visit_return_stmt(self, node: "ReturnStmt", bc: BindingContext = None):
        if bc.blocks[-1].function_context == None:
            raise TypeMismatchInStatement(node)
        
        return_type = bc.blocks[-1].function_context.return_type
        expr_type : SymType = node.expr.accept(self,bc) if node.expr else SymVoid()

        if isinstance(return_type, SymAuto):
            if isinstance(expr_type, SymAuto):
                raise TypeCannotBeInferred(node)
            bc.blocks[-1].function_context.return_type = expr_type
        else:
            if isinstance(expr_type, SymAuto):
                self.update_auto_in_expr(node.expr, return_type, bc)
                expr_type = node.expr.accept(self,bc)

            if type(return_type) != type(expr_type):
                raise TypeMismatchInStatement(node)

    def visit_expr_stmt(self, node: "ExprStmt", bc: BindingContext = None):
        try:
            expr_type = node.expr.accept(self,bc)
            if isinstance(expr_type, SymAuto):
                raise TypeCannotBeInferred(node.expr)
        except TypeMismatchInExpression as e:
            if isinstance(e.expr, AssignExpr) and e.expr == node.expr:
                raise TypeMismatchInStatement(node)
            else:
                raise e
    # Expressions
    def visit_binary_op(self, node: "BinaryOp", bc: BindingContext = None) -> SymType:
        left_type : SymType = node.left.accept(self,bc)
        right_type : SymType = node.right.accept(self,bc)

        # int int operator
        if node.operator in ['%', '&&' , '||']:
            if not isinstance(left_type, (SymAuto, SymInt)) or not isinstance(right_type, (SymInt, SymAuto)):
                raise TypeMismatchInExpression(node)
            self.update_auto_in_binary_op(node, SymInt(), bc)
            
            return SymInt()
        else: # int - float operator
            if node.operator in ['+', '-', '*', '/']:
                has_intlit = isinstance(node.left, IntLiteral) or isinstance(node.right, IntLiteral)
                has_auto = isinstance(left_type, SymAuto) or isinstance(right_type, SymAuto)
                if has_intlit and has_auto:
                    self.update_auto_in_binary_op(node, SymInt(), bc)
                    left_type = node.left.accept(self,bc)
                    right_type = node.right.accept(self,bc)

            if isinstance(left_type, SymAuto) and isinstance(right_type, SymAuto):
                raise TypeCannotBeInferred(node)
        
            if not isinstance(left_type, (SymAuto, SymInt, SymFloat)) or not isinstance(right_type, (SymAuto, SymInt, SymFloat)):
                raise TypeMismatchInExpression(node)
            
            if isinstance(left_type, SymAuto) or isinstance(right_type, SymAuto):
                raise TypeCannotBeInferred(node)
            else:
                if isinstance(left_type, SymFloat) or isinstance(right_type, SymFloat):
                    if node.operator in ['>=', '>', '<', '<=']:
                        return SymInt()
                    return SymFloat()
                return SymInt()
                

    def visit_prefix_op(self, node: "PrefixOp", bc: BindingContext = None) -> SymType:
        # FIX ME
        if node.operator in ['++','--'] and not isinstance(node.operand, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)

        type_operand : SymType = node.operand.accept(self,bc)

        if isinstance(type_operand, SymAuto):
            if node.operator in ['++', '--' , '!']:
                self.update_auto_in_expr(node.operand, SymInt(), bc)
            else:
                raise TypeCannotBeInferred(node)

        type_operand = node.operand.accept(self,bc)

        if node.operator in ['++','--', '!']:
            if not isinstance(type_operand, SymInt):
                raise TypeMismatchInExpression(node)
            return SymInt()
        else:
            if not isinstance(type_operand, (SymInt, SymFloat)):
                raise TypeMismatchInExpression(node)
            return type_operand

    def visit_postfix_op(self, node: "PostfixOp", bc: BindingContext = None) -> SymType:
        # FIX ME
        if not isinstance(node.operand, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)

        type_operand : SymType = node.operand.accept(self,bc)

        if isinstance(type_operand, SymAuto):
            self.update_auto_in_expr(node.operand, SymInt(), bc)
            type_operand = node.operand.accept(self,bc)

        if not isinstance(type_operand, SymInt):
            raise TypeMismatchInExpression(node)

        return type_operand

    def visit_assign_expr(self, node: "AssignExpr", bc: BindingContext = None) -> SymType:
        left_type : SymType = node.lhs.accept(self,bc)
        right_type : SymType = node.rhs.accept(self,bc)
    
        if isinstance(left_type, SymAuto) or isinstance(right_type, SymAuto):
            if isinstance(left_type, SymAuto) and isinstance(right_type, SymAuto):
                raise TypeCannotBeInferred(node)
            try:
                if isinstance(left_type, SymAuto):
                    self.update_auto_in_assign_expr(node, right_type, bc)
                    return right_type
                else:
                    self.update_auto_in_assign_expr(node, left_type, bc)
                    return left_type
            except:
                    raise TypeCannotBeInferred(node)
        
        if isinstance(left_type, SymStruct) and isinstance(right_type, SymStruct):
            if left_type != right_type:
                raise TypeMismatchInExpression(node)

        if isinstance(left_type, SymStruct) and isinstance(right_type, SymStructLiteral):
            struct_members = left_type.members
            literal_values = right_type.values

            if len(struct_members) != len(literal_values):
                raise TypeMismatchInExpression(node)
            
            for i in range(len(struct_members)):
                if type(struct_members[i][1]) != type(literal_values[i]):
                    raise TypeMismatchInExpression(node)

            return left_type
        
        if type(left_type) != type(right_type):
            raise TypeMismatchInExpression(node)
        
        return left_type

    def visit_member_access(self, node: "MemberAccess", bc: BindingContext = None) -> SymType:
        obj_type : SymType = node.obj.accept(self,bc)

        if not isinstance(obj_type, SymStruct):
            raise TypeMismatchInExpression(node)

        for member in obj_type.members:
            if member[0] == node.member:
                return member[1]
        
        raise TypeMismatchInExpression(node)

    def visit_func_call(self, node: "FuncCall", bc: BindingContext = None) -> SymType:
        found,sym_type = bc.try_get_function(node.name)

        if not found:
            raise UndeclaredFunction(node.name)

        if len(node.args) != len(sym_type.params):
            raise TypeMismatchInExpression(node)

        for i in range(len(node.args)):
            arg = node.args[i]
            arg_type = arg.accept(self,bc)
            param_type = sym_type.params[i][1]
            if isinstance(arg, Identifier) and isinstance(arg_type, SymAuto):
                bc.try_update_symbol_type(arg.name, param_type)
                _, arg_type = bc.try_get_identifier(arg.name)
            if isinstance(arg_type, SymStruct) and isinstance(param_type, SymStruct):
                if arg_type != param_type:
                    raise TypeMismatchInExpression(node)
            if type(arg_type) != type(param_type):
                raise TypeMismatchInExpression(node)

        return sym_type.return_type

    def visit_identifier(self, node: "Identifier", bc: BindingContext = None) -> SymType:
        found, sym_type = bc.try_get_identifier(node.name)

        if not found:
            raise UndeclaredIdentifier(node.name)
        
        return sym_type

    def visit_struct_literal(self, node: "StructLiteral", bc: BindingContext = None) -> SymType:
        typs : list[SymType] = []
        for value in node.values:
            typs.append(value.accept(self,bc))

        return SymStructLiteral(typs)

    # Literals
    def visit_int_literal(self, node: "IntLiteral", bc: BindingContext = None) -> SymType:
        return SymInt()

    def visit_float_literal(self, node: "FloatLiteral", bc: BindingContext = None) -> SymType:
        return SymFloat()

    def visit_string_literal(self, node: "StringLiteral", bc: BindingContext = None) -> SymType:
        return SymString()
    
    def update_auto_in_expr(self, node : "Expr", typ : SymType, bc : BindingContext = None) -> SymType:
        if isinstance(node, BinaryOp):
            self.update_auto_in_binary_op(node,typ,bc)
        elif isinstance(node, PrefixOp):
            self.update_auto_in_prefix_op(node,typ,bc)
        elif isinstance(node, PostfixOp):
            self.update_auto_in_postfix_op(node,typ,bc)
        elif isinstance(node, AssignExpr):
            self.update_auto_in_assign_expr(node,typ,bc)
        elif isinstance(node, MemberAccess):
            self.update_auto_in_member_access(node,typ,bc)
        elif isinstance(node, FuncCall):
            self.update_auto_in_func_call(node,typ,bc)
        elif isinstance(node, Identifier):
            self.update_auto_in_identifier(node,typ,bc)
        elif isinstance(node, StructLiteral):
            self.update_auto_in_struct_literal(node,typ,bc)
        elif isinstance(node, IntLiteral):
            self.update_auto_in_int_literal(node,typ,bc)
        elif isinstance(node, FloatLiteral):
            self.update_auto_in_float_literal(node,typ,bc)
        elif isinstance(node, StringLiteral):
            self.update_auto_in_string_literal(node,typ,bc)

    def update_auto_in_binary_op(self, node : "BinaryOp", typ : SymType, bc : BindingContext = None):
        if isinstance(typ, SymInt):
            if node.operator in ['+', '-', '*', '/', '&&', '||', '%']:
                self.update_auto_in_expr(node.left, SymInt(), bc)
                self.update_auto_in_expr(node.right, SymInt(), bc)
            else:
                left_type = node.left.accept(self,bc)
                right_type = node.right.accept(self,bc)

                if isinstance(left_type, SymAuto) or isinstance(right_type, SymAuto):
                    raise TypeCannotBeInferred(node)

        elif isinstance(typ, SymFloat):
            if node.operator in ['&&', '||', '%']:
                raise TypeCannotBeInferred(node)

            left_type = node.left.accept(self,bc)
            right_type = node.right.accept(self,bc)

            if isinstance(node.left, IntLiteral) or isinstance(node.right, IntLiteral):
                raise TypeCannotBeInferred(node)

            if isinstance(left_type, SymAuto) or isinstance(right_type, SymAuto):
                raise TypeCannotBeInferred(node)

        else:
            raise TypeCannotBeInferred(node)
        
    def update_auto_in_prefix_op(self, node : "PrefixOp", typ : SymType, bc : BindingContext = None):    
        if not isinstance(typ, (SymInt, SymFloat)):
            raise TypeCannotBeInferred(node)
        
        if node.operator in ['++', '--', '!']:
            if isinstance(typ, SymFloat):
                raise TypeCannotBeInferred(node)
            self.update_auto_in_expr(node.operand,SymInt(), bc)
        else:
            self.update_auto_in_expr(node.operand,typ,bc)

    def update_auto_in_postfix_op(self, node : "PostfixOp", typ : SymType, bc : BindingContext = None):
        if not isinstance(typ, SymInt):
            raise TypeCannotBeInferred(node)
        
        self.update_auto_in_expr(node.operand,SymInt(), bc)

    def update_auto_in_assign_expr(self, node : "AssignExpr", typ : SymType, bc : BindingContext = None):
        self.update_auto_in_expr(node.lhs, typ, bc)
        self.update_auto_in_expr(node.rhs, typ, bc)

    def update_auto_in_member_access(self, node : "MemberAccess", typ : SymType, bc : BindingContext = None):
        expr_type = self.visit_member_access(node,bc)

        if type(expr_type) != type(typ):
            raise TypeCannotBeInferred(node)
        
    def update_auto_in_func_call(self, node : "FuncCall", typ : SymType, bc : BindingContext = None):
        func_return_type = self.visit_func_call(node,bc)
        if type(func_return_type) != type(typ):
            raise TypeCannotBeInferred(node)
        
    def update_auto_in_identifier(self, node : "Identifier", typ : SymType, bc : BindingContext = None):
        id_type = self.visit_identifier(node,bc)
        if isinstance(id_type, SymAuto):
            bc.try_update_symbol_type(node.name, typ)
        elif type(id_type) != type(typ):
            raise TypeCannotBeInferred(node)

    def update_auto_in_struct_literal(self, node : "StructLiteral", typ : SymType, bc : BindingContext = None):
        if not isinstance(typ, (SymStructLiteral, SymStruct)):
            raise TypeMismatchInExpression(node)

        if isinstance(typ, SymStructLiteral):
            if len(node.values) != len(typ.values):
                raise TypeMismatchInExpression(node)
            
            for i in range(len(node.values)):
                if isinstance(node.values[i].accept(self,bc), SymAuto):
                    self.update_auto_in_expr(node.values[i], typ.values[i], bc)
                elif type(node.values[i].accept(self,bc)) != type(typ.values[i]):
                    raise TypeMismatchInExpression(node)
                
        if isinstance(typ, SymStruct):
            if len(node.values) != len(typ.members):
                raise TypeMismatchInExpression(node)
            
            for i in range(len(node.values)):
                if isinstance(node.values[i].accept(self,bc), SymAuto):
                    self.update_auto_in_expr(node.values[i], typ.members[i][1], bc)
                elif type(node.values[i].accept(self,bc)) != type(typ.members[i][1]):
                    raise TypeMismatchInExpression(node)
        
    def update_auto_in_int_literal(self, node : "IntLiteral", typ : SymType, bc : BindingContext):
        if not isinstance(typ, SymInt):
            raise TypeCannotBeInferred(node)
        
    def update_auto_in_float_literal(self, node : "FloatLiteral", typ : SymType, bc : BindingContext):
        if not isinstance(typ, SymFloat):
            raise TypeCannotBeInferred(node)
        
    def update_auto_in_string_literal(self, node : "StringLiteral", typ : SymType, bc : BindingContext):
        if not isinstance(typ, SymString):
            raise TypeCannotBeInferred(node)
        
    def check_id_in_expr(self, node : "Expr") -> bool:
        if isinstance(node, BinaryOp):
            return self.check_id_in_binary_op(node)
        elif isinstance(node, PrefixOp):
            return self.check_id_in_prefix_op(node)
        elif isinstance(node, PostfixOp):
            return self.check_id_in_postfix_op(node)
        elif isinstance(node, AssignExpr):
            return self.check_id_in_assign_expr(node)
        elif isinstance(node, MemberAccess):
            return self.check_id_in_member_acces(node)
        elif isinstance(node, FuncCall):
            return self.check_id_in_func_call(node)
        elif isinstance(node, Identifier):
            return self.check_id_in_id(node)
        elif isinstance(node, StructLiteral):
            return self.check_id_in_struct_literal(node)
        elif isinstance(node, IntLiteral):
            return self.check_id_in_int_literal(node)
        elif isinstance(node, FloatLiteral):
            return self.check_id_in_float_literal(node)
        elif isinstance(node, StringLiteral):
            return self.check_id_in_string_literal(node)

    def check_id_in_binary_op(self, node : "BinaryOp"):
        return self.check_id_in_expr(node.left) and self.check_id_in_expr(node.right)
    
    def check_id_in_prefix_op(self, node : "PrefixOp"):
        return self.check_id_in_expr(node.operand)
    
    def check_id_in_postfix_op(self, node : "PostfixOp"):
        return self.check_id_in_expr(node.operand)
    
    def check_id_in_func_call(self, node : "FuncCall"):
        return True
    
    def check_id_in_member_acces(self, node : "MemberAccess"):
        return True

    def check_id_in_assign_expr(self, node : "AssignExpr"):
        return True
    
    def check_id_in_id(self, node : "Identifier"):
        return True
    
    def check_id_in_struct_literal(self, node : "StructLiteral"):
        return reduce(
            lambda acc, ele : acc and ele,
            [self.check_id_in_expr(value) for value in node.values],
            True
        )
    
    def check_id_in_int_literal(self, node : "IntLiteral"):
        return False
    
    def check_id_in_float_literal(self, node : "FloatLiteral"):
        return False
    
    def check_id_in_string_literal(self, node : "StringLiteral"):
        return False