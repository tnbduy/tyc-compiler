"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *

LOGIC_OR_OP = '||'
LOGIC_AND_OP = '&&'
LOGIC_NOT_OP = '!'
EQ_OP = '=='
NEQ_OP = '!='
LT_OP = '<'
GT_OP = '>'
LTE_OP = '<='
GTE_OP = '>='
ADD_OP = '+'
SUB_OP = '-'
MUL_OP = '*'
DIV_OP = '/'
MOD_OP = '%'
INC_OP = '++'
DEC_OP = '--'

class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""

    # program: (struct_decl | function_decl)* EOF
    def visitProgram(self, ctx:TyCParser.ProgramContext):
        return Program([structDeclaration.accept(self) for structDeclaration in ctx.struct_decl()] + [functionDeclaration.accept(self) for functionDeclaration in ctx.function_decl()])

    # struct_decl: STRUCT_KEYWORD ID LB_SEP member_list? RB_SEP SM_SEP
    def visitStruct_decl(self, ctx:TyCParser.Struct_declContext):
        return StructDecl(ctx.ID().getText(), ctx.member_list().accept(self) if ctx.member_list() else [])


    # member_list: member member_list | member
    def visitMember_list(self, ctx:TyCParser.Member_listContext):
        if ctx.getChildCount() == 1: #member
            return [ctx.member().accept(self)]
        
        #member member_list
        return [ctx.member().accept(self)] + ctx.member_list().accept(self)


    # member: member_type ID SM_SEP.
    def visitMember(self, ctx:TyCParser.MemberContext):
        return MemberDecl(ctx.member_type().accept(self), ctx.ID().getText())


    # member_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | ID;
    def visitMember_type(self, ctx:TyCParser.Member_typeContext):
        if ctx.ID():
            return StructType(ctx.ID().getText())
        
        if ctx.INT_KEYWORD():
            return IntType()
        
        if ctx.FLOAT_KEYWORD():
            return FloatType()
        
        if ctx.STRING_KEYWORD():
            return StringType()
        

    # function_decl : function_ret_type? ID LP_SEP param_list? RP_SEP LB_SEP statement_list? RB_SEP;
    def visitFunction_decl(self, ctx:TyCParser.Function_declContext):
        function_type = ctx.function_ret_type().accept(self) if ctx.function_ret_type() else None
        function_name = ctx.ID().getText()
        function_paramList = ctx.param_list().accept(self) if ctx.param_list() else None
        function_blockstmt = BlockStmt(ctx.statement_list().accept(self)) if ctx.statement_list() else BlockStmt([])

        return FuncDecl(function_type,function_name,function_paramList,function_blockstmt)

    # function_ret_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | ID | VOID_KEYWORD;
    def visitFunction_ret_type(self, ctx:TyCParser.Function_ret_typeContext):
        if ctx.ID():
            return StructType(ctx.ID().getText())
        
        if ctx.INT_KEYWORD():
            return IntType()
        
        if ctx.FLOAT_KEYWORD():
            return FloatType()
        
        if ctx.STRING_KEYWORD():
            return StringType()
        
        if ctx.VOID_KEYWORD():
            return VoidType()


    # param_list : param CM_SEP param_list | param;
    def visitParam_list(self, ctx:TyCParser.Param_listContext):
        if ctx.getChildCount() == 1: #param
            return [ctx.param().accept(self)]
        
        return [ctx.param().accept(self)] + ctx.param_list().accept(self)


    # param : param_type ID;
    def visitParam(self, ctx:TyCParser.ParamContext):
        return Param(ctx.param_type().accept(self), ctx.ID().getText())


    # param_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | ID;
    def visitParam_type(self, ctx:TyCParser.Param_typeContext):
        if ctx.INT_KEYWORD():
            return IntType()
        
        if ctx.FLOAT_KEYWORD():
            return FloatType()
        
        if ctx.STRING_KEYWORD():
            return StringType()
        
        if ctx.ID():
            return StructType(ctx.ID().getText())


    # list_expression : expression CM_SEP list_expression | expression;
    def visitList_expression(self, ctx:TyCParser.List_expressionContext):
        if ctx.getChildCount() == 1: # expression
            return [ctx.expression().accept(self)]
        
        # expression CM_SEP list_expression
        return [ctx.expression().accept(self)] + ctx.list_expression().accept(self)


    # expression : expression1 ASSIGN_OP expression | expression1;
    def visitExpression(self, ctx:TyCParser.ExpressionContext):
        if ctx.getChildCount() == 1: #expression
            return ctx.expression1().accept(self)
        
        # expression1 ASSIGN_OP expression
        return AssignExpr(ctx.expression1().accept(self),ctx.expression().accept(self))


    # expression1 : expression1 LOGIC_OR_OP expression2 | expression2;
    def visitExpression1(self, ctx:TyCParser.Expression1Context):
        if ctx.getChildCount() == 1: # expression2
            return ctx.expression2().accept(self)
        
        return BinaryOp(ctx.expression1().accept(self), LOGIC_OR_OP, ctx.expression2().accept(self))


    # expression2 : expression2 LOGIC_AND_OP expression3 | expression3;
    def visitExpression2(self, ctx:TyCParser.Expression2Context):
        if ctx.getChildCount() == 1: # expression3
            return ctx.expression3().accept(self)
        
        return BinaryOp(ctx.expression2().accept(self), LOGIC_AND_OP, ctx.expression3().accept(self))


    # expression3 : expression3 (EQ_OP | NEQ_OP) expression4 | expression4;
    def visitExpression3(self, ctx:TyCParser.Expression3Context):
        if ctx.getChildCount() == 1: # expression4
            return ctx.expression4().accept(self)
        
        return BinaryOp(ctx.expression3().accept(self), (EQ_OP if ctx.EQ_OP() else NEQ_OP), ctx.expression4().accept(self))


    # expression4 : expression4 (LT_OP | LTE_OP | GT_OP | GTE_OP) expression5 | expression5;
    def visitExpression4(self, ctx:TyCParser.Expression4Context):
        if ctx.getChildCount() == 1:
            return ctx.expression5().accept(self)
        
        op = LT_OP
        if ctx.LT_OP(): op = LT_OP
        if ctx.GT_OP(): op = GT_OP
        if ctx.GTE_OP(): op = GTE_OP
        if ctx.LTE_OP(): op = LTE_OP

        return BinaryOp(ctx.expression4().accept(self), op, ctx.expression5().accept(self))


    # expression5 : expression5 (ADD_OP | SUB_OP) expression6 | expression6;
    def visitExpression5(self, ctx:TyCParser.Expression5Context):
        if ctx.getChildCount() == 1: # expression6
            return ctx.expression6().accept(self)
        
        return BinaryOp(ctx.expression5().accept(self), ADD_OP if ctx.ADD_OP() else SUB_OP, ctx.expression6().accept(self))


    # expression6 : expression6 (MUL_OP | DIV_OP | MOD_OP) expression7 | expression7;
    def visitExpression6(self, ctx:TyCParser.Expression6Context):
        if ctx.getChildCount() == 1: # expression7
            return ctx.expression7().accept(self)
        
        op = MUL_OP
        if ctx.MUL_OP(): op = MUL_OP
        if ctx.DIV_OP(): op = DIV_OP
        if ctx.MOD_OP(): op = MOD_OP

        return BinaryOp(ctx.expression6().accept(self), op, ctx.expression7().accept(self))


    # expression7 : (LOGIC_NOT_OP | ADD_OP | SUB_OP) expression7 | expression8;
    def visitExpression7(self, ctx:TyCParser.Expression7Context):
        if ctx.getChildCount() == 1: # expression8
            return ctx.expression8().accept(self)
        
        op = LOGIC_AND_OP
        if ctx.LOGIC_NOT_OP(): op = LOGIC_NOT_OP
        if ctx.ADD_OP(): op = ADD_OP
        if ctx.SUB_OP(): op = SUB_OP

        return PrefixOp(op, ctx.expression7().accept(self))


    # expression8 : (INC_OP | DEC_OP) expression8 | expression9;
    def visitExpression8(self, ctx:TyCParser.Expression8Context):
        if ctx.getChildCount() == 1: # expression9
            return ctx.expression9().accept(self)
        
        return PrefixOp(INC_OP if ctx.INC_OP() else DEC_OP, ctx.expression8().accept(self))


    # expression9 : expression9 (INC_OP | DEC_OP) | expression10 | call_function;
    def visitExpression9(self, ctx:TyCParser.Expression9Context):
        if ctx.getChildCount() ==  1: # (expression10 | call_func)
            return ctx.expression10().accept(self) if ctx.expression10() else ctx.call_function().accept(self)

        return PostfixOp(INC_OP if ctx.INC_OP() else DEC_OP, ctx.expression9().accept(self))


    # expression10 : struct_mem_id | expression11;
    def visitExpression10(self, ctx:TyCParser.Expression10Context):
        return ctx.struct_mem_id().accept(self) if ctx.struct_mem_id() else ctx.expression11().accept(self)


    # expression11 : INT_LIT | FLOAT_LIT | STR_LIT | ID | LP_SEP expression RP_SEP | LB_SEP list_expression? RB_SEP;
    def visitExpression11(self, ctx:TyCParser.Expression11Context):
        if ctx.getChildCount() == 1:
            if ctx.INT_LIT():
                return IntLiteral(int(ctx.INT_LIT().getText()))
        
            if ctx.FLOAT_LIT():
                return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        
            if ctx.STR_LIT():
                return StringLiteral(ctx.STR_LIT().getText())
        
            if ctx.ID():
                return Identifier(ctx.ID().getText())

        if ctx.getChildCount() > 1: # BULLSHIT CODE HERE
            if ctx.LP_SEP() and ctx.expression() and ctx.RP_SEP():
                return ctx.expression().accept(self)

            if ctx.LB_SEP() and ctx.RB_SEP():
                return StructLiteral(ctx.list_expression().accept(self) if ctx.list_expression() else [])


    # pre_post_update : (INC_OP | DEC_OP) pre_post_update | pre_post_update (INC_OP | DEC_OP) | (INC_OP | DEC_OP) expression10 | expression10 (INC_OP | DEC_OP);
    def visitPre_post_update(self, ctx:TyCParser.Pre_post_updateContext):
        firstChild = ctx.getChild(0)
        secondChild = ctx.getChild(1)

        if isinstance(firstChild,(TyCParser.Pre_post_updateContext,TyCParser.Expression10Context)): #if this is postfix update
            return PostfixOp(INC_OP if ctx.INC_OP() else DEC_OP, firstChild.accept(self))
        else: # prefix update
            return PrefixOp(INC_OP if ctx.INC_OP() else DEC_OP, secondChild.accept(self))

    # call_function: call_function ID LP_SEP list_expression? RP_SEP | ID LP_SEP list_expression? RP_SEP;
    def visitCall_function(self, ctx:TyCParser.Call_functionContext):
        return FuncCall(ctx.ID().getText(), ctx.list_expression().accept(self) if ctx.list_expression() else "")


    # struct_mem_id : struct_mem_id MEM_ACCESS_OP ID | (call_function | expression11) MEM_ACCESS_OP ID;
    def visitStruct_mem_id(self, ctx:TyCParser.Struct_mem_idContext):
        return MemberAccess(ctx.getChild(0).accept(self), ctx.ID().getText())


    # assign_expression : (struct_mem_id | ID) ASSIGN_OP expression;
    def visitAssign_expression(self, ctx:TyCParser.Assign_expressionContext):
        if ctx.struct_mem_id():
            return AssignExpr(ctx.struct_mem_id().accept(self), ctx.expression().accept(self))
        
        return AssignExpr(Identifier(ctx.ID().getText()), ctx.expression().accept(self))


    # statement_list : statement statement_list | statement;
    def visitStatement_list(self, ctx:TyCParser.Statement_listContext):
        if ctx.getChildCount() == 1: # statement
            return [ctx.statement().accept(self)]
        
        return [ctx.statement().accept(self)] + ctx.statement_list().accept(self)

    """
    statement : var_decl_statement SM_SEP
            | block_statement
            | if_statement
            | while_statement
            | for_statement
            | switch_statement
            | break_statement SM_SEP
            | continue_statement SM_SEP
            | return_statement SM_SEP
            | expression_statement SM_SEP
    """
    def visitStatement(self, ctx:TyCParser.StatementContext):
        return ctx.getChild(0).accept(self)


    # var_decl_statement : premitive_decl;
    def visitVar_decl_statement(self, ctx:TyCParser.Var_decl_statementContext):
        return ctx.premitive_decl().accept(self)


    # premitive_decl : var_type ID (ASSIGN_OP expression)?;
    def visitPremitive_decl(self, ctx:TyCParser.Premitive_declContext):
        return VarDecl(ctx.var_type().accept(self), ctx.ID().getText(),ctx.expression().accept(self) if ctx.expression() else None)


    # var_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | AUTO_KEYWORD | ID;
    def visitVar_type(self, ctx:TyCParser.Var_typeContext):
        if ctx.INT_KEYWORD():
            return IntType()
        
        if ctx.FLOAT_KEYWORD():
            return FloatType()
        
        if ctx.STRING_KEYWORD():
            return StringType()
        
        if ctx.AUTO_KEYWORD():
            return None
        
        if ctx.ID():
            return StructType(ctx.ID().getText())

    # block_statement : LB_SEP statement_list? RB_SEP;
    def visitBlock_statement(self, ctx:TyCParser.Block_statementContext):
        return BlockStmt(ctx.statement_list().accept(self) if ctx.statement_list() else None)


    # if_statement : IF_KEYWORD LP_SEP expression RP_SEP statement (ELSE_KEYWORD statement)?;
    def visitIf_statement(self, ctx:TyCParser.If_statementContext):
        return IfStmt(ctx.expression().accept(self), ctx.statement(0).accept(self), ctx.statement(1).accept(self) if ctx.statement(1) else None)


    # while_statement : WHILE_KEYWORD LP_SEP expression RP_SEP statement;
    def visitWhile_statement(self, ctx:TyCParser.While_statementContext):
        return WhileStmt(ctx.expression().accept(self), ctx.statement().accept(self))

    # for_statement : FOR_KEYWORD LP_SEP for_init? SM_SEP for_condition? SM_SEP for_update? RP_SEP statement;
    def visitFor_statement(self, ctx:TyCParser.For_statementContext):
        for_init = None
        if ctx.for_init():
            if isinstance(ctx.for_init().accept(self),AssignExpr):
                for_init = ExprStmt(ctx.for_init().accept(self))
            else:
                for_init = ctx.for_init().accept(self)
        
        for_condition = ctx.for_condition().accept(self) if ctx.for_condition() else None
        for_update = ctx.for_update().accept(self) if ctx.for_update() else None
        for_stmt = ctx.statement().accept(self)

        return ForStmt(for_init,for_condition,for_update,for_stmt)


    # for_init : var_decl_statement | assign_expression;
    def visitFor_init(self, ctx:TyCParser.For_initContext):
        return ctx.getChild(0).accept(self)


    # for_condition : expression;
    def visitFor_condition(self, ctx:TyCParser.For_conditionContext):
        return ctx.expression().accept(self)


    # for_update : assign_expression | pre_post_update;
    def visitFor_update(self, ctx:TyCParser.For_updateContext):
        return ctx.getChild(0).accept(self)


    # switch_statement : SWITCH_KEYWORD LP_SEP expression RP_SEP LB_SEP case_list? default_switch? case_list? RB_SEP;
    def visitSwitch_statement(self, ctx:TyCParser.Switch_statementContext):
        case_list = [case for caseList in ctx.case_list() for case in caseList.accept(self)] # flatten
        default_case = ctx.default_switch().accept(self) if ctx.default_switch() else None
        return SwitchStmt(ctx.expression().accept(self),case_list,default_case)


    # case_list : case case_list | case;
    def visitCase_list(self, ctx:TyCParser.Case_listContext):
        if ctx.getChildCount() == 1:
            return [ctx.case().accept(self)]
        
        return [ctx.case().accept(self)] + ctx.case_list().accept(self)


    # case : CASE_KEYWORD expression COLON_SEP statement_list?;
    def visitCase(self, ctx:TyCParser.CaseContext):
        return CaseStmt(ctx.expression().accept(self), ctx.statement_list().accept(self) if ctx.statement_list() else [])


    # default_switch : DEFAULT_KEYWORD COLON_SEP statement_list?; 
    def visitDefault_switch(self, ctx:TyCParser.Default_switchContext):
        return DefaultStmt(ctx.statement_list().accept(self) if ctx.statement_list() else [])


    # break_statement : BREAK_KEYWORD;
    def visitBreak_statement(self, ctx:TyCParser.Break_statementContext):
        return BreakStmt()


    # continue_statement : CONTINUE_KEYWORD;
    def visitContinue_statement(self, ctx:TyCParser.Continue_statementContext):
        return ContinueStmt()


    # return_statement : RETURN_KEYWORD expression?;
    def visitReturn_statement(self, ctx:TyCParser.Return_statementContext):
        return ReturnStmt(ctx.expression().accept(self) if ctx.expression() else None)


    # expression_statement : expression;
    def visitExpression_statement(self, ctx:TyCParser.Expression_statementContext):
        return ExprStmt(ctx.expression().accept(self))