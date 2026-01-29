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

// TODO: Define grammar rules here

// Tokens Rules
program: (funcDecl | structDecl)* EOF ;

DIGITS : [0-9]+ ;

BLOCK_CMT : '/*' .*? '*/' -> skip ; // skip block comments
UNCLOSE_BLOCK_COMMENT
  : '/*' ( ~[*] | '*' ~[/] )* EOF
  ;
  
LINE_CMT : '//' ~[\r\n]* -> skip ; // skip line comments

AUTO      : 'auto' ;
BREAK     : 'break' ;
CASE      : 'case' ;
CONTINUE  : 'continue' ;
DEFAULT   : 'default' ;
ELSE      : 'else' ;

FLOAT     : 'float' ;
FOR       : 'for' ;
IF        : 'if' ;
INT       : 'int' ;
RETURN    : 'return' ;
STRING    : 'string' ;
STRUCT    : 'struct' ;

SWITCH    : 'switch' ;
VOID      : 'void' ;
WHILE     : 'while' ;

ID: [a-zA-Z_][a-zA-Z0-9_]* ;

// Arithmetic
INC     : '++' ;
DEC     : '--' ;
PLUS    : '+' ;
MINUS   : '-' ;
MUL     : '*' ;
DIV     : '/' ;
MOD     : '%' ;

// Comparison
EQ      : '==' ;
NEQ     : '!=' ;
LE      : '<=' ;
GE      : '>=' ; 
LT      : '<' ;
GT      : '>' ;

// Logical
OR      : '||' ;
AND     : '&&' ;
NOT     : '!' ;

// Assignment
ASSIGN  : '=' ;

// Member access
DOT     : '.' ;

LBRACK   : '[' ;
RBRACK   : ']' ;
LBRACE   : '{' ;
RBRACE   : '}' ;
LPAREN   : '(' ;
RPAREN   : ')' ;
SEMI     : ';' ;
COMMA    : ',' ;
COLON    : ':' ;

// Int Literal
INT_LIT: DIGITS ;


// Float Literal
fragment EXP: [eE]MINUS?DIGITS;
// better (more standard): [eE] [+\-]? DIGITS

FLOAT_LIT
  : DIGITS '.'                         // 1.
  | DIGITS '.' DIGITS EXP?             // 1.23 or 1.23e4  (requires digits before EXP)
  | '.' DIGITS EXP?                    // .5 or .5e2

  ;

// String Literal
fragment ESC : '\\' [bfnrt"\\] ;
fragment STR_CHAR : ~["\\\r\n] | ESC ;

STRING_LIT
  : '"' STR_CHAR* '"'
  ;

ILLEGAL_ESCAPE
  : '"' (STR_CHAR* '\\' ~[bfnrt"\\]) .*? '"'?   // bad escape after backslash
  ;

UNCLOSE_STRING
  : '"' STR_CHAR* (EOF | '\r' | '\n')
  ;

funcDecl
  : (returnType)? ID LPAREN paramList? RPAREN block
  ;

returnType
  : type
  | VOID
  ;

paramList
  : param (COMMA param)*
  ;

param
  : type ID             // no AUTO here
  ;

type
  : INT
  | FLOAT
  | STRING
  | ID                  // struct type name
  ;

// Struct Declarations rules
structDecl
  : STRUCT ID LBRACE structMemberDecl* RBRACE SEMI
  ;

structMemberDecl
  : type ID SEMI        // no AUTO here
  ;

structInit
  : type ID ASSIGN LBRACE exprList? RBRACE
  ;


// Variable Declaration Rules
  varDecl
  : type ID (ASSIGN expr)? SEMI
  | AUTO ID (ASSIGN expr)? SEMI
  | structInit SEMI
  ;

// Statement Rules
exprStmt
  : expr SEMI
  ;

exprList
  : expr (COMMA expr)*
  ;

// Expression Rules

expr : assignExpr ;

assignExpr
  : logicalOr
  | lvalue ASSIGN assignExpr
  ;

lvalue
  : ID (DOT ID)*
  ;

logicalOr  : logicalAnd (OR logicalAnd)* ;
logicalAnd : equality   (AND equality)* ;
equality   : relational ((EQ | NEQ) relational)* ;
relational : additive   ((LT|LE|GT|GE) additive)* ;
additive   : multiplicative ((PLUS|MINUS) multiplicative)* ;
multiplicative : unary ((MUL|DIV|MOD) unary)* ;

unary
  : (PLUS|MINUS|NOT|INC|DEC) unary
  | postfix
  ;

postfix
  : primary postfixOp*
  ;

primary
  : INT_LIT
  | FLOAT_LIT
  | STRING_LIT
  | ID
  | LPAREN expr RPAREN
  ;

// Postfix Operator Rules
postfixOp
  : LPAREN argList? RPAREN   // function call
  | DOT ID                   // member access
  | INC                      // postfix ++
  | DEC                      // postfix --
  ;
// If Statement Rules
ifStmt
  : IF LPAREN expr RPAREN block (ELSE block)?
  ;

// While Statement Rules
whileStmt
  : WHILE LPAREN expr RPAREN block
  ;

// For Statement Rules
forStmt
  : FOR LPAREN forInit? SEMI forCond? SEMI forUpdate? RPAREN block
  ;

forInit
  : varDeclNoSemi
  | expr
  ;

forCond
  : expr
  ;

forUpdate
  : expr
  ;

varDeclNoSemi
  : type ID (ASSIGN expr)?
  | AUTO ID (ASSIGN expr)?
  | structInitNoSemi
  ;

structInitNoSemi
  : type ID ASSIGN LBRACE exprList? RBRACE
  ;

// Switch Statement Rules
switchStmt
  : SWITCH LPAREN expr RPAREN LBRACE switchSection* RBRACE
  ;

switchSection
  : caseLabel+ stmt*
  ;

caseLabel
  : CASE expr COLON
  | DEFAULT COLON
  ;

// Continue Statement Rules
continueStmt
  : CONTINUE SEMI
  ;

// Break Statement Rules
breakStmt
  : BREAK SEMI
  ;

// Return Statement Rules
returnStmt
  : RETURN expr? SEMI
  ;

// Statement Rules
stmt
  : exprStmt
  | ifStmt
  | whileStmt
  | forStmt
  | switchStmt
  | continueStmt
  | breakStmt
  | returnStmt
  ;

// Code Block Rules
block
  : LBRACE (varDecl | stmt | block)* RBRACE
  ;

argList
  : expr (COMMA expr)*
  ;

// Whitespace
WS : [ \t\r\n\f]+ -> skip ; // skip spaces, tabs

ERROR_CHAR: .;
// ILLEGAL_ESCAPE:.;
// UNCLOSE_STRING:.;
