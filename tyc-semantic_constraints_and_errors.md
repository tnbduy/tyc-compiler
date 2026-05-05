# TyC Programming Language - Semantic Constraints and Error Types
**Static Semantic Analysis Reference**  
**Version 1.0 - January 2026**

## Overview

This document provides a comprehensive reference for all semantic constraints and error types that must be checked by the TyC static semantic analyzer. TyC is a procedural programming language with complete type inference, struct types, and strict type checking where each operator has well-defined type requirements.

## Error Types Summary

The TyC static semantic checker must detect and report the following error types:

1. **Redeclared** - Variables, functions, structs, parameters, or struct members declared multiple times (or a local variable reusing a parameter name in the same function)
2. **UndeclaredIdentifier** - Use of variables or parameters that have not been declared
3. **UndeclaredFunction** - Use of functions that have not been declared
4. **UndeclaredStruct** - Use of struct types that have not been declared
5. **TypeCannotBeInferred** - `auto` without a fixable type; message is `TypeCannotBeInferred(<ctx>)` where `<ctx>` is one AST node (`str` per `src/utils/nodes.py`)
6. **TypeMismatchInStatement** - Type incompatibilities in statements (if, while, for, return, assignment)
7. **TypeMismatchInExpression** - Type incompatibilities in expressions (operators, function calls, member access, struct literals against an expected struct type)
8. **MustInLoop** - Break/continue statements outside of loop contexts

---

## Detailed Error Specifications

### 1. Redeclared Variable/Function/Struct/Parameter/Member

**Rule:** All declarations must be unique within their respective scopes as defined in the TyC specification.

**Exception:** `Redeclared(<kind>, <identifier>)`
- `<kind>`: Type of redeclared entity (`Variable`, `Function`, `Struct`, `Parameter`, `Member`)
- `<identifier>`: Name of the redeclared identifier

**Scope-specific Rules:**
- **Global scope:** Struct names must be unique among all struct declarations, and function names must be unique among all function declarations (no overloading). **Struct type names and function names use separate namespaces:** the same identifier may name both a struct type and a function (e.g. `struct foo { ... };` and `int foo(int x, int y) { ... }` are valid). Context disambiguates—type position in declarations vs. `(` in a call.
- **Function scope:** Parameters belong to the function's scope and are visible throughout the entire function body. Parameter names must be unique within the same parameter list. **You must not declare a local variable with the same name as a parameter anywhere in that function's body**, including inside nested `{ }` blocks; that is reported as `Redeclared(Variable, <name>)` (not shadowing). TyC does not allow inner blocks to shadow an enclosing function's parameters.
- **Local scope (block):** Variables must have unique names within the same block.
- **Shadowing:** Variables in nested blocks may shadow **other local variables** from outer blocks in the same function, subject to the rule above (parameters cannot be shadowed).

**Examples:**
```tyc
// Error: Redeclared Struct in global scope
struct Point {
    int x;
    int y;
};
struct Point {  // Redeclared(Struct, Point)
    int z;
};

// Error: Redeclared Function in global scope
int add(int x, int y) {
    return x + y;
}
int add(int a, int b) {  // Redeclared(Function, add) - no function overloading
    return a + b;
}

// Valid: same identifier for a struct type and a function (separate global namespaces)
struct foo {
    int x;
    int y;
};
int foo(int x, int y) {  // Not Redeclared: struct foo and function foo are distinct
    return x + y;
}

// Error: Redeclared Variable in same block
void main() {
    int count = 10;
    int count = 20;  // Redeclared(Variable, count)
}

// Error: Redeclared Parameter
int calculate(int x, float y, int x) {  // Redeclared(Parameter, x)
    return x + y;
}

// Error: Local variable reuses parameter name (same function; not allowed even in nested blocks)
void func(int x) {
    int x = 10;  // Redeclared(Variable, x)
}

// Error: Duplicate struct member names in the same struct
struct Point {
    int x;
    int x;  // Redeclared(Member, x)
};

// Valid: Shadowing in different scopes
void example() {
    int value = 100;  // Function variable
    
    {
        int value = 200;  // Valid: shadows function variable
        {
            int value = 300;  // Valid: shadows block variable
        }
    }
}

// Valid: Different scopes (no shadowing conflict)
void test() {
    int x = 10;
    {
        int y = 20;  // Valid: different variable name
    }
    int y = 30;  // Valid: y in outer scope doesn't conflict with y in inner scope (different block)
}
```

### 2. Undeclared Identifier

**Rule:** All variables and parameters must be declared before use.

**Exception:** `UndeclaredIdentifier(<identifier>)`

**Identifier Resolution Rules:**
- Identifiers are resolved by searching from innermost scope outward
- Variables must be declared before use within the same or enclosing scope
- A variable's initializer is checked without that variable in scope (see **`tyc_specification.md` § Scope Rules**)
- Parameters are visible throughout the entire function body
- Global variables are not supported in TyC (only function/struct declarations are global)

**Examples:**
```tyc
// Error: Undeclared Variable
void example() {
    int result = undeclaredVar + 10;  // UndeclaredIdentifier(undeclaredVar)
}

// Error: Using variable before declaration in same scope
void test() {
    int x = y + 5;  // UndeclaredIdentifier(y) - y used before declaration
    int y = 10;
}

// Error: Out of scope access
void method1() {
    int localVar = 42;
}

void method2() {
    int value = localVar + 1;  // UndeclaredIdentifier(localVar) - different function scope
}

// Valid: Proper declaration order
void valid() {
    int x = 10;
    int y = x + 5;  // Valid: x is declared before use
}

// Valid: Parameter visible throughout function
int calculate(int x, int y) {
    int result = x + y;  // Valid: parameters x and y are visible
    return result;
}

// Valid: Variable in enclosing scope
void nested() {
    int outer = 10;
    {
        int inner = outer + 5;  // Valid: outer is in enclosing scope
    }
}
```

### 3. Undeclared Function

**Rule:** All functions must be declared before use.

**Exception:** `UndeclaredFunction(<function-name>)`

**Function Declaration Rules:**
- Functions have global scope
- Functions can be called from anywhere after declaration
- Function names must be unique among functions (no function overloading); a function name may match a struct type name
- Built-in functions (`readInt`, `readFloat`, `readString`, `printInt`, `printFloat`, `printString`) are implicitly declared

**Examples:**
```tyc
// Error: Undeclared Function
void main() {
    int result = calculate(5, 3);  // UndeclaredFunction(calculate)
}

// Error: Function called before declaration (if declaration comes later)
void test() {
    int value = add(10, 20);  // UndeclaredFunction(add) - if add is declared later
}

int add(int x, int y) {
    return x + y;
}

// Valid: Function declared before use
int multiply(int x, int y) {
    return x * y;
}

void main() {
    int result = multiply(5, 3);  // Valid: multiply is declared before
}

// Valid: Built-in functions
void example() {
    int x = readInt();        // Valid: built-in function
    printInt(x);              // Valid: built-in function
    float y = readFloat();    // Valid: built-in function
    string s = readString();  // Valid: built-in function
}
```

### 4. Undeclared Struct

**Rule:** All struct types must be declared before use.

**Exception:** `UndeclaredStruct(<struct-name>)`

**Struct Declaration Rules:**
- Structs have global scope
- Struct types can be used throughout the program after declaration
- Struct names must be unique among struct types (may match a function name—separate namespace)
- Struct members cannot use `auto` - only explicit types are allowed
- A member's type cannot be the struct currently being declared (see **`tyc_specification.md` § Struct Type**)

**Examples:**
```tyc
// Error: Undeclared Struct
void main() {
    Point p;  // UndeclaredStruct(Point)
}

struct Point {
    int x;
    int y;
};

// Error: Using struct type before declaration
void test() {
    Person person;  // UndeclaredStruct(Person) - if Person is declared later
}

struct Person {
    string name;
    int age;
};

// Error: Struct member using undeclared struct type
struct Address {
    string street;
    City city;  // UndeclaredStruct(City) - if City is declared later
};

struct City {
    string name;
};

// Valid: Struct declared before use
struct Point {
    int x;
    int y;
};

void main() {
    Point p1;  // Valid: Point is declared before
    Point p2 = {10, 20};  // Valid: Point is declared before
}

// Valid: Struct member using previously declared struct
struct Point {
    int x;
    int y;
};

struct Address {
    string street;
    Point location;  // Valid: Point is declared before
};
```

### 5. Type Cannot Be Inferred

**Rule:** Every `auto` binding must obtain a definite type from initialization or from later use.

**Exception:** `TypeCannotBeInferred(<ctx>)` — `<ctx>` is the AST node the checker attaches to the first unresolved case (`__str__` format in `src/utils/nodes.py`). In practice it is the expression or statement under check (e.g. a binary op, an assignment, a block after locals, a `return`), not a bare variable name.

**Inference:** With init → from the initializer; without init → from first use that fixes the type. Otherwise this error.

**Reporting:** One semantic error per run. Among `TypeCannotBeInferred` failures, the first one hit during the semantic visit is reported. Program-wide ordering (first failure along the visit, not a global sort by error tier) is defined under **Error Detection Priority** in Implementation Guidelines. Snippets below are separate illustrations, not one pasteable program.

```tyc
// Error: neither auto has a known type — cannot use x + y
void example() {
    auto x;
    auto y;
    auto result = x + y;  // TypeCannotBeInferred(BinaryOp(Identifier(x), +, Identifier(y)))
}

// Error: both sides unknown — assignment cannot pick a type
void test() {
    auto x;
    auto y;
    x = y;  // TypeCannotBeInferred(AssignExpr(Identifier(x) = Identifier(y)))
}

// Error: mutual dependency — no literal, parameter, or already-typed operand to anchor inference
void circular() {
    auto a;
    auto b;
    a = b;  // TypeCannotBeInferred(AssignExpr(Identifier(a) = Identifier(b)))
    // (A following `b = a` would be the same class of problem; it is not reported in the same run after the error above.)
}

// Error: both autos unknown — an `int` receiver does not disambiguate operand typings here:
// relational operators yield `int` for any valid numeric operand pair, so the outer type adds little (Rule 2.2.1).
void compare_autos() {
    auto x;
    auto y;
    int result = x < y;  // TypeCannotBeInferred(BinaryOp(Identifier(x), <, Identifier(y)))
}

// Error: declared type of `c` checks the initializer as a whole; it does not infer `a` / `b` inside `a * b` (Rule 2.2.1).
void mixed_decl() {
    auto a;
    auto b;
    int c = a * b;  // TypeCannotBeInferred(BinaryOp(Identifier(a), *, Identifier(b)))
}

// Error: `auto x` is still unknown when typing `x + "hello"` (same message if only `x` is declared)
void string_mix() {
    auto x;
    auto y;  // unused here; failure is reported on the next line’s initializer
    auto result = x + "hello";  // TypeCannotBeInferred(BinaryOp(Identifier(x), +, StringLiteral('hello')))
}

// Error: auto never used — reported when finishing the block (not at the `VarDecl` line alone)
void unused_auto() {
    auto x;
}  // TypeCannotBeInferred(BlockStmt([VarDecl(auto, x)]))

// Error: return uses an auto that still has no type (inferred-return function; needs `void main()` in full program)
func() {
    auto x;
    return x;  // TypeCannotBeInferred(ReturnStmt(return Identifier(x)))
}
void main() {}

// Valid: auto with initialization
void valid1() {
    auto x = 10;         // Valid: type inferred as int from literal
    auto y = 3.14;       // Valid: type inferred as float from literal
    auto msg = "hello";  // Valid: type inferred as string from literal
}

// Valid: auto without initialization - type inferred from first assignment
void valid2() {
    auto a;
    a = 10;        // Valid: type inferred as int from assignment (first usage)

    auto b;
    b = 3.14;      // Valid: type inferred as float from assignment (first usage)
}

// Valid: auto without initialization - type inferred from first usage in expression
void valid3() {
    auto x;
    x = readInt();  // Valid: type inferred as int from function return type (first usage)

    auto y;
    int temp = 10;
    y = temp + 5;   // Valid: type inferred as int from expression (first usage)
}

// Valid: one unknown auto + integer literal — deterministic tie-break (see spec Rule 2.2.1)
void valid4() {
    auto value;
    auto result = value + 5;  // Valid: value fixed as int (not the only typing compatible with `+`,
                              // but TyC pins an unknown numeric `auto` to int when the other operand is an integer literal)
}

// Valid: auto with initialization from expression (operands already typed)
void valid5() {
    int a = 10;
    float b = 3.14;
    auto sum = a + b;  // Valid: type inferred as float from expression
}

// Valid: whole argument is one `auto` identifier — parameter type fixes `x` (contrast `f(x + y)` with two unknowns)
void valid6() {
    auto x;
    printInt(x);  // Valid: type inferred as int from printInt(int) parameter type
}
```

### 6. Type Mismatch In Statement

**Rule:** All statements must conform to TyC's type rules.

**Exception:** `TypeMismatchInStatement(<statement>)`

**Statement Type Rules:**

**Conditional Statements (if, while, for):**
- If/while/for condition expression must evaluate to `int` type (0 is false, non-zero is true)

**For Statement:**
- `<init>`, `<condition>`, `<update>` follow their respective type rules
- Condition must evaluate to `int` type

**Assignment Statements (`ExprStmt` with `AssignExpr`):**
- Left-hand side and right-hand side must have the same type
- Struct assignment: both sides must be the same struct type
- A struct literal on the right-hand side that fails arity or per-member checks against the expected struct type is **`TypeMismatchInExpression`** on that literal, not **`TypeMismatchInStatement`** for that failure alone (see **Struct literal**)
- No type coercion in assignments (unlike some languages)

**Assignment Expression Behavior:**
- Assignment can be used as an expression (not just a statement)
- Assignment expression is right-associative: `x = y = z = 10;` is parsed as `x = (y = (z = 10));`
- Assignment expression returns the value of the left-hand side after assignment
- Type of assignment expression is the type of the left-hand side
- Left-hand side must be an identifier or a member access expression (cannot be a literal or other expression)
- Assignment expression can be used in expression contexts: `int y = (x = 5) + 7;` is valid

**Return Statements:**
- Return expression must match function return type (if function returns non-void)
- If function return type is `void`, `return;` (without expression) must be used
- If function return type is non-void, `return <expression>;` must return a value of that type
- For functions with inferred return type, the return type is inferred from the first return statement that returns a value. All subsequent return statements must return a value of the inferred type - if a return statement returns a value of a different type, it is a TypeMismatchInStatement error

**Switch Statements:**
- Switch expression must evaluate to `int` type
- Case labels must be integer literals or constant expressions evaluating to `int`

**Examples:**
```tyc
// Error: Non-int condition in if statement
void conditionalError() {
    float x = 5.0;
    if (x) {  // Error: TypeMismatchInStatement at if statement
        printInt(1);
    }
    
    string message = "hello";
    if (message) {  // Error: TypeMismatchInStatement at if statement
        printString(message);
    }
}

// Error: Non-int condition in while statement
void whileError() {
    float f = 1.5;
    while (f) {  // Error: TypeMismatchInStatement at while statement
        printFloat(f);
    }
}

// Error: Assignment type mismatch
void assignmentError() {
    int x = 10;
    string text = "hello";
    float f = 3.14;
    
    x = text;    // Error: TypeMismatchInStatement at assignment
    text = x;    // Error: TypeMismatchInStatement at assignment
    f = x;       // Error: TypeMismatchInStatement at assignment (no int to float coercion in assignment)
}

// Error: Struct assignment type mismatch
struct Point {
    int x;
    int y;
};

struct Person {
    string name;
    int age;
};

void structError() {
    Point p;
    Person person;
    p = person;  // Error: TypeMismatchInStatement at assignment
}

// Error: Return type mismatch
int getValue() {
    return "invalid";  // Error: TypeMismatchInStatement at return statement
}

string getText() {
    return 42;  // Error: TypeMismatchInStatement at return statement
}

void returnError() {
    return 10;  // Error: TypeMismatchInStatement at return statement (void function cannot return value)
}

int returnVoidError() {
    return;  // Error: TypeMismatchInStatement at return statement (non-void function must return value)
}

// Error: Switch expression type mismatch
void switchError() {
    float f = 3.14;
    switch (f) {  // Error: TypeMismatchInStatement at switch statement
        case 1: break;
    }
}

// Valid: Proper type matching
void valid() {
    int x = 10;
    int y = 20;
    if (x < y) {  // Valid: condition is int
        x = y;    // Valid: both sides are int
    }
    
    Point p1 = {10, 20};
    Point p2 = {30, 40};
    p1 = p2;      // Valid: both sides are Point
}

// Valid: Assignment expression in expression context
void assignmentExpressionValid() {
    int x;
    int y = (x = 5) + 7;  // Valid: assignment expression returns value of x (after assignment)
    // y = 12, x = 5
    
    int a, b, c;
    a = b = c = 10;  // Valid: right-associative chained assignment
    // All a, b, c are 10
    
    struct Point {
        int x;
        int y;
    };
    Point p;
    int result = (p.x = 5) + 3;  // Valid: member access assignment expression
    // result = 8, p.x = 5
}
```

### 7. Type Mismatch In Expression

**Rule:** All expressions must conform to TyC's type rules for operators and operations.

**Exception:** `TypeMismatchInExpression(<expression>)`

**Expression Type Rules:**

**Binary Arithmetic Operators (`+`, `-`, `*`, `/`):**
- Both operands must be `int` or `float`
- Result type: `int` if both operands are `int`, otherwise `float`

**Modulus Operator (`%`):**
- Both operands must be `int`
- Result type: `int`

**Relational Operators (`==`, `!=`, `<`, `<=`, `>`, `>=`):**
- Both operands must be `int` or `float`
- Result type: `int` (0 for false, non-zero for true)

**Logical Operators (`&&`, `||`):**
- Both operands must be `int`
- Result type: `int`

**Logical NOT Operator (`!`):**
- Operand must be `int`
- Result type: `int`

**Increment/Decrement Operators (`++`, `--`):**
- Operand must be `int` (prefix or postfix)
- Operand must be a variable identifier or a member access expression (cannot be a literal or other expression)
- Result type: `int`

**Member Access Operator (`.`):**
- Left operand must be a struct type
- Right operand must be a member name of that struct type
- Result type: type of the struct member

**Function Call:**
- Number of arguments must match number of parameters
- Argument types must match parameter types (no type coercion)
- Result type: return type of the function

**Struct literal:**
- When a context supplies an expected struct type, the literal must have the same number of fields as the struct, and each field expression’s type must equal the corresponding member’s type (no coercion between distinct primitive types)
- **Exception:** `TypeMismatchInExpression(<StructLiteral>)` — `<StructLiteral>` is the full struct literal node

**Assignment Expression:**
- Left-hand side must be an identifier or a member access expression (cannot be a literal or other expression)
- Left-hand side and right-hand side must have the same type
- Result type: type of the left-hand side (after assignment)
- Assignment expression returns the value of the left-hand side after assignment
- Can be used in expression contexts (e.g., `int y = (x = 5) + 7;`)
- Right-associative: `x = y = z = 10;` is parsed as `x = (y = (z = 10));`

**Examples:**
```tyc
// Error: Arithmetic operation type mismatch
void arithmeticError() {
    int x = 5;
    string text = "hello";
    
    int sum = x + text;     // Error: TypeMismatchInExpression at binary operation
    float result = x * text; // Error: TypeMismatchInExpression at binary operation
}

// Error: Modulus with non-int operands
void modulusError() {
    float f = 3.14;
    int x = 10;
    
    int result = f % x;      // Error: TypeMismatchInExpression at binary operation (float % int)
    int result2 = x % f;     // Error: TypeMismatchInExpression at binary operation (int % float)
}

// Error: Relational operation type mismatch
void relationalError() {
    int x = 10;
    string text = "hello";
    
    int result = x < text;   // Error: TypeMismatchInExpression at binary operation
    int equal = text == x;   // Error: TypeMismatchInExpression at binary operation
}

// Error: Logical operation type mismatch
void logicalError() {
    float f = 3.14;
    int x = 10;
    
    int result = f && x;     // Error: TypeMismatchInExpression at binary operation
    int not = !f;            // Error: TypeMismatchInExpression at unary operation
}

// Error: Increment/decrement on non-int
void incrementError() {
    float f = 3.14;
    ++f;                     // Error: TypeMismatchInExpression at unary operation
    f++;                     // Error: TypeMismatchInExpression at postfix operation
}

// Error: Increment/decrement on literal or expression
void incrementOperandError() {
    int x = 5;
    ++5;                     // Error: TypeMismatchInExpression at unary operation (cannot increment literal)
    --(x + 1);               // Error: TypeMismatchInExpression at unary operation (cannot increment expression)
    (x + 2)++;               // Error: TypeMismatchInExpression at postfix operation (cannot increment expression)
}

// Error: Member access on non-struct
void memberAccessError() {
    int x = 10;
    int value = x.member;    // Error: TypeMismatchInExpression at member access
    
    struct Point {
        int x;
        int y;
    };
    
    Point p = {10, 20};
    int invalid = p.z;       // Error: TypeMismatchInExpression at member access (z doesn't exist)
}

// Error: Function call argument type mismatch
void process(int x) { }

void callError() {
    string text = "123";
    process(text);           // Error: TypeMismatchInExpression at function call
}

int add(int x, int y) {
    return x + y;
}

void callArgumentError() {
    int result = add(10);    // Error: TypeMismatchInExpression at function call (wrong number of arguments)
    int result2 = add(10, 20, 30);  // Error: TypeMismatchInExpression at function call (wrong number of arguments)
}

// Error: Assignment expression type mismatch
void assignmentExpressionError() {
    int x = 10;
    string text = "hello";
    float f = 3.14;
    
    int result = (x = text) + 5;     // Error: TypeMismatchInExpression at assignment expression (int = string)
    int value = (x = f) + 3;         // Error: TypeMismatchInExpression at assignment expression (int = float)
}

// Error: Assignment expression with invalid left-hand side
void assignmentLeftHandSideError() {
    int x = 5;
    int y = (5 = x) + 3;             // Error: TypeMismatchInExpression at assignment expression (cannot assign to literal)
    int z = ((x + 1) = 10) + 2;      // Error: TypeMismatchInExpression at assignment expression (cannot assign to expression)
}

// Valid: Proper expression types
void valid() {
    int x = 10, y = 20;
    int sum = x + y;         // Valid: both int
    int compare = x < y;     // Valid: relational returns int
    int logic = x && y;      // Valid: logical returns int
    ++x;                     // Valid: increment on int
    
    struct Point {
        int x;
        int y;
    };
    
    Point p = {10, 20};
    int x_coord = p.x;       // Valid: member access
    
    // Valid: Assignment expression in expression context
    int a;
    int b = (a = 5) + 7;      // Valid: assignment expression returns value of a (5), b = 12
    
    // Valid: Chained assignment expression
    int c, d, e;
    c = d = e = 10;          // Valid: right-associative, all variables are 10
    
    // Valid: Member access assignment expression
    int result = (p.x = 15) + 5;  // Valid: assignment expression returns value of p.x (15), result = 20
}
```

### 8. Break/Continue Not In Loop

**Rule:** Break and continue statements must be inside a loop (for or while).

**Exception:** `MustInLoop(<statement>)`

**Loop Context Rules:**
- Break and continue are only valid inside `for` or `while` loops
- Break can also be used in `switch` statements (but continue cannot)
- Can be nested inside conditionals within loops
- Cannot cross function boundaries
- Must be in the lexical scope of a loop

**Examples:**
```tyc
// Error: Break/continue outside loop
void loopError() {
    break;     // Error: MustInLoop(break)
    continue;  // Error: MustInLoop(continue)
}

// Error: Break/continue in if without loop
void conditionalError() {
    if (1) {
        break;     // Error: MustInLoop(break)
        continue;  // Error: MustInLoop(continue)
    }
}

// Error: Continue in switch (continue not allowed in switch)
void switchError() {
    int x = 1;
    switch (x) {
        case 1:
            continue;  // Error: MustInLoop(continue) - continue not allowed in switch
            break;
    }
}

// Error: Break/continue in function called from loop
void helperMethod() {
    break;     // Error: MustInLoop(break) - different function scope
    continue;  // Error: MustInLoop(continue)
}

void loopWithCall() {
    for (auto i = 0; i < 10; ++i) {
        helperMethod();  // Method call doesn't transfer loop context
    }
}

// Valid: Break/continue in loops
void validLoops() {
    for (auto i = 0; i < 10; ++i) {
        if (i == 5) {
            break;     // Valid: in for loop
        }
        if (i % 2 == 0) {
            continue;  // Valid: in for loop
        }
        printInt(i);
    }
    
    auto j = 0;
    while (j < 10) {
        if (j == 3) {
            continue;  // Valid: in while loop
        }
        if (j == 8) {
            break;     // Valid: in while loop
        }
        printInt(j);
        ++j;
    }
}

// Valid: Break in switch
void validSwitch() {
    int day = 2;
    switch (day) {
        case 1:
            printInt(1);
            break;     // Valid: break in switch
        case 2:
        case 3:
            printInt(2);
            break;     // Valid: break in switch
        default:
            printInt(0);
    }
}

// Valid: Nested loops
void nestedLoops() {
    for (auto i = 0; i < 5; ++i) {
        for (auto j = 0; j < 5; ++j) {
            if (i == j) {
                continue;  // Valid: affects inner loop
            }
            if (j > 3) {
                break;     // Valid: breaks inner loop
            }
        }
    }
}
```

---

## Implementation Guidelines

### Error Detection Priority

**Single-pass, first failure wins (program-wide).** The checker performs one semantic **visit** over the program (typical depth-first walk). The **only** error reported is the **first** semantic failure encountered along that visit. The implementation may still use extra internal passes or deferred checks (e.g. for inferred return types) as long as **reporting** stays “first failure along the chosen visit order.” **Tier numbers do not promote a later failure ahead of an earlier one:** the visit is not extended to discover all failures and then choose by smallest tier. The tiers below classify error **kinds** and define **tie-breaking within the same tier**; they do not impose a global priority queue over the whole program.

**Error tiers** (for documentation and same-tier ties):

1. **Declaration errors** (Redeclared, UndeclaredIdentifier, UndeclaredFunction, UndeclaredStruct)
2. **Type inference errors** (`TypeCannotBeInferred`; see section 5)
3. **Type errors** (TypeMismatchInStatement, TypeMismatchInExpression)
4. **Control flow errors** (MustInLoop)

**Within one tier:** if more than one failure in that tier would arise before the checker stops, report the **first** in visit order (order depends on how constructs are checked, not on source left-to-right alone).

**One** error per run.

### Scope Management

Lexical scope (blocks, shadowing, and `for` init vs. loop body) is defined normatively in **`tyc_specification.md` § Scope Rules**. The checker should follow that model; the Redeclared / UndeclaredIdentifier rules in this document are consequences of it.

- **Global scope:** Functions and structs (names are unique within each kind; struct names and function names may coincide—see Redeclared rules above). Global binding does not override **declared-before-use** for calls and struct-type uses (sections 3–4); align with **`tyc_specification.md` § Scope Rules, Global Scope**.
- **Function scope:** Parameters (visible throughout function body; see Redeclared rules—locals may not reuse parameter names)
- **Local scope (block):** Variables declared in blocks `{}`
- **Nested scopes:** Inner scopes can shadow outer local variables (not parameters of the enclosing function)

### Type Inference System

TyC uses complete type inference with the following rules:

1. **Literals:** int / float / string as usual
2. **`auto`:** From initializer if present; else from first constraining use
3. **Failure:** Ambiguous or unused `auto` → `TypeCannotBeInferred(<ctx>)` (see section 5)
4. **Expressions:** Operator/operand rules apply once types are known
5. **Function returns:** Explicit or inferred from the function's return statements as a whole (specification Rule 5), not necessarily from a single strict top-to-bottom pass

### Type System Rules

- **Strict typing:** No implicit type coercion except in arithmetic operations (int + float → float)
- **No function overloading:** Function names must be unique among functions (struct and function names may coincide)
- **Struct types:** Must be explicitly declared before use
- **Void type:** Only used as function return type, not for variables or parameters

### Built-in Functions

The following built-in functions are implicitly declared and available:
- `int readInt()`
- `float readFloat()`
- `string readString()`
- `void printInt(int value)`
- `void printFloat(float value)`
- `void printString(string value)`

### Entry Point

A TyC program must have at least one function named `main` that takes no parameters and returns `void`. This serves as the program entry point.

---

*Document prepared for TyC Static Semantic Analysis*  
*Last updated: April 2026*
