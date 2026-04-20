grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}
// ================================= TyC Program Structure =============================//

program : (struct_decl | function_decl)* EOF;

struct_decl : STRUCT_KEYWORD ID LB_SEP member_list? RB_SEP SM_SEP;
member_list : member member_list | member;
member : member_type ID SM_SEP;
member_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | ID;

function_decl : function_ret_type? ID LP_SEP param_list? RP_SEP LB_SEP statement_list? RB_SEP;
function_ret_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | ID | VOID_KEYWORD;
param_list : param CM_SEP param_list | param;
param : param_type ID;
param_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | ID;

// =====================================================================================//

// ================================= Lexical Structure =================================//
// --- LEXER --- //
fragment DIGIT : [0-9];
fragment ALPHABET : [a-zA-Z];

// --- Comment ---//
fragment LINE_COMMENT : '//' ~[\r\n]*;
fragment BLOCK_COMMENT : '/*' .*? '*/';
COMMENT : (LINE_COMMENT | BLOCK_COMMENT) -> skip;

// --- Keywords --- //
AUTO_KEYWORD : 'auto';
BREAK_KEYWORD : 'break';
CASE_KEYWORD : 'case';
CONTINUE_KEYWORD : 'continue';
DEFAULT_KEYWORD : 'default';
ELSE_KEYWORD : 'else';
FLOAT_KEYWORD : 'float';
FOR_KEYWORD : 'for';
IF_KEYWORD : 'if';
INT_KEYWORD : 'int';
RETURN_KEYWORD : 'return';
STRING_KEYWORD : 'string';
STRUCT_KEYWORD : 'struct';
SWITCH_KEYWORD : 'switch';
VOID_KEYWORD : 'void';
WHILE_KEYWORD : 'while';

// --- Identifier --- //

// --- Seperator --- //
LB_SEP : '{';
RB_SEP : '}';
LP_SEP : '(';
RP_SEP : ')';
SM_SEP : ';';
CM_SEP : ',';
COLON_SEP : ':';

// --- Operator --- //
ADD_OP : '+';
SUB_OP : '-';
MUL_OP : '*';
DIV_OP : '/';
MOD_OP : '%';
EQ_OP : '==';
NEQ_OP : '!=';
LT_OP : '<';
GT_OP : '>';
LTE_OP : '<=';
GTE_OP : '>=';
LOGIC_OR_OP : '||';
LOGIC_AND_OP : '&&';
LOGIC_NOT_OP : '!';
INC_OP : '++';
DEC_OP : '--';
ASSIGN_OP : '=';
MEM_ACCESS_OP : '.';

// --- Literal --- //
INT_LIT : DIGIT+;

ID : ('_' | ALPHABET) ('_' | ALPHABET | DIGIT)*;

fragment FLOAT_LIT_1 : '.' DIGIT+ ([Ee] [+-]? DIGIT+)?;
fragment FLOAT_LIT_2 : DIGIT+ (('.' DIGIT*) | ([Ee] [+-]? DIGIT+) | (('.' DIGIT*) ([Ee] [+-]? DIGIT+)));
FLOAT_LIT : FLOAT_LIT_1 | FLOAT_LIT_2;

fragment STR_VALID_CHAR : '\\' [bfrnt"\\] | ~[\r\n"\\];
fragment STR_INVALID_CHAR : '\\' ~[bfnrt"\\\r\n];
STR_LIT : '"' STR_VALID_CHAR* '"' {self.text = self.text[1:-1]};

WS : [ \t\r\n\f]+ -> skip ; // skip spaces, tabs

ERROR_CHAR: .;

ILLEGAL_ESCAPE: '"' STR_VALID_CHAR* STR_INVALID_CHAR {
    raise IllegalEscape(self.text[1:])
};

UNCLOSE_STRING: '"' STR_VALID_CHAR* '\\'? ('\n' | '\r\n' | EOF) {
    if len(self.text) >= 3:
        if self.text[-1] == '\n':
            if self.text[-2] == '\r':
                raise UncloseString(self.text[1:-2])
            else:
                raise UncloseString(self.text[1:-1])
        else:
            raise UncloseString(self.text[1:])
    else:
        if self.text[-1] == '\n':
            raise UncloseString(self.text[1:-1])
        else:
            raise UncloseString(self.text[1:])
};

// =====================================================================================//

// ================================= Type System =============================//

// TODO : BTL2


// ===========================================================================//

// ================================= Expression ==============================//
list_expression : expression CM_SEP list_expression | expression;

expression : expression1 ASSIGN_OP expression | expression1;
expression1 : expression1 LOGIC_OR_OP expression2 | expression2;
expression2 : expression2 LOGIC_AND_OP expression3 | expression3;
expression3 : expression3 (EQ_OP | NEQ_OP) expression4 | expression4;
expression4 : expression4 (LT_OP | LTE_OP | GT_OP | GTE_OP) expression5 | expression5;
expression5 : expression5 (ADD_OP | SUB_OP) expression6 | expression6;
expression6 : expression6 (MUL_OP | DIV_OP | MOD_OP) expression7 | expression7;
expression7 : (LOGIC_NOT_OP | ADD_OP | SUB_OP) expression7 | expression8;
expression8 : (INC_OP | DEC_OP) expression8 | expression9;
expression9 : expression9 (INC_OP | DEC_OP) | expression10 | call_function;
expression10 : struct_mem_id | expression11;
expression11 : INT_LIT | FLOAT_LIT | STR_LIT | ID | LP_SEP expression RP_SEP | LB_SEP list_expression? RB_SEP;

pre_post_update : (INC_OP | DEC_OP) pre_post_update | pre_post_update (INC_OP | DEC_OP) | (INC_OP | DEC_OP) expression10 | expression10 (INC_OP | DEC_OP);

call_function: call_function ID LP_SEP list_expression? RP_SEP | ID LP_SEP list_expression? RP_SEP;
struct_mem_id : struct_mem_id MEM_ACCESS_OP ID | (call_function | expression11) MEM_ACCESS_OP ID;
assign_expression : (struct_mem_id | ID) ASSIGN_OP expression;

// ===========================================================================//

//=================================Statements=================================//
statement_list : statement statement_list | statement;
statement : var_decl_statement SM_SEP
        | block_statement
        | if_statement
        | while_statement
        | for_statement
        | switch_statement
        | break_statement SM_SEP
        | continue_statement SM_SEP
        | return_statement SM_SEP
        | expression_statement SM_SEP;

var_decl_statement : premitive_decl;
premitive_decl : var_type ID (ASSIGN_OP expression)?;
var_type : INT_KEYWORD | FLOAT_KEYWORD | STRING_KEYWORD | AUTO_KEYWORD | ID;
block_statement : LB_SEP statement_list? RB_SEP;
if_statement : IF_KEYWORD LP_SEP expression RP_SEP statement (ELSE_KEYWORD statement)?;
while_statement : WHILE_KEYWORD LP_SEP expression RP_SEP statement;

for_statement : FOR_KEYWORD LP_SEP for_init? SM_SEP for_condition? SM_SEP for_update? RP_SEP statement;
for_init : var_decl_statement | assign_expression;
for_condition : expression;
for_update : assign_expression | pre_post_update;

switch_statement : SWITCH_KEYWORD LP_SEP expression RP_SEP LB_SEP case_list? default_switch? case_list? RB_SEP;
case_list : case case_list | case;
case : CASE_KEYWORD expression COLON_SEP statement_list?;
default_switch : DEFAULT_KEYWORD COLON_SEP statement_list?; 
break_statement : BREAK_KEYWORD;
continue_statement : CONTINUE_KEYWORD;
return_statement : RETURN_KEYWORD expression?;
expression_statement : expression;
//============================================================================//