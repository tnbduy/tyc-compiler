"""
Parser test cases for TyC compiler
TODO: Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser
from tests.utils import Tokenizer

def test_001():
    input = """
    void main() {
    }
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_002():
    input = """
    void main() {
        3 + 3;
    }
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_003():
    input = """
    void main() {
        int a = 3;
    }
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_004():
    input = """
    void main() {
        int a = 3 + 3;
    }
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_005():
    input = """
    int foo() {
        return;
    }
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_006():
    input = """
    int foo() {
        return 1;
    }
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_007():
    input = """
    int foo(int a) {
        return a;
    }
"""
    expect = "success"
    print(Tokenizer(input).get_tokens_as_string())
    assert Parser(input).parse() == expect

def test_008():
    input = """
    void main() {
        ;
    }
"""
    expect = "Error on line 3 col 8: ;"
    assert Parser(input).parse() == expect

def test_009():
    input = """
    int fibo(int n) {
        if (n <= 1) return n;
        return fibo(n - 1) + fibo(n - 2);
    }
"""
    print(Tokenizer(input).get_tokens_as_string())
    expect = "success"
    assert Parser(input).parse() == expect

def test_010():
    input = """
    void main () {
        return a++--++--;
        return ++--++--a++--++--;
    }
    """
    expected = "success"
    assert Parser(input).parse() == expected

def test_011():
    input = """
    void main () {
        return 2004;
        return 2.4;
        return "AnTruong";
        return {20,04,2004}; // struct lit
        return {};
    }
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_012():
    input = """
    void main () {
        return {1+3, "s"++};
    }
"""
    expected = "success"
    assert Parser(input).parse() == expected

def test_013():
    input = """
    void main () {
       for(int a = 1 + 2; i > 2; a++) continue;
       for(a = a.b = 1; ; --a) a++;
       for(auto a = 1; i * 2; a = 2) {return ;}
       for(; ; ) {}
       for({1,2}.a = 1; ; (a+2).b = 2) a++;
    }
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_014():
    input = """
void main () {
    ++a = 1;
}
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_015():
    input = """
void main () {
    for(;; -a) continue;
}
"""
    expect = "Error on line 3 col 11: -"
    assert Parser(input).parse() == expect

def test_016():
    input = """
void main() {
    for(;; +a) continue;
}
"""
    expect = "Error on line 3 col 11: +"
    assert Parser(input).parse() == expect

def test_017():
    input = """
    void main () {
        switch (1 *3 / 4) {
            default:
                1;
            case 2:
                 2;
        }
    
        switch (1 *3 / 4) {
            case 3:1;
            default:1;
            case 2: 2;
        }
    }
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_018():
    input = """
    void main () {
       foo().a;
    }
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_019():
    input = """
void main () {
    a.foo();
}
"""
    expected = "Error on line 3 col 9: ("
    assert Parser(input).parse() == expected

def test_020():
    input = """
void main () {
    foo().b = 2;
}
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_021():
    input = """
void main () {
    foo() = 1;
}
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_022():
    input = """
void main () {
    struct {};
}
"""
    expect = "Error on line 3 col 4: struct"
    assert Parser(input).parse() == expect

def test_023():
    input = """
void main () {
    for(int a;;++(a + b)){}
        for(int a;;{a,b}--){}
}
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_024():
    input = """
void main() {
    int a = 5;
    int a = ++ -- a ++ --; 
}
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_025():
    input = """
void main() {
    for(;;++ -- a ++ -- ) {}
}
"""
    expect = "success"
    assert Parser(input).parse() == expect

def test_026():
    input = """
void main () {
    for(;;a.b);
}
"""
    expect = "Error on line 3 col 13: )"
    assert Parser(input).parse() == expect

def test_027():
    input = """
void main () {
    auto x = readInt();
    switch (x) {
        case 1:
        case 2:
        default:
    }
}
"""
    expected = "success"
    assert Parser(input).parse() == expected