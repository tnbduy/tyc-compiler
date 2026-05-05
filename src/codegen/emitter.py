"""
Emitter class for TyC code generation.
High-level code emission with type conversion, constant loading, variable operations.
"""

import os
from typing import List, Optional, Union
from .jasmin_code import JasminCode
from .error import IllegalOperandException
from ..utils.nodes import (
    IntType, FloatType, StringType, VoidType, StructType,
    IntLiteral, FloatLiteral, StringLiteral
)
from .utils import FunctionType, StructType as CodeGenStructType

# Helper functions for TyC type checking
def is_int_type(in_type):
    """Check if type is int."""
    return type(in_type) is IntType

def is_float_type(in_type):
    """Check if type is float."""
    return type(in_type) is FloatType

def is_string_type(in_type):
    """Check if type is string."""
    return type(in_type) is StringType

def is_void_type(in_type):
    """Check if type is void."""
    return type(in_type) is VoidType

def is_struct_type(in_type):
    """Check if type is struct."""
    return type(in_type) is StructType or type(in_type) is CodeGenStructType


class Emitter:
    """
    Emitter class to generate JVM bytecode instructions for TyC.
    
    Attributes:
        filename (str): Name of the output file
        buff (List[str]): Buffer to store generated code
        jvm (JasminCode): JasminCode instance for JVM instruction generation
    """

    def __init__(self, filename: str):
        """
        Initialize Emitter.
        
        Args:
            filename: Name of the output file (.j file)
        """
        self.filename = filename
        self.filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "runtime", filename
        )
        self.buff: List[str] = []
        self.jvm = JasminCode()

    def get_jvm_type(self, in_type) -> str:
        """
        Convert TyC AST type to JVM type descriptor.
        
        Args:
            in_type: AST type to convert
            
        Returns:
            JVM type descriptor string
        """
        # Check for String[] array type (special marker for main method args)
        # Check by class name or type name
        if type(in_type).__name__ == 'StringArrayType' or (hasattr(in_type, '__class__') and 'StringArray' in str(type(in_type))):
            return "[Ljava/lang/String;"  # String[] in JVM
        
        if is_int_type(in_type):
            return "I"
        elif is_float_type(in_type):
            return "F"
        elif is_string_type(in_type):
            return "Ljava/lang/String;"
        elif is_void_type(in_type):
            return "V"
        elif is_struct_type(in_type):
            struct_name = in_type.struct_name if hasattr(in_type, 'struct_name') else in_type.struct_name
            return "L" + struct_name + ";"
        elif type(in_type) is FunctionType:
            return (
                "("
                + "".join(
                    list(map(lambda x: self.get_jvm_type(x), in_type.param_types))
                )
                + ")"
                + self.get_jvm_type(in_type.return_type)
            )
        else:
            raise IllegalOperandException(f"Unknown type: {type(in_type)}")

    def emit_push_iconst(self, in_: Union[int, str], frame) -> str:
        """
        Emit instruction to push integer constant onto operand stack.
        
        Args:
            in_: Integer value or string representation
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.push()
        if type(in_) is int:
            i = in_
            if i >= -1 and i <= 5:
                return self.jvm.emitICONST(i)
            elif i >= -128 and i <= 127:
                return self.jvm.emitBIPUSH(i)
            elif i >= -32768 and i <= 32767:
                return self.jvm.emitSIPUSH(i)
            else:
                return self.jvm.emitLDC(str(i))
        elif type(in_) is str:
            if in_ == "true":
                return self.emit_push_iconst(1, frame)
            elif in_ == "false":
                return self.emit_push_iconst(0, frame)
            else:
                return self.emit_push_iconst(int(in_), frame)

    def emit_push_fconst(self, in_: str, frame) -> str:
        """
        Emit instruction to push float constant onto operand stack.
        
        Args:
            in_: String representation of float value
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        f = float(in_)
        frame.push()
        rst = "{0:.4f}".format(f)
        if rst == "0.0000" or rst == "1.0000" or rst == "2.0000":
            return self.jvm.emitFCONST(rst[:3])
        else:
            return self.jvm.emitLDC(rst)

    def emit_push_const(self, in_: str, typ, frame) -> str:
        """
        Generate code to push a constant onto the operand stack.
        
        Args:
            in_: The lexeme of the constant
            typ: The type of the constant
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
            
        Raises:
            IllegalOperandException: If type is not supported
        """
        if is_int_type(typ):
            return self.emit_push_iconst(in_, frame)
        elif is_string_type(typ):
            frame.push()
            # String literals - in_ already contains the string value (without quotes)
            # For JVM LDC, we need to properly escape the string
            # Escape backslashes and quotes
            escaped = in_.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
            return self.jvm.emitLDC(f'"{escaped}"')
        else:
            raise IllegalOperandException(f"Unsupported constant type: {type(typ)}")

    def emit_var(
        self, in_: int, var_name: str, in_type, from_label: int, to_label: int
    ) -> str:
        """
        Generate the var directive for a local variable.
        
        Args:
            in_: The index of the local variable
            var_name: The name of the local variable
            in_type: The type of the local variable
            from_label: The starting label of the scope where the variable is active
            to_label: The ending label of the scope where the variable is active
            
        Returns:
            Generated var directive string
        """
        return self.jvm.emitVAR(
            in_, var_name, self.get_jvm_type(in_type), from_label, to_label
        )

    def emit_read_var(self, name: str, in_type, index: int, frame) -> str:
        """
        Emit instruction to read local variable.
        
        Args:
            name: Variable name
            in_type: Variable type
            index: Variable index
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
            
        Raises:
            IllegalOperandException: If type is not supported
        """
        frame.push()
        if is_int_type(in_type):
            return self.jvm.emitILOAD(index)
        elif is_float_type(in_type):
            return self.jvm.emitFLOAD(index)
        elif is_string_type(in_type) or is_struct_type(in_type):
            return self.jvm.emitALOAD(index)
        else:
            raise IllegalOperandException(f"Unsupported variable type: {type(in_type)}")

    def emit_write_var(self, name: str, in_type, index: int, frame) -> str:
        """
        Generate code to pop a value on top of the operand stack and store it to a block-scoped variable.
        
        Args:
            name: The symbol entry of the variable
            in_type: Variable type
            index: Variable index
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
            
        Raises:
            IllegalOperandException: If type is not supported
        """
        frame.pop()

        if is_int_type(in_type):
            return self.jvm.emitISTORE(index)
        elif is_float_type(in_type):
            return self.jvm.emitFSTORE(index)
        elif is_string_type(in_type) or is_struct_type(in_type):
            return self.jvm.emitASTORE(index)
        else:
            raise IllegalOperandException(f"Unsupported variable type: {type(in_type)}")

    def emit_get_field(self, lexeme: str, in_, frame) -> str:
        """
        Emit GETFIELD instruction for struct member access.
        
        Args:
            lexeme: Field name (struct_name/member_name)
            in_: Field type
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        # GETFIELD pops object reference, pushes field value
        frame.pop()  # Pop object reference
        frame.push()  # Push field value
        return self.jvm.emitGETFIELD(lexeme, self.get_jvm_type(in_))

    def emit_put_field(self, lexeme: str, in_, frame) -> str:
        """
        Emit PUTFIELD instruction for struct member assignment.
        
        Args:
            lexeme: Field name (struct_name/member_name)
            in_: Field type
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        frame.pop()
        return self.jvm.emitPUTFIELD(lexeme, self.get_jvm_type(in_))

    def emit_invoke_static(self, lexeme: str, in_, frame) -> str:
        """
        Generate code to invoke a static method.
        
        Args:
            lexeme: The qualified name of the method (class-name/method-name)
            in_: The type descriptor of the method
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        typ = in_
        list(map(lambda x: frame.pop(), typ.param_types))
        if not is_void_type(typ.return_type):
            frame.push()
        return self.jvm.emitINVOKESTATIC(lexeme, self.get_jvm_type(in_))

    def emit_neg_op(self, in_, frame) -> str:
        """
        Generate ineg, fneg.
        
        Args:
            in_: The type of the operands
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        if is_int_type(in_):
            return self.jvm.emitINEG()
        else:
            return self.jvm.emitFNEG()

    def emit_add_op(self, lexeme: str, in_, frame) -> str:
        """
        Generate iadd, isub, fadd or fsub.
        
        Args:
            lexeme: The lexeme of the operator
            in_: The type of the operands
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        if lexeme == "+":
            if is_int_type(in_):
                return self.jvm.emitIADD()
            else:
                return self.jvm.emitFADD()
        else:
            if is_int_type(in_):
                return self.jvm.emitISUB()
            else:
                return self.jvm.emitFSUB()

    def emit_mul_op(self, lexeme: str, in_, frame) -> str:
        """
        Generate imul, idiv, fmul or fdiv.
        
        Args:
            lexeme: The lexeme of the operator
            in_: The type of the operands
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        if lexeme == "*":
            if is_int_type(in_):
                return self.jvm.emitIMUL()
            else:
                return self.jvm.emitFMUL()
        else:
            if is_int_type(in_):
                return self.jvm.emitIDIV()
            else:
                return self.jvm.emitFDIV()

    def emit_mod(self, frame) -> str:
        """
        Emit modulo instruction.
        
        Args:
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIREM()

    def emit_and_op(self, frame) -> str:
        """
        Generate iand for logical AND.
        
        Args:
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIAND()

    def emit_or_op(self, frame) -> str:
        """
        Generate ior for logical OR.
        
        Args:
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIOR()

    def emit_re_op(self, op: str, in_, frame) -> str:
        """
        Emit relational operation (returns int: 0 for false, non-zero for true).
        
        Args:
            op: Operator string (==, !=, <, <=, >, >=)
            in_: Type of operands
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        result = list()
        label_f = frame.get_new_label()
        label_o = frame.get_new_label()

        frame.pop()
        frame.pop()
        if is_int_type(in_):
            if op == ">":
                result.append(self.jvm.emitIFICMPLE(label_f))
            elif op == ">=":
                result.append(self.jvm.emitIFICMPLT(label_f))
            elif op == "<":
                result.append(self.jvm.emitIFICMPGE(label_f))
            elif op == "<=":
                result.append(self.jvm.emitIFICMPGT(label_f))
            elif op == "!=":
                result.append(self.jvm.emitIFICMPEQ(label_f))
            else:  # op == "=="
                result.append(self.jvm.emitIFICMPNE(label_f))
        else:  # float
            result.append(self.jvm.emitFCMPL())
            if op == ">":
                result.append(self.jvm.emitIFLE(label_f))
            elif op == ">=":
                result.append(self.jvm.emitIFLT(label_f))
            elif op == "<":
                result.append(self.jvm.emitIFGE(label_f))
            elif op == "<=":
                result.append(self.jvm.emitIFGT(label_f))
            elif op == "!=":
                result.append(self.jvm.emitIFEQ(label_f))
            else:  # op == "=="
                result.append(self.jvm.emitIFNE(label_f))
        
        result.append(self.emit_push_iconst(1, frame))
        result.append(self.emit_goto(label_o, frame))
        result.append(self.emit_label(label_f, frame))
        result.append(self.emit_push_iconst(0, frame))
        result.append(self.emit_label(label_o, frame))
        return "".join(result)

    def emit_method(self, lexeme: str, in_type, is_static: bool) -> str:
        """
        Generate the method directive for a function.
        
        Args:
            lexeme: The name of the method
            in_type: The type descriptor of the method
            is_static: True if the method is static; false otherwise (always True for TyC)
            
        Returns:
            Generated method directive string
        """
        return self.jvm.emitMETHOD(lexeme, self.get_jvm_type(in_type), True)  # All TyC functions are static

    def emit_end_method(self, frame) -> str:
        """
        Generate the end directive for a function.
        
        Args:
            frame: Frame object for stack management
            
        Returns:
            Generated end method directive string
        """
        buffer = list()
        buffer.append(self.jvm.emitLIMITSTACK(frame.get_max_op_stack_size()))
        buffer.append(self.jvm.emitLIMITLOCAL(frame.get_max_index()))
        buffer.append(self.jvm.emitENDMETHOD())
        return "".join(buffer)

    def emit_if_true(self, label: int, frame) -> str:
        """
        Generate code to jump to label if the value on top of operand stack is true (non-zero).
        
        Args:
            label: The label where the execution continues if the value on top of stack is true
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIFGT(label)

    def emit_if_false(self, label: int, frame) -> str:
        """
        Generate code to jump to label if the value on top of operand stack is false (zero).
        
        Args:
            label: The label where the execution continues if the value on top of stack is false
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitIFLE(label)

    def emit_dup(self, frame) -> str:
        """
        Generate code to duplicate the value on the top of the operand stack.
        
        Args:
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.push()
        return self.jvm.emitDUP()

    def emit_dup_x1(self, frame) -> str:
        """
        Generate code to duplicate the value and insert below the second stack entry.
        Stack: [..., value2, value1] -> [..., value1, value2, value1]
        
        Args:
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.push()
        return self.jvm.emitDUPX1()

    def emit_dup_x2(self, frame) -> str:
        """
        Generate code to duplicate the value below two stack entries.
        
        Args:
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.push()
        return self.jvm.emitDUPX2()

    def emit_pop(self, frame) -> str:
        """
        Emit POP instruction.
        
        Args:
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.pop()
        return self.jvm.emitPOP()

    def emit_i2f(self, frame) -> str:
        """
        Generate code to convert an integer on top of stack to a floating-point number.
        
        Args:
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        return self.jvm.emitI2F()

    def emit_return(self, in_, frame) -> str:
        """
        Generate code to return.
        
        Args:
            in_: The type of the returned expression
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        if is_int_type(in_):
            frame.pop()
            return self.jvm.emitIRETURN()
        elif is_float_type(in_):
            frame.pop()
            return self.jvm.emitFRETURN()
        elif is_void_type(in_):
            return self.jvm.emitRETURN()
        elif is_string_type(in_) or is_struct_type(in_):
            frame.pop()
            return self.jvm.emitARETURN()
        else:
            raise IllegalOperandException(f"Unsupported return type: {type(in_)}")

    def emit_new(self, lexeme: str, frame) -> str:
        """
        Emit NEW instruction for creating struct instances.
        
        Args:
            lexeme: Struct name
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        frame.push()
        return self.jvm.emitNEW(lexeme)

    def emit_new_instance(self, class_name: str, frame) -> str:
        """
        Emit code to create a new instance of a class and call its constructor.
        Equivalent to: new ClassName; dup; invokespecial ClassName/<init>()V
        
        After this, the stack has the initialized object reference.
        
        Args:
            class_name: Class name (e.g., "Point")
            frame: Frame object for stack management
            
        Returns:
            Generated JVM instruction string
        """
        code = ""
        # new ClassName - pushes uninitialized object ref
        frame.push()
        code += self.jvm.emitNEW(class_name)
        # dup - duplicate the object ref (one for init, one to keep)
        frame.push()
        code += self.jvm.emitDUP()
        # invokespecial ClassName/<init>()V - consumes one ref
        frame.pop()
        code += self.jvm.emitINVOKESPECIAL(class_name + "/<init>", "()V")
        # Stack now has one initialized object reference
        return code

    def emit_label(self, label: int, frame) -> str:
        """
        Generate code that represents a label.
        
        Args:
            label: The label
            frame: Frame object for stack management
            
        Returns:
            Generated label code
        """
        return self.jvm.emitLABEL(label)

    def emit_goto(self, label: int, frame) -> str:
        """
        Generate code to jump to a label.
        
        Args:
            label: The label
            frame: Frame object for stack management
            
        Returns:
            Generated goto instruction string
        """
        return self.jvm.emitGOTO(label)

    def emit_prolog(self, name: str) -> str:
        """
        Generate starting directives for TyC program (single class with all functions).
        
        Args:
            name: Class name (usually "TyC" or "Main")
            
        Returns:
            Generated prolog directives string
        """
        result = list()
        result.append(self.jvm.emitSOURCE(name + ".java"))
        result.append(self.jvm.emitCLASS("public " + name))
        result.append(self.jvm.emitSUPER("java/lang/Object"))
        return "".join(result)

    def emit_epilog(self) -> None:
        """
        Write generated code to file.
        """
        file = open(self.filepath, "w")
        tmp = "".join(self.buff)
        file.write(tmp)
        file.close()

    def print_out(self, in_: str) -> None:
        """
        Print out the code to screen (add to buffer).
        
        Args:
            in_: The code to be printed out
        """
        self.buff.append(in_)

    def clear_buff(self) -> None:
        """
        Clear the code buffer.
        """
        self.buff.clear()
