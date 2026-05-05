from .utils import ASTGenerator
from src.utils.nodes import *

def test_001():
    source = """
void main() {
    printString("Hello, World!");
}
"""
    expected = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(
                    FuncCall("printString", [StringLiteral("Hello, World!")])
                )
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_002():
    source = """
int add(int x, int y) {
    return x + y;
}

int multiply(int x, int y) {
    return x * y;
}

void main() {
    auto a = readInt();
    auto b = readInt();
    
    auto sum = add(a, b);
    auto product = multiply(a, b);
    
    printInt(sum);
    printInt(product);
}
"""
    expected = Program([
        FuncDecl(
            IntType(),
            "add",
            [Param(IntType(), "x"), Param(IntType(), "y")],
            BlockStmt([
                ReturnStmt(
                    BinaryOp(Identifier("x"), "+", Identifier("y"))
                )
            ])
        ),
        FuncDecl(
            IntType(),
            "multiply",
            [Param(IntType(), "x"), Param(IntType(), "y")],
            BlockStmt([
                ReturnStmt(
                    BinaryOp(Identifier("x"), "*", Identifier("y"))
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "a", FuncCall("readInt", [])),
                VarDecl(None, "b", FuncCall("readInt", [])),
                VarDecl(None, "sum", FuncCall("add", [Identifier("a"), Identifier("b")])),
                VarDecl(None, "product", FuncCall("multiply", [Identifier("a"), Identifier("b")])),
                ExprStmt(FuncCall("printInt", [Identifier("sum")])),
                ExprStmt(FuncCall("printInt", [Identifier("product")]))
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_003():
    source = """
void main() {
    auto n = readInt();
    auto i = 0;
    
    while (i < n) {
        printInt(i);
        ++i;
    }
    
    for (auto j = 0; j < n; ++j) {
        if (j % 2 == 0) {
            printInt(j);
        }
    }
}
"""
    expected = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "n", FuncCall("readInt", [])),
                VarDecl(None, "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", Identifier("n")),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(PrefixOp("++", Identifier("i")))
                    ])
                ),
                ForStmt(
                    VarDecl(None, "j", IntLiteral(0)),
                    BinaryOp(Identifier("j"), "<", Identifier("n")),
                    PrefixOp("++", Identifier("j")),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(
                                BinaryOp(Identifier("j"), "%", IntLiteral(2)),
                                "==",
                                IntLiteral(0)
                            ),
                            BlockStmt([
                                ExprStmt(FuncCall("printInt", [Identifier("j")]))
                            ]),
                            None
                        )
                    ])
                )
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_004():
    source = """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

void main() {
    auto num = readInt();
    auto result = factorial(num);
    printInt(result);
}
"""
    expected = Program([
        FuncDecl(
            IntType(),
            "factorial",
            [Param(IntType(), "n")],
            BlockStmt([
                IfStmt(
                    BinaryOp(Identifier("n"), "<=", IntLiteral(1)),
                    BlockStmt([
                        ReturnStmt(IntLiteral(1))
                    ]),
                    BlockStmt([
                        ReturnStmt(
                            BinaryOp(
                                Identifier("n"),
                                "*",
                                FuncCall(
                                    "factorial",
                                    [BinaryOp(Identifier("n"), "-", IntLiteral(1))]
                                )
                            )
                        )
                    ])
                )
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "num", FuncCall("readInt", [])),
                VarDecl(None, "result", FuncCall("factorial", [Identifier("num")])),
                ExprStmt(FuncCall("printInt", [Identifier("result")]))
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_005():
    source = """
void main() {
    // With auto and initialization
    auto x = readInt();
    auto y = readFloat();
    auto name = readString();
    
    // With auto without initialization
    auto sum;
    sum = x + y;              // sum: float (inferred from first usage - assignment)
    
    // With explicit type and initialization
    int count = 0;
    float total = 0.0;
    string greeting = "Hello, ";
    
    // With explicit type without initialization
    int i;
    float f;
    i = readInt();            // assignment to int
    f = readFloat();          // assignment to float
    
    printFloat(sum);
    printString(greeting);
    printString(name);
}
"""
    expected = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(None, "x", FuncCall("readInt", [])),
                VarDecl(None, "y", FuncCall("readFloat", [])),
                VarDecl(None, "name", FuncCall("readString", [])),

                VarDecl(None, "sum", None),
                ExprStmt(
                    AssignExpr(
                        Identifier("sum"),
                        BinaryOp(Identifier("x"), "+", Identifier("y"))
                    )
                ),

                VarDecl(IntType(), "count", IntLiteral(0)),
                VarDecl(FloatType(), "total", FloatLiteral(0.0)),
                VarDecl(StringType(), "greeting", StringLiteral("Hello, ")),

                VarDecl(IntType(), "i", None),
                VarDecl(FloatType(), "f", None),
                ExprStmt(
                    AssignExpr(Identifier("i"), FuncCall("readInt", []))
                ),
                ExprStmt(
                    AssignExpr(Identifier("f"), FuncCall("readFloat", []))
                ),

                ExprStmt(FuncCall("printFloat", [Identifier("sum")])),
                ExprStmt(FuncCall("printString", [Identifier("greeting")])),
                ExprStmt(FuncCall("printString", [Identifier("name")]))
            ])
        )
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


    
def test_006():
    source = """
struct A {};
struct B {int a; ID b;};
struct C {float a; string b;};
struct D {Z a;};
"""
    expected = Program([
        StructDecl('A', []),
        StructDecl('B', [MemberDecl(IntType(), 'a'), MemberDecl(StructType('ID'), 'b')]),
        StructDecl('C', [MemberDecl(FloatType(), 'a'), MemberDecl(StringType(), 'b')]),
        StructDecl('D', [ MemberDecl(StructType('Z'), 'a')]),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_007():
    source = """
void main() {}
main(int a) {}
int main(int a, ID b) {}
float main(float b) {}
string main(string b, int a, Z b) {}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([])),
        FuncDecl(None, "main",
            [Param(IntType(), "a")],
            BlockStmt([])
        ),
        FuncDecl(IntType(), "main",
            [Param(IntType(), "a"), Param(StructType("ID"), "b")],
            BlockStmt([])
        ),
        FuncDecl(FloatType(), "main",
            [Param(FloatType(), "b")],
            BlockStmt([])
        ),
        FuncDecl(StringType(), "main",
            [
                Param(StringType(), "b"),
                Param(IntType(), "a"),
                Param(StructType("Z"), "b")
            ],
            BlockStmt([])
        ),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_008():
    source = """
void main() {
    1;
    1.3;
    "s";
    {};
    {1, {2}};
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(IntLiteral(1)),
            ExprStmt(FloatLiteral(1.3)),
            ExprStmt(StringLiteral("s")),
            ExprStmt(StructLiteral([])),
            ExprStmt(StructLiteral([
                IntLiteral(1),
                StructLiteral([
                    IntLiteral(2)
                ])
            ]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_009():
    source = """
void main() {
    a = b = 1.0;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                AssignExpr(
                    Identifier("a"),
                    AssignExpr(
                        Identifier("b"),
                        FloatLiteral(1.0),
                    )
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_010():
    source = """
void main() {
    1 || 2 || 3;
    a = 2 || 3;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                BinaryOp(
                    BinaryOp(IntLiteral(1), "||", IntLiteral(2)),
                    "||",
                    IntLiteral(3)
                )
            ),
            ExprStmt(
                AssignExpr( Identifier("a"), BinaryOp( IntLiteral(2), "||", IntLiteral(3) ) )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_011():
    source = """
void main() {
    1 && 2 && 3;
    1 || 2 && 3;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                BinaryOp(
                    BinaryOp(IntLiteral(1), "&&", IntLiteral(2)),
                    "&&",
                    IntLiteral(3)
                )
            ),
            ExprStmt(
                BinaryOp( IntLiteral(1), "||", BinaryOp( IntLiteral(2), "&&", IntLiteral(3) ) )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_012():
    source = """
void main() {
    1 == 2 != 3;
    1 && 2 == 3;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                BinaryOp(
                    BinaryOp(IntLiteral(1), "==", IntLiteral(2)),
                    "!=",
                    IntLiteral(3)
                )
            ),
            ExprStmt(
                BinaryOp(
                    IntLiteral(1),
                    "&&",
                    BinaryOp(IntLiteral(2), "==", IntLiteral(3))
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_013():
    source = """
void main() {
    1 > 2 >= 3 < 4 <= 5;
    1 == 2 > 3;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            BinaryOp(IntLiteral(1), ">", IntLiteral(2)),
                            ">=",
                            IntLiteral(3)
                        ),
                        "<",
                        IntLiteral(4)
                    ),
                    "<=",
                    IntLiteral(5)
                )
            ),
            ExprStmt(
                BinaryOp(
                    IntLiteral(1),
                    "==",
                    BinaryOp(IntLiteral(2), ">", IntLiteral(3))
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_014():
    source = """
void main() {
    1 + 2 - 3;
    1 > 2 + 3;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                BinaryOp(
                    BinaryOp(IntLiteral(1), "+", IntLiteral(2)),
                    "-",
                    IntLiteral(3)
                )
            ),
            ExprStmt(
                BinaryOp(
                    IntLiteral(1),
                    ">",
                    BinaryOp(IntLiteral(2), "+", IntLiteral(3))
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_015():
    source = """
void main() {
    1 * 2 / 3 % 4;
    1 + 2 % 3;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(IntLiteral(1), "*", IntLiteral(2)),
                        "/",
                        IntLiteral(3)
                    ),
                    "%",
                    IntLiteral(4)
                )
            ),
            ExprStmt(
                BinaryOp(
                    IntLiteral(1),
                    "+",
                    BinaryOp(IntLiteral(2), "%", IntLiteral(3))
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_016():
    source = """
void main() {
    a;
    (a + 2) * 3;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
               Identifier('a')
            ),
            ExprStmt(
                BinaryOp( BinaryOp( Identifier('a'), "+", IntLiteral(2)), '*', IntLiteral(3))
            ),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_017():
    source = """
void main() {
    foo();
    foo1(a + 2, a = 2);
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
               FuncCall('foo', [])
            ),
            ExprStmt(
                FuncCall('foo1', [BinaryOp( Identifier('a'), "+", IntLiteral(2)), AssignExpr( Identifier('a'), IntLiteral(2))])
            ),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_018():
    source = """
void main() {
    a.b.c.d;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                MemberAccess(
                    MemberAccess(
                        MemberAccess(Identifier("a"), "b"),
                        "c"
                    ),
                    "d"
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_019():
    source = """
void main() {
    3 * a.b;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                BinaryOp(IntLiteral(3), '*',  MemberAccess(Identifier("a"), "b"))
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_020():
    source = """
void main() {
    -+!-+! 2;
    -a.b.c;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                PrefixOp(
                    "-",
                    PrefixOp(
                        "+",
                        PrefixOp(
                            "!",
                            PrefixOp(
                                "-",
                                PrefixOp(
                                    "+",
                                    PrefixOp(
                                        "!",
                                        IntLiteral(2)
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            ExprStmt(
                PrefixOp( "-",
                MemberAccess(
                    MemberAccess( Identifier("a"), "b"),
                    "c"
                ))
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_021():
    source = """
void main() {
    ++ -- ++ -- ++ ++ 1;
    -++a;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                PrefixOp(
                    "++",
                    PrefixOp(
                        "--",
                        PrefixOp(
                            "++",
                            PrefixOp(
                                "--",
                                PrefixOp(
                                    "++",
                                    PrefixOp(
                                        "++",
                                        IntLiteral(1)
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            ExprStmt(
                    PrefixOp('-',PrefixOp( "++", Identifier("a")))
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_022():
    source = """
void main() {
    1 ++ ++ -- ++ -- ++;
    --a++;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                PostfixOp(
                    "++",
                    PostfixOp(
                        "--",
                        PostfixOp(
                            "++",
                            PostfixOp(
                                "--",
                                PostfixOp(
                                    "++",
                                    PostfixOp(
                                        "++",
                                        IntLiteral(1)
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            ExprStmt(
                    PrefixOp('--',PostfixOp( "++", Identifier("a")))
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_023():
    source = """
void main() {
    string a = 3 + 1;
    auto b;
    ID f;
    int g;
    float k = foo();
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(
                StringType(),
                "a",
                BinaryOp(IntLiteral(3), "+", IntLiteral(1))
            ),
            VarDecl(None, "b", None),
            VarDecl(StructType("ID"), "f", None),
            VarDecl(IntType(), "g", None),
            VarDecl(FloatType(), "k", FuncCall("foo", []))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_024():
    source = """
void main() {
    break;
    continue;
    return ;
    return foo.a + 2;

}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            BreakStmt(),
            ContinueStmt(),
            ReturnStmt(None),
            ReturnStmt(
                BinaryOp(
                    MemberAccess(Identifier("foo"), "a"),
                    "+",
                    IntLiteral(2)
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_025():
    source = """
void main() {
    {}
    {continue; break;}
    {{{return;}}}
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            BlockStmt([]),
            BlockStmt([
               ContinueStmt(), BreakStmt()
            ]),
            BlockStmt([
                BlockStmt([
                    BlockStmt([
                        ReturnStmt(None)
                    ])
                ])
            ])
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_026():
    source = """
void main() {
    a = 1;
    a = b = c;
    a.b.d = c = e;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(
                AssignExpr(
                Identifier("a"),
                IntLiteral(1))
            ),
            ExprStmt(
                AssignExpr(
                    Identifier("a"),
                    AssignExpr(
                        Identifier("b"),
                        Identifier("c")
                    )
                )
            ),
            ExprStmt(
                AssignExpr(
                    MemberAccess(
                        MemberAccess(Identifier("a"), "b"),
                        "d"
                    ),
                    AssignExpr(
                        Identifier("c"),
                        Identifier("e")
                    )
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_027():
    source = """
void main() {
    if (1 + 2) continue;

    if (a.b.c) {
        break;
        return;
    }
    else break;

    if (foo()) {} else {}
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(
                BinaryOp(IntLiteral(1), "+", IntLiteral(2)),
                ContinueStmt(),
                None
            ),
            IfStmt(
                MemberAccess(
                    MemberAccess(Identifier("a"), "b"),
                    "c"
                ),
                BlockStmt([
                    BreakStmt(),
                    ReturnStmt(None)
                ]),
                BreakStmt()
            ),
            IfStmt(
                FuncCall("foo", []),
                BlockStmt([]),
                BlockStmt([])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_028():
    source = """
void main() {
    if (1) 1;
    else if (2) continue;
    else {}
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            IfStmt(
                IntLiteral(1),
                ExprStmt(IntLiteral(1)),
                IfStmt(
                    IntLiteral(2),
                    ContinueStmt(),
                    BlockStmt([])
                ),
            ),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_029():
    source = """
void main() {
    while(a.b) {}
    while(foo()) return;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            WhileStmt(
                MemberAccess(Identifier("a"), "b"),
                BlockStmt([])
            ),
            WhileStmt(
                FuncCall("foo", []),
                ReturnStmt(None)
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_030():
    source = """
void main() {
    for (;;) continue;
    for (a.b=1;a.b;) {}
    for (auto a = 1; ; ) {return;}
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(
                None,
                None,
                None,
                ContinueStmt()
            ),
            ForStmt(
                 ExprStmt(AssignExpr(
                    MemberAccess(Identifier("a"), "b"),
                    IntLiteral(1)
                ))
                ,
                MemberAccess(Identifier("a"), "b"),
                None,
                BlockStmt([])
            ),
            ForStmt(
                VarDecl( None, "a", IntLiteral(1)),
                None,
                None,
                BlockStmt([
                    ReturnStmt(None)
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_031():
    source = """
void main() {
    for(;;a++) {}
    for (;;++a) {}
    for (;;a.b=2) {}
    for (a=1;;a.b=2) {}
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(
                None,
                None,
                PostfixOp('++', Identifier("a")),
                BlockStmt([])
            ),
            ForStmt(
                None,
                None,
                PrefixOp('++', Identifier("a")),
                BlockStmt([])
            ),
            ForStmt(
                None,
                None,
                AssignExpr(
                    MemberAccess(Identifier("a"), "b"),
                    IntLiteral(2)
                ),
                BlockStmt([])
            ),
            ForStmt(
                 ExprStmt(AssignExpr(
                   Identifier("a"),
                    IntLiteral(1)
                )),
                None,
                AssignExpr(
                    MemberAccess(Identifier("a"), "b"),
                    IntLiteral(2)
                ),
                BlockStmt([])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_032():
    source = """
void main() {
    for (int a;i<2;a.b=2) {}
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), "a", None),
                BinaryOp(Identifier("i"), "<", IntLiteral(2)),
                AssignExpr(
                    MemberAccess(Identifier("a"), "b"),
                    IntLiteral(2)
                ),
                BlockStmt([])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_033():
    source = """
void main() {
    switch(a) {
        case 1: b = 2;
        case 2: c = 3;
        default: d = 4;
    }
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(
                Identifier("a"),
                [
                    CaseStmt(
                        IntLiteral(1),
                        [ExprStmt(AssignExpr(Identifier("b"), IntLiteral(2)))]
                    ),
                    CaseStmt(
                        IntLiteral(2),
                        [ExprStmt(AssignExpr(Identifier("c"), IntLiteral(3)))]
                    )
                ],
                DefaultStmt([
                    ExprStmt(AssignExpr(Identifier("d"), IntLiteral(4)))
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_034():
    source = """
void main() {
    switch(x) {
        case 1: d = 4; b = 2; c = 3;
        case 2: y = 3;
    }
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(
                Identifier("x"),
                [
                    CaseStmt(IntLiteral(1), [
                    ExprStmt(AssignExpr(Identifier("d"), IntLiteral(4))),
                    ExprStmt(AssignExpr(Identifier("b"), IntLiteral(2))),
                    ExprStmt(AssignExpr(Identifier("c"), IntLiteral(3)))
                ]),
                    CaseStmt(
                        IntLiteral(2),
                        [ExprStmt(AssignExpr(Identifier("y"), IntLiteral(3)))]
                    )
                ],
                None
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_035():
    source = """
void main() {
    switch(1) {
        default: d = 4; b = 2; c = 3;
    }
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(
                IntLiteral(1),
                [],
                DefaultStmt([
                    ExprStmt(AssignExpr(Identifier("d"), IntLiteral(4))),
                    ExprStmt(AssignExpr(Identifier("b"), IntLiteral(2))),
                    ExprStmt(AssignExpr(Identifier("c"), IntLiteral(3)))
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_036():
    source = """
void main() {
    switch(1) {
    }
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(
                IntLiteral(1),
                [],
                None
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_037():
    source = """
void main() {
    a = 1;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier('a'),IntLiteral(1)))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_039():
    source = """
void main() {
    a = {1, 2, 3};
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(Identifier("a"),StructLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)])))
            ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_040():
    source = """
void main() {
    {1, 2}.a.b;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(MemberAccess(MemberAccess(StructLiteral([IntLiteral(1), IntLiteral(2)]),'a'),'b'))]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_041():
    source = """
void main() {
   
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
           
            
            ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_042():
    source = """
void main() {
    a.b = 2;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(AssignExpr(MemberAccess(Identifier("a"), "b"),IntLiteral(2)))
            
            ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_043():
    source = """
void main() {
    if (1) 
        if (2) return 2; 
        else return;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
                IfStmt(
                    IntLiteral(1),
                    IfStmt(
                        IntLiteral(2),
                        ReturnStmt(IntLiteral(2)),
                        ReturnStmt()
                    ),
                    None
                )
    
            ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_044():
    source = """
void main() {
    if (1) 
        if (2) return 2; 
        else return;
}
"""
    expected = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
                IfStmt(
                    IntLiteral(1),
                    IfStmt(
                        IntLiteral(2),
                        ReturnStmt(IntLiteral(2)),
                        ReturnStmt()
                    ),
                    None
                )
    
            ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)