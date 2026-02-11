"""
AST Generation test cases for TyC compiler.
TODO: Implement 100 test cases for AST generation
"""

import pytest
from tests.utils import ASTGenerator

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
    expect = "Program(" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "BlockStmt([" \
                "ExprStmt(" \
                    "BinaryOp(" \
                    "IntLiteral(3), " \
                    "+, " \
                    "IntLiteral(3)" \
                    ")" \
                ")" \
            "])" \
        ")" \
    ")"

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
    }
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
            "[" \
                "IfStmt(if BinaryOp(Identifier(n), IntLiteral(1)) then ReturnStmt(returnIdentifier(n))), " \
                "ReturnStmt(returnBinaryOp(" \
                    "FuncCall(fibo, BinaryOp(Identifier(n), -, IntLiteral(1))), " \
                    "+, " \
                    "FuncCall(fibo, BinaryOp(Identifier(n), -, IntLiteral(2)))" \
                "))))" \
            "]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_007():
    input = """
void main() {
    int x = 3 + 3 * 2;
}
"""
    expect = "Program([" \
        "FuncDecl(" \
            "VoidType()" \
            "main, " \
            "[], " \
            "[VarDecl(" \
                "IntType(), " \
                "x" \
                "BinaryOp(" \
                    "IntLiteral(3), " \
                    "+, " \
                    "BinaryOp(" \
                        "IntLiteral(3), " \
                        "*, " \
                        "IntLiteral(2)" \
                    ")" \
                ")" \
            ")]" \
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
        "VarDecl(IntType(), x)" \
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
            "[ReturnStmt(returnIntLiteral(1))]" \
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
            "[ReturnStmt(returnIntLiteral(1))]" \
        "), " \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "[ExprStmt(FuncCall(" \
                "foo, " \
                "[]" \
            "))]" \
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
            "[ExprStmt(IntLiteral(36))]" \
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
            "[ExprStmt(PrefixOp(-IntLiteral(36)))]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_013():
    input = """
void main() {
    3           6;
}
"""
    # TODO
    print(str(ASTGenerator(input).generate()))
    assert False

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
            "[ExprStmt(PrefixOp(-IntLiteral(36)))]" \
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
            "[ExprStmt(PrefixOp(-IntLiteral(36)))]" \
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
            "[ExprStmt(PrefixOp(++IntLiteral(3)))]" \
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
            "[ExprStmt(PrefixOp(--IntLiteral(3)))]" \
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
            "[ExprStmt(PrefixOp(+IntLiteral(3)))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(PrefixOp(!IntLiteral(3)))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(PostfixOp(IntLiteral(36)++))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(PostfixOp(IntLiteral(36)++))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(PostfixOp(IntLiteral(36)++))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(PostfixOp(IntLiteral(36)++))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(PrefixOp(-IntLiteral(36)))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(PrefixOp(-IntLiteral(3)))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(3.6))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(3.6))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(3.6e24))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(3.6e24))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(3.6e-24))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(0.36))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(PrefixOp(-FloatLiteral(0.36)))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(36.0))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(0.36e36))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(0.36e36))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(0.36e-36))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

def test_037():
    input = """
void main() {
    .;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

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
            "[ExprStmt(FloatLiteral(3.0e6))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

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
            "[ExprStmt(FloatLiteral(0.3e6))]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

def test_040():
    input = """
void main() {
    .e36;
}
"""

    print(str(ASTGenerator(input).generate()))
    
    assert False

def test_041():
    input = """
void main() {
    .e-36;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_042():
    input = """
void main() {
    3.e;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_043():
    input = """
void main() {
    3.6e*3;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_044():
    input = """
void main() {
    3.6ee3;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_045():
    input = """
void main() {
    "Hello, World!",
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "[ExprStmt(StringLiteral(Hello, World!))]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_046():
    input = """
void main() {
    "Hello, World! \\n\\r\\n An Truong 2004"
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "[ExprStmt(StringLiteral(Hello, World! \\n\\r\\n An Truong 2004))]" \
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

    print(str(ASTGenerator(input).generate()))

    assert False

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
            "[ExprStmt(PrefixOp(++PrefixOp(++,IntLiteral(3)))]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_049():
    input = """
void main() {
    +++++
                3;
}
"""

    expect = "Program([" \
        "VoidType(), " \
        "main, " \
        "[], " \
        "[ExprStmt(PrefixOp(" \
            "++PrefixOp(" \
                "++PrefixOp(" \
                    "++PrefixOp(+IntLiteral(3))" \
                ")" \
            ")" \
        "))]" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_050():
    input = """
void main() {
    !!++!!--!!-3;
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "ExprStmt(" \
                "PrefixOp(" \
                    "!PrefixOp(" \
                        "++PrefixOp(" \
                            "!PrefixOp(" \
                                "!PrefixOp(" \
                                    "--PrefixOp(" \
                                        "!PrefixOp(" \
                                            "!PrefixOp(" \
                                                "-PrefixOp(IntLiteral(3))" \
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
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_051():
    input = """
void main() {
    *+3;
}
"""

    print(str(ASTGenerator(input).generate()))

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
            "[ExprStmt(" \
                "Postfix(" \
                    "Postfix(36++)--" \
                ")" \
            ")]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_052():
    input = """
void main() {
    36!++;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_053():
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
            "[ExprStmt(AssignExpr(Identifier(a), IntLiteral(5)))]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_054():
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
                "Identifier(a), " \
                "BinaryOp(" \
                    "AssignExpr(Identifier(b),IntLiteral(3)), " \
                    "+, " \
                    "IntLiteral(5)" \
                ")" \
            ")]" \
        ")" \
    "])"

    str(ASTGenerator(input).generate()) == expect

def test_055():
    input = """
void main() {
    a = ;
}
"""

    print(ASTGenerator(input).generate())

    assert False

def test_056():
    input = """
void main() {
    invalidExpr = **;
}
"""

    print(ASTGenerator(input).generate())

    assert False

def test_057():
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
            "[ExprStmt(MemberAcces(Identifier(a).b))]" \
        ")" \
    "])"

    assert ASTGenerator(input).generate() == expect

def test_058():
    input = """
void main() {
    36.ab; // is valid ?????
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_059():
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
            "[ExprStmt(" \
                "MemberAcces(StructLiteral({1,2}).x)" \
            ")]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_060():
    input = """
void main() {
    a.;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_061():
    input = """
void main() {
    .a;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_062():
    input = """
void main() {
    .;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_063():
    input = """
void main() {
    a.36;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_064():
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
            "[ExprStmt(" \
                "MemberAccess(CallFunc(foo, []).x)" \
            ")]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_065():
    input = """
void main() {
    x.foo();
}
"""

    expect = "Program([" \
        "FuncDecl(" \
            "VoidType(), " \
            "main, " \
            "[], " \
            "[ExprStmt(" \
                "MemberAcces" \
            ")]" \
        ")" \
    "])"

def test_066():
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
            "[ExprStmt(" \
                "CallFunc(foo, [])" \
            ")]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_067():
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
            "[ExprStmt(" \
                "CallFunc(foo, [IntLiteral(5)])" \
            ")]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_068():
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
            "[ExprStmt(CallFunc(foo, [StringLiteral(AnTruong), FloatLiteral(2.4), IntLiteral(12)]))]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_069():
    input = """
void main() {
    foo(;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_070():
    input = """
void main() {
    foo);
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_071():
    input = """
void main() {
    ();
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_072():
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
            "[ExprStmt(StructLiteral({{IntLiteral(1), IntLiteral(2)}}))]" \
        ")" \
    "])"
    
    assert str(ASTGenerator(input).generate()) == expect

def test_073():
    input = """
void main() {
    x.{1,2};
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_074():
    input = """
void main() {
    {,};
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_075():
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
            "[StructLiteral({{" \
                "BinaryOp(IntLiteral(1), +, IntLiteral(2)), " \
                "BinaryOp(IntLiteral(3), +, IntLiteral(4))" \
            "}})]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_076():
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
            "[BlockStmt([" \
                "ExprStmt(BinaryOp(IntLiteral(3), +, IntLiteral(2)))" \
            "])]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_077():
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
            "[" \
                "BlockStmt(" \
                "[" \
                    "VarDecl(IntType(), aIntLiteral(3)), " \
                    "ExprStmt(CallFunc(foo, [])), " \
                    "IfStmt(if BinaryOp(Identifier(a), <, IntLiteral(5) then CallFunc(foo, []))" \
                "])" \
            "]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_078():
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
            "[BlockStmt([" \
                "VarDecl(IntType(), aIntLiteral(3)), " \
                "BlockStmt([" \
                    "VarDecl(FLoatType(), bFloatLiteral(5.0)), " \
                    "VarDecl(FloatType(), cBinaryOp(Identifier(a), +, Identifier(b))), " \
                    "ExprStmt(CallFunc(foo, [Identifier(a), Identifier(b), Identifier(c)])), " \
                    "BlockStmt([" \
                        "VarDecl(StringType(), sStringLiteral(Hello, World!))" \
                    "])" \
                "])" \
            "])]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

def test_079():
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
            "[BlockStmt([])]" \
        ")" \
    "])"

    return str(ASTGenerator(input).generate()) == expect

def test_080():
    input = """
void main() {
    {int a; foo();
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_081():
    input = """
void main() {
    int a; foo();}
}    
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_082():
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
            "[" \
                "VarDecl(IntType(), a), " \
                "VarDecl(IntType(), bCallFunc(foo, []))" \
            "]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_083():
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
            "[" \
                "VarDecl(FloatType(), a), " \
                "VarDecl(FloatType(),bCallFunc(foo, []))" \
            "]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_084():
    input = """
void main() {
    = a;
}
"""

    print(str(ASTGenerator(input).generate()))

    assert False

def test_085():
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
            "[" \
                "VarDecl(StringType(), s), " \
                "VarDecl(StringType(), ssStringLiteral(AnTruong))" \
            "]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

def test_086():
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
            "[VarDecl(StructType(Vector2), v2StructLiteral({{IntLiteral(3), IntLiteral(6)}}))]" \
        ")" \
    "])"

    assert str(ASTGenerator(input).generate()) == expect

