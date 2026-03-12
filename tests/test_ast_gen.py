"""
AST Generation test cases for TyC compiler.
TODO: Implement 100 test cases for AST generation
"""

import pytest
from tests.utils import ASTGenerator
from src.utils.nodes import *

"""
def test_ast_gen_placeholder():
    source = "void main() {}"
    # TODO: Add actual test assertions
    # Example:
    expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    assert str(ASTGenerator(source).generate()) == expected
    assert True
"""

def test_001():
    input = "void main() {}"
    expect = "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"
    assert str(ASTGenerator(input).generate()) == expect

def test_002():
    input = """
void main() {
    3 + 3;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(BinaryOp(IntLiteral(3), +, IntLiteral(3)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_003():
    input = """
    struct testStruct {};
"""
    expect = "Program([" \
        "StructDecl(" \
            "testStruct, " \
            "[]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_004():
    input = """
    struct testStruct {
        int x;
    };
"""
    expect = "Program([" \
        "StructDecl(" \
            "testStruct, " \
            "[MemberDecl(IntType(), x)]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_005():
    input = """
    struct Vector2 {
        float x;
        float y;
    };
"""
    expect = "Program([" \
        "StructDecl(" \
            "Vector2, " \
            "[MemberDecl(FloatType(), x), MemberDecl(FloatType(), y)]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_006():
    input = """
    int fibo(int n) {
        if (n <= 1) return n;
        return fibo(n - 1) + fibo(n - 2);
    }
"""

    expect = "Program([" \
        "FuncDecl(" \
            "IntType(), " \
            "fibo, " \
            "[Param(IntType(), n)], " \
            "BlockStmt([" \
                "IfStmt(if BinaryOp(Identifier(n), <=, IntLiteral(1)) then ReturnStmt(return Identifier(n))), " \
                "ReturnStmt(return BinaryOp(" \
                    "FuncCall(fibo, [BinaryOp(Identifier(n), -, IntLiteral(1))]), " \
                    "+, " \
                    "FuncCall(fibo, [BinaryOp(Identifier(n), -, IntLiteral(2))])" \
                "))" \
            "])" \
        ")" \
    "])"

    print(str(ASTGenerator(input).generate()))

    print(expect)

    assert str(ASTGenerator(input).generate()) == expect

def test_007():
    input = """
void main() {
    int x = 3 + 3 * 2;
}
"""
    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([" \
                "VarDecl(" \
                    "IntType(), " \
                    "x = " \
                    "BinaryOp(" \
                        "IntLiteral(3), " \
                        "+, " \
                        "BinaryOp(" \
                            "IntLiteral(3), " \
                            "*, " \
                            "IntLiteral(2)" \
                        ")" \
                    ")" \
                ")" \
            "])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_008():
    input = """
void main() {
    int x;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([VarDecl(IntType(), x)])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_009():
    input = """
float foo() {
    return 1;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "FloatType(), " \
            "foo, " \
            "[], " \
            "BlockStmt([ReturnStmt(return IntLiteral(1))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_010():
    input = """
float foo() {
    return 1;
}

void main() {
    foo();
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "FloatType(), " \
            "foo, " \
            "[], " \
            "BlockStmt([ReturnStmt(return IntLiteral(1))])" \
        "), " \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FuncCall(" \
                "foo, " \
                "[]" \
            "))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

# Test listerals
def test_011():
    input = """
void main() {
    36;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(IntLiteral(36))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_012():
    input = """
void main() {
    -36;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PrefixOp(-IntLiteral(36)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_013():
    input = """
void main() {
    3           6;
}
"""

    expect = "AST Generation Error: Error on line 3 col 16: 6"

    assert str(ASTGenerator(input).generate()) == expect

def test_014():
    input = """
void main() {
    -   36;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PrefixOp(-IntLiteral(36)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_015():
    input = """
void main() {
    -
            36;
}
"""
    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PrefixOp(-IntLiteral(36)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_016():
    input = """
void main() {
    ++3; // invalid in C
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PrefixOp(++IntLiteral(3)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_017():
    input = """
void main() {
    --3; // invalid in C
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PrefixOp(--IntLiteral(3)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_018():
    input = """
void main() {
    +3;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PrefixOp(+IntLiteral(3)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_019():
    input = """
void main() {
    -3;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PrefixOp(-IntLiteral(3)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_020():
    input = """
void main() {
    !3; // invalid in C
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PrefixOp(!IntLiteral(3)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_021():
    input = """
void main() {
    36++; // invalid in C
}
"""
    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PostfixOp(IntLiteral(36)++))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_022():
    input = """
void main() {
    36  ++; // invalid in C
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PostfixOp(IntLiteral(36)++))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_023():
    input = """
void main() {
    36
            ++; // invalid in C
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PostfixOp(IntLiteral(36)++))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_024():
    input = """
void main() {
    36--; // invalid in C
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PostfixOp(IntLiteral(36)--))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_025():
    input = """
    void main() {
        036;
    }
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(IntLiteral(36))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_026():
    input = """
    void main() {
        00000000000003;
    }
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(IntLiteral(3))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_027():
    input = """
void main() {
    3.6;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(3.6))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_028():
    input = """
void main() {
    03.6;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(3.6))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_029():
    input = """
void main() {
    3.6e24;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(3.6e+24))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_030():
    input = """
void main() {
    3.6e+24;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(3.6e+24))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_031():
    input =  """
void main() {
    3.6e-24;
}
"""
    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(3.6e-24))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_031():
    input = """
void main() {
    // AnTruong HCMUT
    .36;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(0.36))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_032():
    input = """
void main() {
    -.36;
}
"""
    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(PrefixOp(-FloatLiteral(0.36)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_033():
    input = """
void main() {
    36.;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(36.0))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_034():
    input = """
void main() {
    .36e36;
}
"""
    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(3.6e+35))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_035():
    input = """
void main() {
    .36+36;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([" \
                "ExprStmt(BinaryOp(FloatLiteral(0.36), +, IntLiteral(36)))" \
            "])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_036():
    input = """
void main() {
    .36e-36;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(3.6e-37))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_037():
    input = """
void main() {
    .;
}
"""

    expect = "AST Generation Error: Error on line 3 col 4: ."

    assert str(ASTGenerator(input).generate()) == expect

def test_038():
    input = """
void main() {
    3.e6;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(3000000.0))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_039():
    input = """
void main() {
    .3e6;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FloatLiteral(300000.0))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_040():
    input = """
void main() {
    .e36;
}
"""

    expect = "AST Generation Error: Error on line 3 col 4: ."
    
    assert str(ASTGenerator(input).generate()) == expect

def test_041():
    input = """
void main() {
    .e-36;
}
"""

    expect = "AST Generation Error: Error on line 3 col 4: ."

    assert str(ASTGenerator(input).generate()) == expect

def test_042():
    input = """
void main() {
    3.e;
}
"""

    expect = "AST Generation Error: Error on line 3 col 6: e"

    assert str(ASTGenerator(input).generate()) == expect

def test_043():
    input = """
void main() {
    3.6e*3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 7: e"

    assert str(ASTGenerator(input).generate()) == expect

def test_044():
    input = """
void main() {
    3.6ee3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 7: ee3"

    assert str(ASTGenerator(input).generate()) == expect

def test_045():
    input = """
void main() {
    "Hello, World!";
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(StringLiteral('Hello, World!'))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_046():
    input = """
void main() {
    "Hello, World! \\n\\r\\n An Truong 2004";
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(StringLiteral('Hello, World! \\\\n\\\\r\\\\n An Truong 2004'))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_047():
    input = """
void main() {
    "Hello,
        World!"
}
"""

    expect = "AST Generation Error: Unclosed String: Hello,"

    assert str(ASTGenerator(input).generate()) == expect

def test_048():
    input = """
void main() {
    ++++    3;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([" \
                "ExprStmt(PrefixOp(++PrefixOp(++IntLiteral(3))))" \
            "])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_049():
    input = """
void main() {
    (++(++(+
                a)));
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([" \
                "ExprStmt(" \
                    "PrefixOp(" \
                        "++PrefixOp(" \
                            "++PrefixOp(" \
                                "+Identifier(a)" \
                            ")" \
                        ")" \
                    ")" \
                ")" \
            "])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_050():
    input = """
void main() {
    !!+!!-!!-3;
}
"""

    expect = "Program" \
    "([" \
        "FuncDecl" \
        "(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt" \
            "([" \
                "ExprStmt" \
                "(" \
                    "PrefixOp" \
                    "(" \
                        "!PrefixOp" \
                        "(" \
                            "!PrefixOp" \
                            "(" \
                                "+PrefixOp" \
                                "(" \
                                    "!PrefixOp" \
                                    "(" \
                                        "!PrefixOp" \
                                        "(" \
                                            "-PrefixOp" \
                                            "(" \
                                                "!PrefixOp" \
                                                "(" \
                                                    "!PrefixOp" \
                                                    "(" \
                                                        "-IntLiteral(3)" \
                                                    ")" \
                                                ")" \
                                            ")" \
                                        ")" \
                                    ")" \
                                ")" \
                            ")" \
                        ")" \
                    ")" \
                ")" \
            "])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_051():
    input = """
void main() {
    *+3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 4: *"

    assert str(ASTGenerator(input).generate()) == expect

def test_052():
    input = """
void main() {
    36      ++--;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([" \
                "ExprStmt(PostfixOp(PostfixOp(IntLiteral(36)++)--))" \
            "])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_053():
    input = """
void main() {
    36!++;
}
"""

    expect = "AST Generation Error: Error on line 3 col 6: !"

    assert str(ASTGenerator(input).generate()) == expect


def test_054():
    input = """    
void main() {
    a = 5; // just test
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(AssignExpr(Identifier(a) = IntLiteral(5)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_055():
    input = """
void main() {
    a = (b = 3) + 5;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "[ExprStmt(AssignExpr(" \
                "Identifier(a) = " \
                "BinaryOp(" \
                    "AssignExpr(Identifier(b) = IntLiteral(3)), " \
                    "+, " \
                    "IntLiteral(5)" \
                ")" \
            ")]" \
        ")" \
    "])"

    str(ASTGenerator(input).generate()) == expect

def test_056():
    input = """
void main() {
    a = ;
}
"""

    expect = "AST Generation Error: Error on line 3 col 8: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_057():
    input = """
void main() {
    invalidExpr = **a;
}
"""

    expect = "AST Generation Error: Error on line 3 col 18: *"

    assert str(ASTGenerator(input).generate())

def test_058():
    input = """
void main() {
    a.b;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(MemberAccess(Identifier(a).b))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_059():
    input = """
void main() {
    36.ab; // is valid ?????
}
"""

    expect = "AST Generation Error: Error on line 3 col 7: ab"

    assert str(ASTGenerator(input).generate()) == expect

def test_060():
    input = """
void main() {
    {1,2}.x;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(" \
                "MemberAccess(StructLiteral({IntLiteral(1), IntLiteral(2)}).x)" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_061():
    input = """
void main() {
    a.;
}
"""

    expect = "AST Generation Error: Error on line 3 col 6: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_062():
    input = """
void main() {
    .a;
}
"""

    expect = "AST Generation Error: Error on line 3 col 4: ."

    assert str(ASTGenerator(input).generate()) == expect

def test_063():
    input = """
void main() {
    .;
}
"""

    expect = "AST Generation Error: Error on line 3 col 4: ."

    assert str(ASTGenerator(input).generate()) == expect

def test_064():
    input = """
void main() {
    a.36;
}
"""

    expect = "AST Generation Error: Error on line 3 col 5: .36"

    assert str(ASTGenerator(input).generate()) == expect

def test_065():
    input = """
void main() {
    foo().x;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(" \
                "MemberAccess(FuncCall(foo, []).x)" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_066():
    input = """
void main() {
    x.foo();
}
"""

    expect = "AST Generation Error: Error on line 3 col 9: ("

    assert str(ASTGenerator(input).generate()) == expect

def test_067():
    input = """
void main() {
    foo();
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(" \
                "FuncCall(foo, [])" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_068():
    input = """
void main() {
    fibo(5);
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(" \
                "FuncCall(fibo, [IntLiteral(5)])" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_069():
    input = """
void main() {
    foo("AnTruong",2.4,12);
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(FuncCall(foo, [StringLiteral('AnTruong'), FloatLiteral(2.4), IntLiteral(12)]))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_070():
    input = """
void main() {
    foo(;
}
"""

    expect = "AST Generation Error: Error on line 3 col 8: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_071():
    input = """
void main() {
    foo);
}
"""

    expect = "AST Generation Error: Error on line 3 col 7: )"

    assert str(ASTGenerator(input).generate()) == expect


def test_072():
    input = """
void main() {
    ();
}
"""

    expect = "AST Generation Error: Error on line 3 col 5: )"

    assert str(ASTGenerator(input).generate()) == expect

def test_073():
    input = """
void main() {
    {1,2};
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(StructLiteral({IntLiteral(1), IntLiteral(2)}))])" \
        ")" \
    "])"
    
    assert str(ASTGenerator(input).generate()) == expect

def test_074():
    input = """
void main() {
    x.{1,2};
}
"""


    expect = "AST Generation Error: Error on line 3 col 6: {"

    assert str(ASTGenerator(input).generate()) == expect

def test_075():
    input = """
void main() {
    {,};
}
"""

    expect = "AST Generation Error: Error on line 3 col 5: ,"

    assert str(ASTGenerator(input).generate()) == expect

def test_076():
    input = """
void main() {
    {1+2,3+4};
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ExprStmt(" \
                "StructLiteral({" \
                    "BinaryOp(IntLiteral(1), +, IntLiteral(2)), " \
                    "BinaryOp(IntLiteral(3), +, IntLiteral(4))" \
                "})" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_077():
    input = """
void main() {
    {
        3 + 2;
    }
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([BlockStmt([" \
                "ExprStmt(BinaryOp(IntLiteral(3), +, IntLiteral(2)))" \
            "])])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_078():
    input = """
void main() {
    {
        int a = 3;
        foo();
        if (a < 5) foo();
    }
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([" \
                "BlockStmt(" \
                "[" \
                    "VarDecl(IntType(), a = IntLiteral(3)), " \
                    "ExprStmt(FuncCall(foo, [])), " \
                    "IfStmt(if BinaryOp(Identifier(a), <, IntLiteral(5)) then ExprStmt(FuncCall(foo, [])))" \
                "])" \
            "])" \
        ")" \
    "])"

    print(str(ASTGenerator(input).generate()))

    print(expect)

    assert str(ASTGenerator(input).generate()) == expect

def test_079():
    input = """
void main() {
    {
        int a = 3;
        {
            float b = 5.0;
            float c = a + b;
            foo(a,b,c);
            {
                string s = "Hello, World!";
            }
        }
    }
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([BlockStmt([" \
                "VarDecl(IntType(), a = IntLiteral(3)), " \
                "BlockStmt([" \
                    "VarDecl(FloatType(), b = FloatLiteral(5.0)), " \
                    "VarDecl(FloatType(), c = BinaryOp(Identifier(a), +, Identifier(b))), " \
                    "ExprStmt(FuncCall(foo, [Identifier(a), Identifier(b), Identifier(c)])), " \
                    "BlockStmt([" \
                        "VarDecl(StringType(), s = StringLiteral('Hello, World!'))" \
                    "])" \
                "])" \
            "])])" \
        ")" \
    "])"

    print(str(ASTGenerator(input).generate()))

    print(expect)

    assert str(ASTGenerator(input).generate()) == expect

def test_080():
    input = """
void main() {
    {}
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([BlockStmt([])])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_081():
    input = """
void main() {
    {int a; foo();
}
"""

    expect = "AST Generation Error: Error on line 5 col 0: <EOF>"

    assert str(ASTGenerator(input).generate()) == expect

def test_082():
    input = """
void main() {
    int a; foo();}
}    
"""

    expect = "AST Generation Error: Error on line 4 col 0: }"

    assert str(ASTGenerator(input).generate()) == expect


def test_083():
    input = """
void main() {
    int a;
    int b = foo();
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([" \
                "VarDecl(IntType(), a), " \
                "VarDecl(IntType(), b = FuncCall(foo, []))" \
            "])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_084():
    input = """
void main() {
    float a;
    float b = foo();
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([" \
                "VarDecl(FloatType(), a), " \
                "VarDecl(FloatType(), b = FuncCall(foo, []))" \
            "])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_085():
    input = """
void main() {
    = a;
}
"""

    expect = "AST Generation Error: Error on line 3 col 4: ="

    assert str(ASTGenerator(input).generate()) == expect

def test_086():
    input = """
void main() {
    string s;
    string ss = "AnTruong";
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([" \
                "VarDecl(StringType(), s), " \
                "VarDecl(StringType(), ss = StringLiteral('AnTruong'))" \
            "])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_087():
    input = """
void main() {
    Vector2 v2 = {3,6};
}
"""
    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([VarDecl(StructType(Vector2), v2 = StructLiteral({IntLiteral(3), IntLiteral(6)}))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_088():
    input = """
void main() {
    int a = ;
}
"""

    expect = "AST Generation Error: Error on line 3 col 12: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_089():
    input = """
void main() {
    int = 3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 8: ="

    assert str(ASTGenerator(input).generate()) == expect

def test_090():
    input = """
void main() {
    int = ;
}
"""

    expect = "AST Generation Error: Error on line 3 col 8: ="

    assert str(ASTGenerator(input).generate()) == expect

def test_091():
    input = """
void main() {
    int;
}
"""

    expect = "AST Generation Error: Error on line 3 col 7: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_092():
    input = """
void main() {
    if (a == 1)         a = 2;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([IfStmt(" \
                "if BinaryOp(Identifier(a), ==, IntLiteral(1)) then ExprStmt(AssignExpr(Identifier(a) = IntLiteral(2)))" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_093():
    input = """
void main() {
    if (a == 1) a = 2; else a = 3;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([IfStmt(" \
                "if BinaryOp(Identifier(a), ==, IntLiteral(1)) then ExprStmt(AssignExpr(Identifier(a) = IntLiteral(2))), else ExprStmt(AssignExpr(Identifier(a) = IntLiteral(3)))" \
            ")])" \
        ")" \
    "])"

    print(str(ASTGenerator(input).generate())) == expect

    print(expect)

    assert str(ASTGenerator(input).generate()) == expect

def test_094():
    input = """
void main() {
    else a = 3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 4: else"

    assert str(ASTGenerator(input).generate()) == expect

def test_095():
    input = """
void main() {
    if (a == 1) a = 2; else ;
}
"""

    expect = "AST Generation Error: Error on line 3 col 28: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_096():
    input = """
void main() {
    if (a == 1) a = 2
    else a = 3;
}
"""

    expect = "AST Generation Error: Error on line 4 col 4: else"

    assert str(ASTGenerator(input).generate()) == expect

def test_097():
    input = """
void main() {
    if a == 1 a = 2;
}
"""

    expect = "AST Generation Error: Error on line 3 col 7: a"

    assert str(ASTGenerator(input).generate()) == expect

def test_098():
    input = """
void main() {
    if (a == 1);
}
"""

    expect = "AST Generation Error: Error on line 3 col 15: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_099():
    input = """
void main() {
    if;
}
"""

    expect = "AST Generation Error: Error on line 3 col 6: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_100():
    input = """
void main() {
    if (a == 1)
        if (a == 2)
            a = 3;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([IfStmt(" \
                "if BinaryOp(Identifier(a), ==, IntLiteral(1)) then " \
                    "IfStmt(if BinaryOp(Identifier(a), ==, IntLiteral(2)) then " \
                        "ExprStmt(AssignExpr(Identifier(a) = IntLiteral(3)))" \
                    ")" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_101():
    input = """
void main() {
    if (a == 1) else a = 2;
}
"""

    expect = "AST Generation Error: Error on line 3 col 16: else"

    assert str(ASTGenerator(input).generate()) == expect

def test_102():
    input = """
void main() {
    if (a == 1) a = 2 else;
}
"""

    expect = "AST Generation Error: Error on line 3 col 22: else"

    assert str(ASTGenerator(input).generate()) == expect

def test_103():
    input = """
void main() {
    if () a = 1;
}
"""

    expect = "AST Generation Error: Error on line 3 col 8: )"

    assert str(ASTGenerator(input).generate()) == expect

def test_104():
    input = """
void main() {
    if (int a = 3) a = 3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 8: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_105():
    input = """
void main() {
    int a = (int a = 3);
}
"""

    expect = "AST Generation Error: Error on line 3 col 13: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_106():
    input = """
void main() {
    if (a == 1) int foo() {
        return 1;
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 23: ("

    assert str(ASTGenerator(input).generate()) == expect

def test_107():
    input = """
void main() {
    if (a == 1) {
        foo();
        int b = 3;
    }
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([IfStmt(" \
                "if BinaryOp(Identifier(a), ==, IntLiteral(1)) then BlockStmt([" \
                    "ExprStmt(FuncCall(foo, [])), " \
                    "VarDecl(IntType(), b = IntLiteral(3))" \
                "])" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_108():
    input = """
void main() {
    if (a == 1) a = 1; else {}
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([IfStmt(" \
                "if BinaryOp(Identifier(a), ==, IntLiteral(1)) then ExprStmt(AssignExpr(Identifier(a) = IntLiteral(1))), else BlockStmt([])" \
            ")])" \
        ")" \
    "])"

    print(str(ASTGenerator(input).generate()))

    print(expect)

    assert str(ASTGenerator(input).generate()) == expect

def test_109():
    input = """
void main() {
    IF (a == 1) a = 1;
}
"""

    expect = "AST Generation Error: Error on line 3 col 18: ="

    assert str(ASTGenerator(input).generate()) == expect

def test_110():
    input = """
void main() {
    if (a == 1) a = 1 ELSE a = 2;
}
"""

    expect = "AST Generation Error: Error on line 3 col 22: ELSE"

    assert str(ASTGenerator(input).generate()) == expect

def test_111():
    input = """
void main() {
    int foo() {
    
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 11: ("

    assert str(ASTGenerator(input).generate()) == expect

def test_112():
    input = """
void main() {
    int a = int b;
}
"""

    expect = "AST Generation Error: Error on line 3 col 12: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_113():
    input = """
void main() {
    int a = int foo() {
        return 1;
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 12: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_114():
    input = """
void main() {
    while (a < 5) a++;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([WhileStmt(while BinaryOp(Identifier(a), <, IntLiteral(5)) do ExprStmt(PostfixOp(Identifier(a)++)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_115():
    input = """
void main() {
    while (a != b) {
        int c = a;
        a = b;
        b = c;
    }
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([WhileStmt(" \
                "while BinaryOp(Identifier(a), !=, Identifier(b)) do BlockStmt([" \
                    "VarDecl(IntType(), c = Identifier(a)), " \
                    "ExprStmt(AssignExpr(Identifier(a) = Identifier(b))), " \
                    "ExprStmt(AssignExpr(Identifier(b) = Identifier(c)))" \
                "])" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_116():
    input = """
void main() {
    while () int a = 3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 11: )"

    assert str(ASTGenerator(input).generate()) == expect

def test_117():
    input = """
void main() {
    while (a == 3);
}
"""

    expect = "AST Generation Error: Error on line 3 col 18: ;"

    assert str(ASTGenerator(input).generate()) == expect


def test_118():
    input = """
void main() {
    while (int a = 3) a = 3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 11: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_119():
    input = """
void main() {
    WHILE (a = 1) b = 2;
}
"""

    expect = "AST Generation Error: Error on line 3 col 20: ="

    assert str(ASTGenerator(input).generate()) == expect

def test_120():
    input = """
void main() {
    while a == 1 b = 2;
}
"""

    expect = "AST Generation Error: Error on line 3 col 10: a"

    assert str(ASTGenerator(input).generate()) == expect

def test_121():
    input = """
void main() {
    while (a == 1 b = 2;
}
"""

    expect = "AST Generation Error: Error on line 3 col 18: b"

    assert str(ASTGenerator(input).generate()) == expect

def test_122():
    input = """
void main() {
    while;
}
"""

    expect = "AST Generation Error: Error on line 3 col 9: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_123():
    input = """
void main() {
    for (int i = 0;i < 10;++i)
        a = a + i;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ForStmt(" \
                "for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PrefixOp(++Identifier(i)) do ExprStmt(AssignExpr(Identifier(a) = BinaryOp(Identifier(a), +, Identifier(i))))" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_124():
    input = """
void main() {
    for (i = 0;i < 10;i++) {
        int b = foo();
        string s = "Hello, World!";
    }
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ForStmt(" \
                "for " \
                    "ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0))); " \
                    "BinaryOp(Identifier(i), <, IntLiteral(10)); " \
                    "PostfixOp(Identifier(i)++) " \
                "do BlockStmt([" \
                    "VarDecl(IntType(), b = FuncCall(foo, [])), " \
                    "VarDecl(StringType(), s = StringLiteral('Hello, World!'))" \
                "])" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_125():
    input = """
void main() {
    for (;;) 
    {
    }
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ForStmt(" \
                "for None; None; None do BlockStmt([])" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_126():
    input = """
void main() {
    for (int i = 0 i < 10 i++) {}
}
"""

    expect = "AST Generation Error: Error on line 3 col 19: i"

    assert str(ASTGenerator(input).generate()) == expect

def test_127():
    input = """
void main() {
    for () int a = 1;
}
"""

    expect = "AST Generation Error: Error on line 3 col 9: )"

    assert str(ASTGenerator(input).generate()) == expect

def test_128():
    input = """
void main() {
    for (int i = 0;int i = 0;int i = 0) {
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 19: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_129():
    input = """
void main() {
    for (foo(); i < 10;++i) {
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 14: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_130():
    input = """
void main() {
    for (if (a == 0) a = 1;; i < 10;++i) {
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 9: if"

    assert str(ASTGenerator(input).generate()) == expect

def test_131():
    input = """
void main() {
    for (int i = 0; return 36;; ++i) {
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 20: return"

    assert str(ASTGenerator(input).generate()) == expect

def test_132():
    input = """
void main() {
    for (int i = 0;i < 36;foo()) {
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 31: )"

    assert str(ASTGenerator(input).generate()) == expect

def test_133():
    input = """
void main() {
    for (int i = 0;i < 36;return 36;) {
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 26: return"

    assert str(ASTGenerator(input).generate()) == expect

def test_134():
    input = """
void main() {
    for (int i = 0;i < 36;3 + 6) {
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 28: +"

    assert str(ASTGenerator(input).generate()) == expect

def test_135():
    input = """
void main() {
    for (int i = 0;i < 36;++i);
}
"""

    expect = "AST Generation Error: Error on line 3 col 30: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_136():
    input = """
void main() {
    for int i = 0;i < 36;++i {}
}
"""

    expect = "AST Generation Error: Error on line 3 col 8: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_137():
    input = """
void main() {
    FOR (int i = 0;i < 36;++i) i = 1;
}
"""

    expect = "AST Generation Error: Error on line 3 col 9: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_138():
    input = """
void main() {
    switch (a) {
        case 1:
            print(a);
            break;
        case 2:
            print(a);
            break;
        default:
            break;
    } 
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([SwitchStmt(" \
                "switch Identifier(a) cases [" \
                    "CaseStmt(case IntLiteral(1): [" \
                        "ExprStmt(FuncCall(print, [Identifier(a)])), " \
                        "BreakStmt()" \
                    "]), " \
                    "CaseStmt(case IntLiteral(2): [" \
                        "ExprStmt(FuncCall(print, [Identifier(a)])), " \
                        "BreakStmt()" \
                    "])" \
                "], default DefaultStmt(default: [BreakStmt()])" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_139():
    input = """
void main() {
    switch () {
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 12: )"

    assert str(ASTGenerator(input).generate()) == expect

def test_140():
    input = """
void main() {
    switch (a) int a = 0;
}
"""

    expect = "AST Generation Error: Error on line 3 col 15: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_141():
    input = """
void main() {
    switch (a) {
    }
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([SwitchStmt(" \
                "switch Identifier(a) cases []" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_142():
    input = """
void main() {
    switch (int a = 0) {
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 12: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_143():
    input = """
void main() {
    switch (1 + 1) {
        case:
            foo();
            break;
    }
}
"""

    expect = "AST Generation Error: Error on line 4 col 12: :"

    assert str(ASTGenerator(input).generate()) == expect

def test_144():
    input = """
void main() {
    switch (1 + 1) {
        case break;:
            foo();
            break;
    }
}
"""

    expect = "AST Generation Error: Error on line 4 col 13: break"

    assert str(ASTGenerator(input).generate()) == expect

def test_145():
    input = """
void main() {
    switch (1 + 1) {
        case 2 foo();
    }
}
"""

    expect = "AST Generation Error: Error on line 4 col 15: foo"

    assert str(ASTGenerator(input).generate()) == expect

def test_146():
    input = """
void main() {
    switch (2 + 2) {
        case;
    }
}
"""

    expect = "AST Generation Error: Error on line 4 col 12: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_147():
    input = """
void main() {
    switch (a);
}
"""

    expect = "AST Generation Error: Error on line 3 col 14: ;"

    assert str(ASTGenerator(input).generate()) == expect

def test_148():
    input = """
void main() {
    switch (a) {
        default int a = 3;:
            break;
    }
}
"""

    expect = "AST Generation Error: Error on line 4 col 16: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_149():
    input = """
void main() {
    switch (a) {
        default break;
    }
}
"""

    expect = "AST Generation Error: Error on line 4 col 16: break"

    assert str(ASTGenerator(input).generate()) == expect

def test_150():
    input = """
void main() {
    switch (a) {
    }
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([SwitchStmt(" \
                "switch Identifier(a) cases []" \
            ")])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_151():
    input = """
void main() {
    switch (a)
        case 3:
}
"""

    expect = "AST Generation Error: Error on line 4 col 8: case"

    assert str(ASTGenerator(input).generate()) == expect

def test_152():
    input = """
void main() {
    switch (a) {
        default:
            break;
        default:
            break;
    }
}
"""

    expect = "AST Generation Error: Error on line 6 col 8: default"

    assert str(ASTGenerator(input).generate()) == expect

def test_153():
    input = """
void main() {
    switch (a) {
        default 5:
    }
}
"""

    expect = "AST Generation Error: Error on line 4 col 16: 5"

    assert str(ASTGenerator(input).generate()) == expect

def test_154():
    input = """
void main() {
    continue;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ContinueStmt()])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_155():
    input = """
void main() {
    continue 3 + 3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 13: 3"

    assert str(ASTGenerator(input).generate()) == expect

def test_156():
    input = """
void main() {
    continue int a = 3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 13: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_157():
    input = """
void main() {
    return;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ReturnStmt(return)])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_158():
    input = """
void main() {
    return 1 + 2;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "BlockStmt([ReturnStmt(return BinaryOp(IntLiteral(1), +, IntLiteral(2)))])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_159():
    input = """
void main() {
    return int a = 3;
}
"""

    expect = "AST Generation Error: Error on line 3 col 11: int"

    assert str(ASTGenerator(input).generate()) == expect

def test_160():
    input = """
struct foo() {
};
"""

    expect = "AST Generation Error: Error on line 2 col 10: ("

    assert str(ASTGenerator(input).generate()) == expect

def test_161():
    input = """
MyStruct foo() {
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "StructType(MyStruct), " \
            "foo, " \
            "[], " \
            "BlockStmt([])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_162():
    input = """
int foo(int a = 3) {
}
"""

    expect = "AST Generation Error: Error on line 2 col 14: ="

    assert str(ASTGenerator(input).generate()) == expect

def test_163():
    input = """
int foo() {
    int foo1() {
    }
}
"""

    expect = "AST Generation Error: Error on line 3 col 12: ("

    assert str(ASTGenerator(input).generate()) == expect

def test_164():
    input = """
int foo() {
    {
        {
        
        }
    }

    {
    }
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "IntType(), " \
            "foo, " \
            "[], " \
            "BlockStmt([BlockStmt([BlockStmt([])]), BlockStmt([])])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_165():
    input = """
int foo {

}
"""

    expect = "AST Generation Error: Error on line 2 col 8: {"

    assert str(ASTGenerator(input).generate()) == expect

def test_166():
    input = """
struct MyStruct {
    int a = 3;
};
"""

    expect = "AST Generation Error: Error on line 3 col 10: ="

    assert str(ASTGenerator(input).generate()) == expect

def test_167():
    input = """
foo() {
    int a = 3;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "auto, " \
            "foo, " \
            "[], " \
            "BlockStmt([" \
                "VarDecl(IntType(), a = IntLiteral(3))" \
            "])" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_168():
    input = """
struct MyStruct() {
};
"""

    expect = "AST Generation Error: Error on line 2 col 15: ("

    assert str(ASTGenerator(input).generate()) == expect

def test_169():
    input = """
struct MyStruct {
    return 1;
};
"""

    expect = "AST Generation Error: Error on line 3 col 4: return"

    assert str(ASTGenerator(input).generate()) == expect

def test_170():
    input = """
void main() {
    int a = return 1;
}
"""

    expect = "AST Generation Error: Error on line 3 col 12: return"

    assert str(ASTGenerator(input).generate()) == expect