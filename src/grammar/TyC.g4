grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:
        result = super().emit()
        raise UncloseString(result.text)
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit()
        raise IllegalEscape(result.text)
    elif tk == self.ERROR_CHAR:
        result = super().emit()
        raise ErrorToken(result.text)
    else:
        return super().emit()
}

options{
    language=Python3;
}

/* =========================
 *          PARSER
 * ========================= */

program
    : decl+ EOF
    ;

decl
    : structDecl
    | funcDecl
    ;

structDecl
    : STRUCT ID LBRACE structMember* RBRACE SEMI
    ;

structMember
    : typeSpec ID SEMI
    ;

// return type can be omitted (inferred)【turn5file0†tyc_specification.md†L44-L46】
funcDecl
    : returnType ID LPAREN paramList? RPAREN block
    | ID LPAREN paramList? RPAREN block
    ;

paramList
    : param (COMMA param)*
    ;

// params must have explicit type (not auto)【turn5file0†tyc_specification.md†L55-L56】
param
    : typeSpec ID
    ;

returnType
    : typeSpec
    | VOID
    ;

typeSpec
    : INT
    | FLOAT
    | STRING
    | ID              // struct type name
    ;

block
    : LBRACE blockItem* RBRACE
    ;

blockItem
    : varDeclStmt
    | stmt
    ;

// variable declaration statement (auto or explicit type)【turn5file15†tyc_specification.md†L35-L45】
varDeclStmt
    : AUTO ID (ASSIGN initValue)? SEMI
    | typeSpec ID (ASSIGN initValue)? SEMI
    ;

initValue
    : expr
    | structLiteral
    ;

stmt
    : block
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    ;

ifStmt
    : IF LPAREN expr RPAREN stmt (ELSE stmt)?
    ;

whileStmt
    : WHILE LPAREN expr RPAREN stmt
    ;

// for(init; cond; update) stmt  (cond/update may be empty)
forStmt
    : FOR LPAREN forInit? SEMI expr? SEMI expr? RPAREN stmt
    ;

forInit
    : forVarDecl
    | expr
    ;

// like var decl but without trailing ';'
forVarDecl
    : AUTO ID (ASSIGN initValue)?
    | typeSpec ID (ASSIGN initValue)?
    ;

// switch statement (supports empty body)【turn4file7†tyc_specification.md†L1-L4】
switchStmt
    : SWITCH LPAREN expr RPAREN LBRACE switchSection* defaultSection? RBRACE
    ;

switchSection
    : CASE constExpr COLON stmt*
    ;

defaultSection
    : DEFAULT COLON stmt*
    ;

// spec allows constant expressions like 1+2, (4), +5, -6【turn4file7†tyc_specification.md†L26-L40】
constExpr
    : expr
    ;

breakStmt
    : BREAK SEMI
    ;

continueStmt
    : CONTINUE SEMI
    ;

returnStmt
    : RETURN expr? SEMI
    ;

exprStmt
    : expr SEMI
    ;

/* =========================
 *        EXPRESSIONS
 * precedence & associativity per spec【turn5file3†tyc_specification.md†L42-L59】
 * ========================= */

expr
    : assignExpr
    ;

// right-associative assignment
assignExpr
    : lvalue ASSIGN assignExpr
    | orExpr
    ;

// constrain LHS to identifier / member access chain (no call, no ++/--)
lvalue
    : lvalueAtom (DOT ID)*
    ;

lvalueAtom
    : ID
    | LPAREN expr RPAREN
    ;

orExpr
    : andExpr (OR andExpr)*
    ;

andExpr
    : eqExpr (AND eqExpr)*
    ;

eqExpr
    : relExpr ((EQ | NEQ) relExpr)*
    ;

relExpr
    : addExpr ((LT | LE | GT | GE) addExpr)*
    ;

addExpr
    : mulExpr ((PLUS | MINUS) mulExpr)*
    ;

mulExpr
    : unaryExpr ((MUL | DIV | MOD) unaryExpr)*
    ;

unaryExpr
    : (PLUS | MINUS | NOT | INC | DEC) unaryExpr
    | postfixExpr
    ;

// postfix: primary then any number of (.id) or (args) then optional ++/--
postfixExpr
    : primary ( (DOT ID) | callSuffix )* (INC | DEC)?
    ;

callSuffix
    : LPAREN argList? RPAREN
    ;

argList
    : expr (COMMA expr)*
    ;

primary
    : literal
    | ID
    | LPAREN expr RPAREN
    | structLiteral
    ;

structLiteral
    : LBRACE (expr (COMMA expr)*)? RBRACE
    ;

literal
    : INTLIT
    | FLOATLIT
    | STRINGLIT
    ;

/* =========================
 *          LEXER
 * ========================= */

// keywords【turn5file9†tyc_specification.md†L34-L41】
AUTO: 'auto';
BREAK: 'break';
CASE: 'case';
CONTINUE: 'continue';
DEFAULT: 'default';
ELSE: 'else';
FLOAT: 'float';
FOR: 'for';
IF: 'if';
INT: 'int';
RETURN: 'return';
STRING: 'string';
STRUCT: 'struct';
SWITCH: 'switch';
VOID: 'void';
WHILE: 'while';

// operators & separators【turn5file9†tyc_specification.md†L42-L53】【turn5file1†tyc_specification.md†L5-L8】
INC: '++';
DEC: '--';
LE: '<=';
GE: '>=';
EQ: '==';
NEQ: '!=';
AND: '&&';
OR: '||';

ASSIGN: '=';
DOT: '.';
LT: '<';
GT: '>';
NOT: '!';
PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
MOD: '%';

LBRACE: '{';
RBRACE: '}';
LPAREN: '(';
RPAREN: ')';
SEMI: ';';
COMMA: ',';
COLON: ':';

// identifiers【turn5file2†tyc_specification.md†L80-L83】
ID: [a-zA-Z_] [a-zA-Z0-9_]* ;

// numeric literals
fragment DIGIT: [0-9];
fragment EXP: [eE] [+\-]? DIGIT+;

FLOATLIT
    : DIGIT+ '.' DIGIT* EXP?
    | '.' DIGIT+ EXP?
    | DIGIT+ EXP
    ;

INTLIT
    : DIGIT+
    ;

// comments【turn5file2†tyc_specification.md†L58-L71】
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;

// whitespace (includes formfeed \f)【turn5file2†tyc_specification.md†L54-L55】
WS: [ \t\r\n\f]+ -> skip;

/*
String literal rules:
- valid: strip quotes => token text is content only【turn5file1†tyc_specification.md†L50-L50】
- errors: strip opening quote; ILLEGAL_ESCAPE includes up to illegal escape【turn5file4†tyc_specification.md†L1-L9】
- detection order: ILLEGAL_ESCAPE first, then UNCLOSE_STRING, then STRINGLIT【turn5file4†tyc_specification.md†L5-L9】
*/
fragment ESC_SEQ: '\\' [bfrnt"\\];
fragment STR_CHAR: ~["\\\r\n];

ILLEGAL_ESCAPE
    : '"' (STR_CHAR | ESC_SEQ)* '\\' ~[bfrnt"\\\r\n]
      { self.text = self.text[1:]; }
    ;

UNCLOSE_STRING
    : '"' (STR_CHAR | ESC_SEQ)* ( '\r'? '\n' | EOF )
      {
        txt = self.text[1:]
        if len(txt) > 0 and (txt[-1] == '\n' or txt[-1] == '\r'):
            txt = txt[:-1]
        if len(txt) > 0 and txt[-1] == '\r':
            txt = txt[:-1]
        self.text = txt
      }
    ;

STRINGLIT
    : '"' (STR_CHAR | ESC_SEQ)* '"'
      { self.text = self.text[1:-1]; }
    ;

// must be last
ERROR_CHAR: . ;
