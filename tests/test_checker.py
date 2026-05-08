"""
Test cases for TyC Static Semantic Checker

This module contains test cases for the static semantic checker.
100 test cases covering all error types and comprehensive scenarios.
"""

from .utils import Checker
from src.utils.nodes import (
    Program,
    FuncDecl,
    BlockStmt,
    VarDecl,
    AssignExpr,
    ExprStmt,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    Identifier,
    BinaryOp,
    MemberAccess,
    FuncCall,
    StructDecl,
    MemberDecl,
    Param,
    ReturnStmt,
)

def test_001():
    """Test a valid program that should pass all checks"""
    source = """
void main() {
    int x = 5;
    int y = x + 1;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_002():
    """Test valid program with int type inference"""
    source = """
void main() {
    int x = 10;
    int y = 3.14;
    int z = x + y;
}
"""
    expected = "TypeMismatchInStatement(VarDecl(IntType(), y = FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected


def test_003():
    """Test valid program with functions"""
    source = """
int add(int x, int y) {
    return x + y;
}
void main() {
    int sum = add(5, 3);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_004():
    """Test valid program with struct"""
    source = """
struct Point {
    int x;
    int y;
};
void main() {
    Point p;
    p.x = 10;
    p.y = 20;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_005():
    """Test valid program with nested blocks"""
    source = """
void main() {
    int x = 10;
    {
        int y = 20;
        int z = x + y;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_006():
    source = """
struct Point {
    int x;
    int y;
};
struct Point {
    int z;
};
"""
    assert Checker(source).check_from_source() == "Redeclared(Struct, Point)"

def test_007():
    source = """
int add(int x, int y) {
    return x + y;
}
int add(int a, int b) {
    return a + b;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Function, add)"

def test_008():
    source = """
void main() {
    int count = 10;
    int count = 20;  // Redeclared(Variable, count)
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Variable, count)"

def test_009():
    source = """
int calculate(int x, float y, int x) {  // Redeclared(Parameter, x)
    return x + y;
}
"""
    assert Checker(source).check_from_source() == "Redeclared(Parameter, x)"

def test_010():
    source = """
void example() {
    int value = 100;  // Function variable
    
    {
        int value = 200;  // Valid: shadows function variable
        {
            int value = 300;  // Valid: shadows block variable
        }
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"

def test_011():
    source = """
void test() {
    int x = 10;
    {
        int y = 20;  // Valid: different variable name
    }
    int y = 30;  // Valid: y in outer scope doesn't conflict with y in inner scope (different block)
}

"""
    assert Checker(source).check_from_source() == "Static checking passed"

def test_012():
    source = """
void example() {
    int result = undeclaredVar + 10;  // UndeclaredIdentifier(undeclaredVar)
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(undeclaredVar)"

def test_013():
    source = """
void test() {
    int x = y + 5;  // UndeclaredIdentifier(y) - y used before declaration
    int y = 10;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(y)"

def test_014():
    source = """
void method1() {
    int localVar = 42;
}

void method2() {
    int value = localVar + 1;  // UndeclaredIdentifier(localVar) - different function scope
}
"""
    assert Checker(source).check_from_source() == "UndeclaredIdentifier(localVar)"

def test_015():
    source = """
void valid() {
    int x = 10;
    int y = x + 5;  // Valid: x is declared before use
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"

def test_016():
    source = """
int calculate(int x, int y) {
    int result = x + y;  // Valid: parameters x and y are visible
    return result;
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"

def test_017():
    source = """
void nested() {
    int outer = 10;
    {
        int inner = outer + 5;  // Valid: outer is in enclosing scope
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"

def test_018():
    source = """
void main() {
    int result = calculate(5, 3);  // UndeclaredFunction(calculate)
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(calculate)"

def test_019():
    source = """
void test() {
    int value = add(10, 20);  // UndeclaredFunction(add) - if add is declared later
}

int add(int x, int y) {
    return x + y;
}
"""
    assert Checker(source).check_from_source() == "UndeclaredFunction(add)"

def test_020():
    source = """
int multiply(int x, int y) {
    return x * y;
}

void main() {
    int result = multiply(5, 3);  // Valid: multiply is declared before
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"

def test_021():
    source = """
void example() {
    int x = readInt();        // Valid: built-in function
    printInt(x);              // Valid: built-in function
    float y = readFloat();    // Valid: built-in function
    string s = readString();  // Valid: built-in function
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"

def test_022():
    source = """
void main() {
    Point p;  // UndeclaredStruct(Point)
}

struct Point {
    int x;
    int y;
};
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Point)"

def test_023():
    source = """
void test() {
    Person person;  // UndeclaredStruct(Person) - if Person is declared later
}

struct Person {
    string name;
    int age;
};
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(Person)"

def test_024():
    source = """
struct Address {
    string street;
    City city;  // UndeclaredStruct(City) - if City is declared later
};

struct City {
    string name;
};
"""
    assert Checker(source).check_from_source() == "UndeclaredStruct(City)"

# def test_025():
#     source = """
# struct Point {
#     int x;
#     int y;
# };

# void main() {
#     Point p1;  // Valid: Point is declared before
#     Point p2 = {10, 20};  // Valid: Point is declared before
# }
# """
#     assert Checker(source).check_from_source() == "Static checking passed"

def test_026():
    source = """
struct Point {
    int x;
    int y;
};

struct Address {
    string street;
    Point location;  // Valid: Point is declared before
};
"""
    assert Checker(source).check_from_source() == "Static checking passed"

def test_027():
    source = """
void loopError() {
    break;     // Error: MustInLoop(break)
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(BreakStmt())"

def test_028():
    source = """
void loopError() {
    continue;  // Error: MustInLoop(continue)
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(ContinueStmt())"

def test_029():
    source = """
void switchError() {
    int x = 1;
    switch (x) {
        case 1:
            break;
            continue;
    }
}
"""
    assert Checker(source).check_from_source() == "MustInLoop(ContinueStmt())"

def test_030():
    source = """
void switchError() {
    for (int i = 0; i < 5; ++i) {            
        break;
        continue;
    }
}
"""
    assert Checker(source).check_from_source() == "Static checking passed"

def test_031():
    source = """
void arithmeticError() {
    int x = 5;
    string text = "hello";
    
    int sum = x + text;     // Error: TypeMismatchInExpression at binary operation
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(x), +, Identifier(text)))"

def test_032():
    source = """
void arithmeticError() {
    int x = 5;
    string text = "hello";
    
    float result = x * text; // Error: TypeMismatchInExpression at binary operation
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(x), *, Identifier(text)))"


def test_033():
    source = """
void modulusError() {
    float f = 3.14;
    int x = 10 % 2;
    
    int result = f % x;      // Error: TypeMismatchInExpression at binary operation (float % int)
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(f), %, Identifier(x)))"


def test_034():
    source = """
void modulusError() {
    float f = 3.14;
    int x = 10;
    
    int result2 = x % f;     // Error: TypeMismatchInExpression at binary operation (int % float)
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(x), %, Identifier(f)))"

def test_035():
    source = """
void relationalError() {
    int x = 10 == 1;
    string text = "hello";
    
    int equal = text == x;   // Error: TypeMismatchInExpression at binary operation
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(text), ==, Identifier(x)))"

def test_036():
    source = """
void relationalError() {
    int x = 10 > 2;
    string text = "hello";
    
    int result = x < text;   // Error: TypeMismatchInExpression at binary operation
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(x), <, Identifier(text)))"


def test_037():
    source = """
void logicalError() {
    float f = 3.14;
    int x = 10 && 20;
    
    int result = f && x;     // Error: TypeMismatchInExpression at binary operation
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(BinaryOp(Identifier(f), &&, Identifier(x)))"


def test_038():
    source = """
void logicalError() {
    float f = 3.14;
    int x = !10;
    
    int not = !f;            // Error: TypeMismatchInExpression at unary operation
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(!Identifier(f)))"

def test_039():
    source = """
void incrementError() {
    float f = 3.14;
    ++f;                     // Error: TypeMismatchInExpression at unary operation
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(++Identifier(f)))"

def test_040():
    source = """
void incrementError() {
    float f = 3.14;
    f++;                     // Error: TypeMismatchInExpression at postfix operation
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PostfixOp(Identifier(f)++))"


def test_041():
    source = """
void incrementOperandError() {
    int x = 5;
    ++ x;
    x ++;
    ++5;                     // Error: TypeMismatchInExpression at unary operation (cannot increment literal)
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(++IntLiteral(5)))"


def test_042():
    source = """
void incrementOperandError() {
    int x = 5;
    --(x + 1);               // Error: TypeMismatchInExpression at unary operation (cannot increment expression)
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PrefixOp(--BinaryOp(Identifier(x), +, IntLiteral(1))))"

def test_043():
    source = """
void incrementOperandError() {
    int x = 5;
    (x + 2)++;               // Error: TypeMismatchInExpression at postfix operation (cannot increment expression
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(PostfixOp(BinaryOp(Identifier(x), +, IntLiteral(2))++))"


def test_044():
    source = """
struct Point {
    int x;
    int y;
};

void memberAccessError() {
    int x = 10;
    int value = x.member;    // Error: TypeMismatchInExpression at member access
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(MemberAccess(Identifier(x).member))"

# def test_045():
#     source = """
# struct Point {
#     int x;
#     int y;
# };

# void memberAccessError() {
#     Point p = {10, 20};
#     int t = p.x + p.y;
#     int invalid = p.z;       // Error: TypeMismatchInExpression at member access (z doesn't exist)
# }
# """
#     assert Checker(source).check_from_source() == "TypeMismatchInExpression(MemberAccess(Identifier(p).z))"

def test_046():
    source = """
void process(int x) { }

void callError() {
    string text = "123";
    process(text);   // sai kiểu: string -> int
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(process, [Identifier(text)]))"

def test_047():
    source = """
int add(int x, int y) {
    return x + y;
}

void callArgumentError() {
    int result = add(10);   // thiếu 1 tham số
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(add, [IntLiteral(10)]))"

def test_048():
    source = """
int add(int x, int y) {
    return x + y;
}

void callArgumentError() {
    int result = add(10, 20, 30);   // dư tham số
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(add, [IntLiteral(10), IntLiteral(20), IntLiteral(30)]))"

def test_049():
    source = """
void assignmentExpressionError() {
    int x = 10;
    string text = "hello";
    float f = 3.14;
    
    int result = (x = text) + 5;     // Error: TypeMismatchInExpression at assignment expression (int = string)
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(AssignExpr(Identifier(x) = Identifier(text)))"

def test_050():
    source = """
void conditionalError() {
    float x = 5.0;
    if (x) {
        printInt(1);
    }
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(IfStmt(if Identifier(x) then BlockStmt([ExprStmt(FuncCall(printInt, [IntLiteral(1)]))])))"

def test_051():
    source = """
void conditionalError() {
    string message = "hello";
    if (message) {
        printString(message);
    }
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(IfStmt(if Identifier(message) then BlockStmt([ExprStmt(FuncCall(printString, [Identifier(message)]))])))"

def test_052():
    source = """
void whileError() {
    float f = 1.5;
    while (f) {
        printFloat(f);
    }
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(WhileStmt(while Identifier(f) do BlockStmt([ExprStmt(FuncCall(printFloat, [Identifier(f)]))])))"

def test_054():
    source = """
void foo() {
    int i = 0;
    for (i=1; "s"; i++) {}
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(1))); StringLiteral('s'); PostfixOp(Identifier(i)++) do BlockStmt([])))"

def test_055():
    source = """
void switchError() {
    float f = 3.14;
    switch (f) {  // Error: TypeMismatchInStatement at switch statement
        case 1: break;
    }
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch Identifier(f) cases [CaseStmt(case IntLiteral(1): [BreakStmt()])]))"

def test_056():
    source = """
int getValue() {
    return "invalid";  // Error: TypeMismatchInStatement at return statement
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return StringLiteral('invalid')))"


def test_057():
    source = """
int returnVoidError() {
    return;  // Error: TypeMismatchInStatement at return statement (non-void function must return value)
}
"""
    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return))"

def test_059():
    source = """
int foo() {
    auto a;
    auto b;
    a = b;
}
"""
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(AssignExpr(Identifier(a) = Identifier(b)))"

def test_062():
    source = """
    struct Point {
        int Point;
        int y;
    };
    void main(Point a) {}
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_063():
    source = """
    struct Point {
        int Point;
        int y;
    };
    void Point(Point a) {}
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_064():
    source = """
    void main() {
        int a;
        switch (1) {
            case 1:
                int a;
                int b;
            case 2:
                int c = a;
                {int a;}
            default:
                int d = b;
                string b;
        }
    }
    """
    assert Checker(source).check_from_source() == "Redeclared(Variable, b)"

def test_065():
    source = """
    struct A {};
    A B () {
        int A;
        A a;
    }
    """

    assert Checker(source).check_from_source() == "Static checking passed"

def test_066():
    source = """
    void main() {
        while(1){
            break;
            continue;
            while(2) {
                {
                    break;
                    continue;
                    continue;
                    break;
                }
            }
            break;
            continue;
            {continue; break;}
        }
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_067():
    source = """
    void main() {
        return;
        return 1;
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(ReturnStmt(return IntLiteral(1)))"

def test_068():
    source = """
    void main() {
        int a = +- 1;
        int b = +- 1.0;
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(IntType(), b = PrefixOp(+PrefixOp(-FloatLiteral(1.0)))))"

def test_069():
    source = """
    void main() {
        int x;
        int y = (x = 5) + 7;
    }
    """

    assert Checker(source).check_from_source() == "Static checking passed"

def test_070():
    source = """
    void main() {
        int x;
        x = x = x = 3.14;
    }
    """
    assert Checker(source).check_from_source() == "TypeMismatchInExpression(AssignExpr(Identifier(x) = FloatLiteral(3.14)))"

def test_071():
    source = """
    void main() {
        auto a;
        auto b;
        int c = a + b;
    }
    """

    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BinaryOp(Identifier(a), +, Identifier(b)))"

def test_072():
    source = """
    void main() {
        auto b;
        int c = 1 + b;
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_073():
    source = """
    void main() {
        auto b;
        int c = b * 2;
    }
    """

    assert Checker(source).check_from_source() == "Static checking passed"

def test_074():
    source = """
    void main() {
        auto a;
        ++ a;
        float b = a;
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(FloatType(), b = Identifier(a)))"

def test_075():
    source = """
    void main() {
        auto a;
        + a;
        float b = a;
    }
    """

    assert Checker(source).check_from_source() == "TypeCannotBeInferred(PrefixOp(+Identifier(a)))"

def test_076():
    source = """
    void main() {
        auto a; auto b;
        a = 1;
        a + b;
    }
    """

    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BinaryOp(Identifier(a), +, Identifier(b)))"

def test_077():
    source = """
    void main() {
        auto a;
        a ++;
        float b = a;
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(FloatType(), b = Identifier(a)))"

def test_078():
    source = """
    void foo(int a){}
    void main() {
        auto a;
        foo(a);
        float b = a;
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(FloatType(), b = Identifier(a)))"

def test_079():
    source = """
    void main() {
        auto a;
        for (;a;) {}
        float b = a;
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(FloatType(), b = Identifier(a)))"

def test_080():
    source = """
    void main() {
        auto a;
        switch (a){}
        float b = a;
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(FloatType(), b = Identifier(a)))"

def test_081():
    source = """
    func() { auto a; return a;}
    void main() {
        auto a = func();
        float b = a;
    }
    """

    assert Checker(source).check_from_source() == "TypeCannotBeInferred(ReturnStmt(return Identifier(a)))"

def test_082():
    source = """
    void unused_auto() {
        auto x;
    }  // TypeCannotBeInferred(BlockStmt([VarDecl(auto, x)]))
    """

    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BlockStmt([VarDecl(auto, x)]))"

def test_083():
    source = """
    void main() {
        auto b;
        int c = 1.0 + b;
    }
    """
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BinaryOp(FloatLiteral(1.0), +, Identifier(b)))"

def test_084():
    source = """
    void main() {
        auto b;
        int a = 1;
        float c = b + a;
        int d = b;
    }
    """
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BinaryOp(Identifier(b), +, Identifier(a)))"

def test_085():
    source = """
    void main() {
        auto b;
        int a = 1;
        auto c = a + b;
    }
    """
    assert Checker(source).check_from_source() == "TypeCannotBeInferred(BinaryOp(Identifier(a), +, Identifier(b)))"

def test_086():
    source = """
    int a () {return 1;}
    void foo() {
        int x = 1;
        switch (x) {
            case a():
        }
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch Identifier(x) cases [CaseStmt(case FuncCall(a, []): [])]))"

def test_087():
    source = """
    int a(){return 1;}
    void foo() {
        int a;
        switch (a()) {
            case 1 + a:
        }
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(SwitchStmt(switch FuncCall(a, []) cases [CaseStmt(case BinaryOp(IntLiteral(1), +, Identifier(a)): [])]))"

def test_088():
    source = """
    struct Point {
        int x;
        int y;
    };
    
    void foo() {
        Point p = {10};
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInExpression(StructLiteral({IntLiteral(10)}))"

def test_089():
    source = """
    struct A {};
    struct B {};
    void foo() {
        A a;
        B b = a;
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(StructType(B), b = Identifier(a)))"

def test_090():
    source = """
    struct A {};
    struct B {};
    void foo(A a) {}
    void main() {
        A a;
        B b;
        foo(a);
        foo(b);
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInExpression(FuncCall(foo, [Identifier(b)]))"

def test_091():
    source = """
    struct Point {
        int x;
        int y;
    };
    
    void foo() {
        auto a;
        auto b;
        Point p = {a , b};
        a = b = 1;
    }
    """

    assert Checker(source).check_from_source() == "Static checking passed"

def test_092():
    source = """
    struct Point {
        int x;
        int y;
    };
    
    struct Person {
        string name;
        int age;
        float height;
    };
    
    void main() {
        // Struct variable declaration without initialization
        Point p1;
        p1.x = 10;
        p1.y = 20;
    
        // Struct variable declaration with initialization
        Point p2 = {30, 40};
    
        // Access and modify struct members
        printInt(p2.x);
        printInt(p2.y);
    
        // Struct assignment
        p1 = p2;  // Copy all members
    
        // Person struct usage
        Person person1 = {"John", 25, 1.75};
        printString(person1.name);
        printInt(person1.age);
        printFloat(person1.height);
    
        // Modify struct members
        person1.age = 26;
        person1.height = 1.76;
    
        // Using struct with auto
        auto p3 = p2;  // p3: Point (inferred from assignment)
        printInt(p3.x);
    }
    """
        
    assert Checker(source).check_from_source() == "Static checking passed"

def test_093():
    source = """
    foo() {}
    
    void main() {
        int a = foo();
    }
    """

    assert Checker(source).check_from_source() == "TypeMismatchInStatement(VarDecl(IntType(), a = FuncCall(foo, [])))"