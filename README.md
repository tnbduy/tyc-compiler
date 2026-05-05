# TyC Compiler Project

A comprehensive compiler implementation for **TyC**, a simple C-like programming language with complete type inference, using the ANTLR4 parser generator.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![ANTLR](https://img.shields.io/badge/ANTLR-4.13.2-orange.svg)](https://www.antlr.org/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)](LICENSE)

## Overview

This is a mini project for **Principles of Programming Languages** course that implements a compiler for **TyC**, a custom C-like programming language designed for educational purposes.

📋 **For detailed language specification, see [TyC Specification](tyc_specification.md)**

The project demonstrates fundamental concepts of compiler construction including:

- **Lexical Analysis**: Tokenization and error handling for invalid characters, unclosed strings, and illegal escape sequences
- **Syntax Analysis**: Grammar-based parsing using ANTLR4 (ANother Tool for Language Recognition)
- **AST Generation**: Building abstract syntax trees from parse trees
- **Semantic Analysis**: Complete type inference system with static type checking
- **Code Generation**: Generating target code from validated AST
- **Error Handling**: Comprehensive error reporting for all compilation phases
- **Testing Framework**: Automated testing with HTML report generation

---

## Assignment 1 - Lexical Analysis and Syntax Analysis

### Required Tasks to Complete

1. **Read the language specification carefully**

   - Study the detailed [TyC Specification](tyc_specification.md) document
   - Understand the syntax and semantics of the TyC language
   - Master the lexical and syntax rules

2. **Implement the TyC.g4 file**

   - Complete the ANTLR4 grammar file in `src/grammar/TyC.g4`
   - Define lexical rules (tokens)
   - Define parser rules (grammar rules)
   - Handle precedence and associativity

3. **Write 100 lexer tests and 100 parser tests**
   - **100 test cases for lexer** in `tests/test_lexer.py`
     - Test valid and invalid tokens
     - Test error handling (unclosed strings, illegal escape sequences, etc.)
     - Test edge cases and boundary conditions
   - **100 test cases for parser** in `tests/test_parser.py`
     - Test valid grammar structures
     - Test syntax errors and error recovery
     - Test nested structures and complex expressions

### Lexical Error Handling Requirements

For lexical errors, the lexer must return the following tokens with specific lexemes:

- **ERROR_TOKEN** with `<unrecognized char>` lexeme: when the lexer detects an unrecognized character.

- **UNCLOSE_STRING** with `<unclosed string>` lexeme: when the lexer detects an unterminated string. The `<unclosed string>` lexeme does not include the opening quote.

- **ILLEGAL_ESCAPE** with `<wrong string>` lexeme: when the lexer detects an illegal escape in string. The wrong string is from the beginning of the string (without the opening quote) to the illegal escape.

### Evaluation Criteria

- **Grammar Implementation**: Accuracy and completeness of the `TyC.g4` file
- **Test Coverage**: Quantity and quality of test cases (200 tests total)
- **Error Handling**: Capability to handle lexical and syntax errors

---

## Assignment 2 - AST Generation

### Required Tasks to Complete

1. **Study the AST Node Structure**

   - Read carefully all node classes in `src/utils/nodes.py`
   - Understand the AST node hierarchy and their properties
   - Master how different language constructs map to AST nodes

2. **Implement the ASTGeneration Class**

   - Create a class `ASTGeneration` in `src/astgen/ast_generation.py`
   - Inherit from `TyCVisitor` (generated from ANTLR4)
   - Override visitor methods to construct appropriate AST nodes
   - Handle all language constructs defined in the TyC specification

3. **Write AST Generation Test Cases**
   - Implement test cases in `tests/test_ast_gen.py`
   - Test AST generation for all language features
   - Verify correct node types and structure
   - Test edge cases and complex nested structures

### AST Generation Requirements

The `ASTGeneration` class must:

- **Inherit from TyCVisitor**: Use the visitor pattern to traverse parse trees
- **Return AST nodes**: Each visit method should return appropriate node objects from `nodes.py`
- **Handle all constructs**: Support all language features defined in the grammar
- **Maintain structure**: Preserve the logical structure and relationships between language elements

### Evaluation Criteria

- **AST Implementation**: Correctness and completeness of the `ASTGeneration` class
- **Node Usage**: Proper utilization of node classes from `nodes.py`
- **Test Coverage**: Quality and comprehensiveness of AST generation test cases
- **Structure Accuracy**: AST must correctly represent the source program structure

---

## Assignment 3 - Static Semantic Analysis

### Required Tasks to Complete

1. **Study Semantic Constraints and Error Types**
   - Read carefully all semantic rules in `tyc-semantic_constraints_and_errors.md`
   - Understand the comprehensive error detection requirements
   - Master the type inference system and scope management rules

2. **Implement the Static Checker**
   - Implement the class `StaticChecker` in `src/semantics/static_checker.py` (currently a skeleton raising `NotImplementedError`)
   - Inherit from `ASTVisitor` for traversing AST nodes
   - Implement comprehensive semantic analysis for all language features
   - Handle scope management, type inference, type checking, and error detection

3. **Write 100 Static Checker Test Cases**
   - Implement **100 test cases** in `tests/test_checker.py`
   - Test all semantic error types and valid programs
   - Cover edge cases and complex semantic scenarios
   - Verify correct error messages and program validation  
   - For test layout, see `oplang-compiler/tests/test_checker.py` and the `Checker` wrapper in `tests/utils.py`

### Semantic Analysis Requirements

📋 **For detailed semantic constraints, see [Semantic Constraints and Errors](tyc-semantic_constraints_and_errors.md)**

The `StaticChecker` class must:

- **Inherit from ASTVisitor**: Use the visitor pattern to traverse AST nodes
- **Type Inference**: Implement complete type inference system for `auto` variables
- **Scope Management**: Handle global scope (functions, structs) and local scope (variables, parameters)
- **Error Detection**: Detect all 8 error types specified in the semantic constraints document
- **Type Checking**: Verify type compatibility in statements and expressions according to TyC's strict typing rules

### Error Types to Detect

1. **Redeclared** - Variables, functions, structs, or parameters declared multiple times
2. **UndeclaredIdentifier** - Use of variables or parameters that have not been declared
3. **UndeclaredFunction** - Use of functions that have not been declared
4. **UndeclaredStruct** - Use of struct types that have not been declared
5. **TypeCannotBeInferred** - single AST argument ``ctx`` (e.g. full **`AssignExpr`** for `x = y`; other nodes when failure is not on an assignment — see semantic constraints doc)
6. **TypeMismatchInStatement** - Type incompatibilities in statements (if, while, for, return, assignment)
7. **TypeMismatchInExpression** - Type incompatibilities in expressions (operators, function calls, member access)
8. **MustInLoop** - Break/continue statements outside of loop contexts

### Evaluation Criteria

- **Semantic Analysis**: Correctness and completeness of the `StaticChecker` implementation
- **Type Inference**: Accurate type inference for all `auto` variable declarations
- **Error Detection**: Accurate identification of all required error types
- **Test Coverage**: Quality and comprehensiveness of 100 semantic checker test cases

---

## Assignment 4 - Code Generation

### Required Tasks to Complete

1. **Study code generation components**

   - Read `src/codegen/codegen.py`, `src/codegen/emitter.py`, and helper files in `src/codegen/`
   - Understand the runtime support in `src/runtime/io.java` and `src/runtime/jasmin.jar`
   - Understand the output flow: `AST -> .j -> .class -> run on JVM`

2. **Implement code generation**

   - Complete `CodeGenerator` in `src/codegen/codegen.py`
   - Complete `Emitter` in `src/codegen/emitter.py`
   - Generate correct Jasmin code for TyC programs

3. **Write test cases for Assignment 4**

   - Implement **100 test cases** in `tests/test_codegen.py`
   - Cover basic and advanced language constructs
   - Verify output of generated programs

### Code Generation Requirements

The Assignment 4 implementation must:

- **Traverse AST with ASTVisitor** and emit code for declarations, statements, and expressions
- **Generate valid Jasmin code** that can be assembled and executed
- **Support built-in I/O functions** through runtime class `io`
- **Manage stack, local variables, and labels** correctly during code generation

### Evaluation Criteria

- **Code Generation Implementation**: Correctness and completeness of `CodeGenerator` and `Emitter`
- **Runtime Execution**: Generated code assembles and runs correctly on JVM
- **Test Coverage**: Quality and comprehensiveness of code generation test cases
- **Output Correctness**: Program outputs match expected results in tests

---

## Project Structure

```
.
├── Makefile              # Cross-platform build automation
├── run.py                # Main project entrypoint
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── tyc_specification.md  # Language specification
├── tyc-semantic_constraints_and_errors.md  # Semantic constraints (Assignment 3)
├── external/             # External dependencies
│   └── antlr-4.13.2-complete.jar
├── src/                  # Source code
│   ├── astgen/           # AST generation module
│   │   ├── __init__.py   # Package initialization
│   │   └── ast_generation.py # ASTGeneration class implementation
│   ├── grammar/          # Grammar definitions
│   │   ├── TyC.g4        # ANTLR4 grammar specification
│   │   └── lexererr.py   # Custom lexer error classes
│   └── utils/            # Utility modules
│       ├── error_listener.py
│       ├── nodes.py      # AST node class definitions
│       └── visitor.py    # Base visitor classes
│   ├── semantics/        # Semantic analysis (Assignment 3)
│   │   ├── __init__.py
│   │   ├── static_checker.py   # StaticChecker — student implementation
│   │   └── static_error.py     # Semantic error exception classes (predefined)
│   ├── codegen/          # Code generation (Assignment 4)
│   │   ├── codegen.py    # CodeGenerator — student implementation
│   │   ├── emitter.py    # Emitter helpers — student implementation
│   │   ├── frame.py      # Frame management
│   │   ├── jasmin_code.py
│   │   ├── io.py
│   │   ├── utils.py
│   │   └── error.py
│   └── runtime/          # Runtime support for Assignment 4
│       ├── io.java
│       └── jasmin.jar
└── tests/                # Test suite
    ├── test_lexer.py     # Lexer tests
    ├── test_parser.py    # Parser tests
    ├── test_ast_gen.py   # AST generation tests
    ├── test_checker.py   # Semantic analysis tests (Assignment 3)
    ├── test_codegen.py   # Code generation tests (Assignment 4)
    └── utils.py          # Testing utilities (Tokenizer, Parser, ASTGenerator, Checker, CodeGenerator)
```

## Quick Start

### Prerequisites

- **Python 3.12+** (recommended) or Python 3.8+
- **Java Runtime Environment (JRE) 8+** (required for ANTLR4)

### Setup

1. **Clone the repository:**
   ```bash
   cd TyC-compiler
   ```

2. **Check system requirements:**
   ```bash
   python3 run.py check
   ```

3. **Set up the environment:**
   ```bash
   python3 run.py setup
   ```

4. **Activate virtual environment:**
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

5. **Build the compiler:**
   ```bash
   python3 run.py build
   ```

6. **Run tests:**
   ```bash
   python3 run.py test-lexer
   python3 run.py test-parser
   python3 run.py test-ast
   python3 run.py test-checker
   python3 run.py test-codegen
   ```

## Available Commands

- `python3 run.py setup` - Install dependencies and set up environment
- `python3 run.py build` - Compile ANTLR grammar files
- `python3 run.py check` - Verify required tools are installed
- `python3 run.py test-lexer` - Run lexer tests
- `python3 run.py test-parser` - Run parser tests
- `python3 run.py test-ast` - Run AST generation tests
- `python3 run.py test-checker` - Run semantic checker tests (Assignment 3)
- `python3 run.py test-codegen` - Run code generation tests (Assignment 4)
- `python3 run.py clean` - Clean build files

## License

This project is developed for educational purposes as part of the **Principles of Programming Languages** course.

**Author**: MEng. Trần Ngọc Bảo Duy  
**Institution**: Faculty of Computer Science and Engineering, Ho Chi Minh City University of Technology, VNU-HCM
