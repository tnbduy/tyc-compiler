"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""

    # program: (struct_decl | function_decl)* EOF
    def visitProgram(self, ctx:TyCParser.ProgramContext):
        return self.visitChildren(ctx)


    # struct_decl: STRUCT_KEYWORD ID LB_SEP member_list? RB_SEP SM_SEP
    def visitStruct_decl(self, ctx:TyCParser.Struct_declContext):
        return self.visitChildren(ctx)


    # member_list: member member_list | member
    def visitMember_list(self, ctx:TyCParser.Member_listContext):
        return self.visitChildren(ctx)


    # member: member_type ID SM_SEP.
    def visitMember(self, ctx:TyCParser.MemberContext):
        return self.visitChildren(ctx)


    # member_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | ID;
    def visitMember_type(self, ctx:TyCParser.Member_typeContext):
        return self.visitChildren(ctx)


    # function_decl : function_ret_type? ID LP_SEP param_list? RP_SEP LB_SEP statement_list? RB_SEP;
    def visitFunction_decl(self, ctx:TyCParser.Function_declContext):
        return self.visitChildren(ctx)


    # function_ret_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | ID | VOID_KEYWORD;
    def visitFunction_ret_type(self, ctx:TyCParser.Function_ret_typeContext):
        return self.visitChildren(ctx)


    # param_list : param CM_SEP param_list | param;
    def visitParam_list(self, ctx:TyCParser.Param_listContext):
        return self.visitChildren(ctx)


    # param : param_type ID;
    def visitParam(self, ctx:TyCParser.ParamContext):
        return self.visitChildren(ctx)


    # param_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | ID;
    def visitParam_type(self, ctx:TyCParser.Param_typeContext):
        return self.visitChildren(ctx)


    # list_expression : expression CM_SEP list_expression | expression;
    def visitList_expression(self, ctx:TyCParser.List_expressionContext):
        return self.visitChildren(ctx)


    # expression : assign_expression | expression1;
    def visitExpression(self, ctx:TyCParser.ExpressionContext):
        return self.visitChildren(ctx)


    # expression1 : expression1 LOGIC_OR_OP expression2 | expression2;
    def visitExpression1(self, ctx:TyCParser.Expression1Context):
        return self.visitChildren(ctx)


    # expression2 : expression2 LOGIC_AND_OP expression3 | expression3;
    def visitExpression2(self, ctx:TyCParser.Expression2Context):
        return self.visitChildren(ctx)


    # expression3 : expression3 (EQ_OP | NEQ_OP) expression4 | expression4;
    def visitExpression3(self, ctx:TyCParser.Expression3Context):
        return self.visitChildren(ctx)


    # expression4 : expression4 (LT_OP | LTE_OP | GT_OP | GTE_OP) expression5 | expression5;
    def visitExpression4(self, ctx:TyCParser.Expression4Context):
        return self.visitChildren(ctx)


    # expression5 : expression5 (ADD_OP | SUB_OP) expression6 | expression6;
    def visitExpression5(self, ctx:TyCParser.Expression5Context):
        return self.visitChildren(ctx)


    # expression6 : expression6 (MUL_OP | DIV_OP | MOD_OP) expression7 | expression7;
    def visitExpression6(self, ctx:TyCParser.Expression6Context):
        return self.visitChildren(ctx)


    # expression7 : (LOGIC_NOT_OP | ADD_OP | SUB_OP) expression7 | expression8;
    def visitExpression7(self, ctx:TyCParser.Expression7Context):
        return self.visitChildren(ctx)


    # expression8 : (INC_OP | DEC_OP) expression8 | expression9;
    def visitExpression8(self, ctx:TyCParser.Expression8Context):
        return self.visitChildren(ctx)


    # expression9 : expression9 (INC_OP | DEC_OP) | expression10 | call_function;
    def visitExpression9(self, ctx:TyCParser.Expression9Context):
        return self.visitChildren(ctx)


    # expression10 : struct_mem_id | expression11;
    def visitExpression10(self, ctx:TyCParser.Expression10Context):
        return self.visitChildren(ctx)


    # expression11 : INT_LIT | FLOAT_LIT | STR_LIT | ID | LP_SEP expression RP_SEP | LB_SEP list_expression? RB_SEP;
    def visitExpression11(self, ctx:TyCParser.Expression11Context):
        return self.visitChildren(ctx)


    # pre_post_update : (INC_OP | DEC_OP) pre_post_update | pre_post_update (INC_OP | DEC_OP) | (INC_OP | DEC_OP) expression10 | expression10 (INC_OP | DEC_OP);
    def visitPre_post_update(self, ctx:TyCParser.Pre_post_updateContext):
        return self.visitChildren(ctx)


    # call_function: call_function ID LP_SEP list_expression? RP_SEP | ID LP_SEP list_expression? RP_SEP;
    def visitCall_function(self, ctx:TyCParser.Call_functionContext):
        return self.visitChildren(ctx)


    # struct_mem_id : struct_mem_id MEM_ACCESS_OP ID | (call_function | expression11) MEM_ACCESS_OP ID;
    def visitStruct_mem_id(self, ctx:TyCParser.Struct_mem_idContext):
        return self.visitChildren(ctx)


    # assign_expression : (struct_mem_id | ID) ASSIGN_OP expression;
    def visitAssign_expression(self, ctx:TyCParser.Assign_expressionContext):
        return self.visitChildren(ctx)


    # statement_list : statement statement_list | statement;
    def visitStatement_list(self, ctx:TyCParser.Statement_listContext):
        return self.visitChildren(ctx)


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
        return self.visitChildren(ctx)


    # var_decl_statement : premitive_decl;
    def visitVar_decl_statement(self, ctx:TyCParser.Var_decl_statementContext):
        return self.visitChildren(ctx)


    # premitive_decl : var_type ID (ASSIGN_OP expression)?;
    def visitPremitive_decl(self, ctx:TyCParser.Premitive_declContext):
        return self.visitChildren(ctx)


    # var_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | AUTO_KEYWORD | ID;
    def visitVar_type(self, ctx:TyCParser.Var_typeContext):
        return self.visitChildren(ctx)


    # block_statement : LB_SEP statement_list? RB_SEP;
    def visitBlock_statement(self, ctx:TyCParser.Block_statementContext):
        return self.visitChildren(ctx)


    # if_statement : IF_KEYWORD LP_SEP expression RP_SEP statement (ELSE_KEYWORD statement)?;
    def visitIf_statement(self, ctx:TyCParser.If_statementContext):
        return self.visitChildren(ctx)


    # while_statement : WHILE_KEYWORD LP_SEP expression RP_SEP statement;
    def visitWhile_statement(self, ctx:TyCParser.While_statementContext):
        return self.visitChildren(ctx)


    # for_statement : FOR_KEYWORD LP_SEP for_init? SM_SEP for_condition? SM_SEP for_update? RP_SEP statement;
    def visitFor_statement(self, ctx:TyCParser.For_statementContext):
        return self.visitChildren(ctx)


    # for_init : var_decl_statement | assign_expression;
    def visitFor_init(self, ctx:TyCParser.For_initContext):
        return self.visitChildren(ctx)


    # for_condition : expression;
    def visitFor_condition(self, ctx:TyCParser.For_conditionContext):
        return self.visitChildren(ctx)


    # for_update : assign_expression | pre_post_update;
    def visitFor_update(self, ctx:TyCParser.For_updateContext):
        return self.visitChildren(ctx)


    # switch_statement : SWITCH_KEYWORD LP_SEP expression RP_SEP LB_SEP case_list? default_switch? case_list? RB_SEP;
    def visitSwitch_statement(self, ctx:TyCParser.Switch_statementContext):
        return self.visitChildren(ctx)


    # case_list : case case_list | case;
    def visitCase_list(self, ctx:TyCParser.Case_listContext):
        return self.visitChildren(ctx)


    # case : CASE_KEYWORD expression COLON_SEP statement_list?;
    def visitCase(self, ctx:TyCParser.CaseContext):
        return self.visitChildren(ctx)


    # default_switch : DEFAULT_KEYWORD COLON_SEP statement_list?; 
    def visitDefault_switch(self, ctx:TyCParser.Default_switchContext):
        return self.visitChildren(ctx)


    # break_statement : BREAK_KEYWORD;
    def visitBreak_statement(self, ctx:TyCParser.Break_statementContext):
        return self.visitChildren(ctx)


    # continue_statement : CONTINUE_KEYWORD;
    def visitContinue_statement(self, ctx:TyCParser.Continue_statementContext):
        return self.visitChildren(ctx)


    # return_statement : RETURN_KEYWORD expression?;
    def visitReturn_statement(self, ctx:TyCParser.Return_statementContext):
        return self.visitChildren(ctx)


    # expression_statement : expression;
    def visitExpression_statement(self, ctx:TyCParser.Expression_statementContext):
        return self.visitChildren(ctx)
