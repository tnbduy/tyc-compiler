"""
Low-level Jasmin instruction generation.
"""

from abc import ABC, abstractmethod
from .error import IllegalOperandException


class MachineCode(ABC):
    @abstractmethod
    def emitPUSHNULL(self):
        pass

    @abstractmethod
    def emitICONST(self, i):
        pass

    @abstractmethod
    def emitBIPUSH(self, i):
        pass

    @abstractmethod
    def emitSIPUSH(self, i):
        pass

    @abstractmethod
    def emitLDC(self, in_):
        pass

    @abstractmethod
    def emitFCONST(self, i):
        pass

    @abstractmethod
    def emitILOAD(self, in_):
        pass

    @abstractmethod
    def emitFLOAD(self, in_):
        pass

    @abstractmethod
    def emitISTORE(self, in_):
        pass

    @abstractmethod
    def emitFSTORE(self, in_):
        pass

    @abstractmethod
    def emitALOAD(self, in_):
        pass

    @abstractmethod
    def emitASTORE(self, in_):
        pass

    @abstractmethod
    def emitIASTORE(self):
        pass

    @abstractmethod
    def emitFASTORE(self):
        pass

    @abstractmethod
    def emitAASTORE(self):
        pass

    @abstractmethod
    def emitIALOAD(self):
        pass

    @abstractmethod
    def emitFALOAD(self):
        pass

    @abstractmethod
    def emitAALOAD(self):
        pass

    @abstractmethod
    def emitGETSTATIC(self, lexeme, typ):
        pass

    @abstractmethod
    def emitPUTSTATIC(self, lexeme, typ):
        pass

    @abstractmethod
    def emitGETFIELD(self, lexeme, typ):
        pass

    @abstractmethod
    def emitPUTFIELD(self, lexeme, typ):
        pass

    @abstractmethod
    def emitIADD(self):
        pass

    @abstractmethod
    def emitFADD(self):
        pass

    @abstractmethod
    def emitISUB(self):
        pass

    @abstractmethod
    def emitFSUB(self):
        pass

    @abstractmethod
    def emitIMUL(self):
        pass

    @abstractmethod
    def emitFMUL(self):
        pass

    @abstractmethod
    def emitIDIV(self):
        pass

    @abstractmethod
    def emitFDIV(self):
        pass

    @abstractmethod
    def emitIAND(self):
        pass

    @abstractmethod
    def emitIOR(self):
        pass

    @abstractmethod
    def emitIREM(self):
        pass

    @abstractmethod
    def emitIFACMPEQ(self, label):
        pass

    @abstractmethod
    def emitIFACMPNE(self, label):
        pass

    @abstractmethod
    def emitIFICMPEQ(self, label):
        pass

    @abstractmethod
    def emitIFICMPNE(self, label):
        pass

    @abstractmethod
    def emitIFICMPLT(self, label):
        pass

    @abstractmethod
    def emitIFICMPLE(self, label):
        pass

    @abstractmethod
    def emitIFICMPGT(self, label):
        pass

    @abstractmethod
    def emitIFICMPGE(self, label):
        pass

    @abstractmethod
    def emitIFEQ(self, label):
        pass

    @abstractmethod
    def emitIFNE(self, label):
        pass

    @abstractmethod
    def emitIFLT(self, label):
        pass

    @abstractmethod
    def emitIFLE(self, label):
        pass

    @abstractmethod
    def emitIFGT(self, label):
        pass

    @abstractmethod
    def emitIFGE(self, label):
        pass

    @abstractmethod
    def emitLABEL(self, label):
        pass

    @abstractmethod
    def emitGOTO(self, label):
        pass

    @abstractmethod
    def emitINEG(self):
        pass

    @abstractmethod
    def emitFNEG(self):
        pass

    @abstractmethod
    def emitDUP(self):
        pass

    @abstractmethod
    def emitDUPX1(self):
        pass

    @abstractmethod
    def emitDUPX2(self):
        pass

    @abstractmethod
    def emitPOP(self):
        pass

    @abstractmethod
    def emitI2F(self):
        pass

    @abstractmethod
    def emitNEW(self, lexeme):
        pass

    @abstractmethod
    def emitNEWARRAY(self, lexeme):
        pass

    @abstractmethod
    def emitANEWARRAY(self, lexeme):
        pass

    @abstractmethod
    def emitINVOKESTATIC(self, lexeme, typ):
        pass

    @abstractmethod
    def emitINVOKESPECIAL(self, lexeme=None, typ=None):
        pass

    @abstractmethod
    def emitINVOKEVIRTUAL(self, lexeme, typ):
        pass

    @abstractmethod
    def emitLIMITSTACK(self, in_):
        pass

    @abstractmethod
    def emitFCMPL(self):
        pass

    @abstractmethod
    def emitLIMITLOCAL(self, in_):
        pass

    @abstractmethod
    def emitVAR(self, in_, varName, inType, fromLabel, toLabel):
        pass

    @abstractmethod
    def emitMETHOD(self, lexeme, typ, isStatic):
        pass

    @abstractmethod
    def emitENDMETHOD(self):
        pass

    @abstractmethod
    def emitSOURCE(self, lexeme):
        pass

    @abstractmethod
    def emitCLASS(self, lexeme):
        pass

    @abstractmethod
    def emitSUPER(self, lexeme):
        pass

    @abstractmethod
    def emitRETURN(self):
        pass

    @abstractmethod
    def emitIRETURN(self):
        pass

    @abstractmethod
    def emitFRETURN(self):
        pass

    @abstractmethod
    def emitARETURN(self):
        pass


class JasminCode(MachineCode):
    END = "\n"
    INDENT = "\t"

    def emitPUSHNULL(self):
        return JasminCode.INDENT + "aconst_null" + JasminCode.END

    def emitICONST(self, i):
        if i == -1:
            return JasminCode.INDENT + "iconst_m1" + JasminCode.END
        elif i >= 0 and i <= 5:
            return JasminCode.INDENT + "iconst_" + str(i) + JasminCode.END
        else:
            raise IllegalOperandException(str(i))

    def emitBIPUSH(self, i):
        if (i >= -128 and i < -1) or (i > 5 and i <= 127):
            return JasminCode.INDENT + "bipush " + str(i) + JasminCode.END
        else:
            raise IllegalOperandException(str(i))

    def emitSIPUSH(self, i):
        if (i >= -32768 and i < -128) or (i > 127 and i <= 32767):
            return JasminCode.INDENT + "sipush " + str(i) + JasminCode.END
        else:
            raise IllegalOperandException(str(i))

    def emitLDC(self, in_):
        return JasminCode.INDENT + "ldc " + in_ + JasminCode.END

    def emitFCONST(self, i):
        if i == "0.0":
            return JasminCode.INDENT + "fconst_0" + JasminCode.END
        elif i == "1.0":
            return JasminCode.INDENT + "fconst_1" + JasminCode.END
        elif i == "2.0":
            return JasminCode.INDENT + "fconst_2" + JasminCode.END
        else:
            raise IllegalOperandException(i)

    def emitILOAD(self, in_):
        if in_ >= 0 and in_ <= 3:
            return JasminCode.INDENT + "iload_" + str(in_) + JasminCode.END
        else:
            return JasminCode.INDENT + "iload " + str(in_) + JasminCode.END

    def emitFLOAD(self, in_):
        if in_ >= 0 and in_ <= 3:
            return JasminCode.INDENT + "fload_" + str(in_) + JasminCode.END
        else:
            return JasminCode.INDENT + "fload " + str(in_) + JasminCode.END

    def emitISTORE(self, in_):
        if in_ >= 0 and in_ <= 3:
            return JasminCode.INDENT + "istore_" + str(in_) + JasminCode.END
        else:
            return JasminCode.INDENT + "istore " + str(in_) + JasminCode.END

    def emitFSTORE(self, in_):
        if in_ >= 0 and in_ <= 3:
            return JasminCode.INDENT + "fstore_" + str(in_) + JasminCode.END
        else:
            return JasminCode.INDENT + "fstore " + str(in_) + JasminCode.END

    def emitALOAD(self, in_):
        if in_ >= 0 and in_ <= 3:
            return JasminCode.INDENT + "aload_" + str(in_) + JasminCode.END
        else:
            return JasminCode.INDENT + "aload " + str(in_) + JasminCode.END

    def emitASTORE(self, in_):
        if in_ >= 0 and in_ <= 3:
            return JasminCode.INDENT + "astore_" + str(in_) + JasminCode.END
        else:
            return JasminCode.INDENT + "astore " + str(in_) + JasminCode.END

    def emitIASTORE(self):
        return JasminCode.INDENT + "iastore" + JasminCode.END

    def emitFASTORE(self):
        return JasminCode.INDENT + "fastore" + JasminCode.END

    def emitAASTORE(self):
        return JasminCode.INDENT + "aastore" + JasminCode.END

    def emitIALOAD(self):
        return JasminCode.INDENT + "iaload" + JasminCode.END

    def emitFALOAD(self):
        return JasminCode.INDENT + "faload" + JasminCode.END

    def emitAALOAD(self):
        return JasminCode.INDENT + "aaload" + JasminCode.END

    def emitGETSTATIC(self, lexeme, typ):
        return JasminCode.INDENT + "getstatic " + lexeme + " " + typ + JasminCode.END

    def emitPUTSTATIC(self, lexeme, typ):
        return JasminCode.INDENT + "putstatic " + lexeme + " " + typ + JasminCode.END

    def emitGETFIELD(self, lexeme, typ):
        return JasminCode.INDENT + "getfield " + lexeme + " " + typ + JasminCode.END

    def emitPUTFIELD(self, lexeme, typ):
        return JasminCode.INDENT + "putfield " + lexeme + " " + typ + JasminCode.END

    def emitIADD(self):
        return JasminCode.INDENT + "iadd" + JasminCode.END

    def emitFADD(self):
        return JasminCode.INDENT + "fadd" + JasminCode.END

    def emitISUB(self):
        return JasminCode.INDENT + "isub" + JasminCode.END

    def emitFSUB(self):
        return JasminCode.INDENT + "fsub" + JasminCode.END

    def emitIMUL(self):
        return JasminCode.INDENT + "imul" + JasminCode.END

    def emitFMUL(self):
        return JasminCode.INDENT + "fmul" + JasminCode.END

    def emitIDIV(self):
        return JasminCode.INDENT + "idiv" + JasminCode.END

    def emitFDIV(self):
        return JasminCode.INDENT + "fdiv" + JasminCode.END

    def emitIAND(self):
        return JasminCode.INDENT + "iand" + JasminCode.END

    def emitIOR(self):
        return JasminCode.INDENT + "ior" + JasminCode.END

    def emitIREM(self):
        return JasminCode.INDENT + "irem" + JasminCode.END

    def emitIFACMPEQ(self, label):
        return JasminCode.INDENT + "if_acmpeq Label" + str(label) + JasminCode.END

    def emitIFACMPNE(self, label):
        return JasminCode.INDENT + "if_acmpne Label" + str(label) + JasminCode.END

    def emitIFICMPEQ(self, label):
        return JasminCode.INDENT + "if_icmpeq Label" + str(label) + JasminCode.END

    def emitIFICMPNE(self, label):
        return JasminCode.INDENT + "if_icmpne Label" + str(label) + JasminCode.END

    def emitIFICMPLT(self, label):
        return JasminCode.INDENT + "if_icmplt Label" + str(label) + JasminCode.END

    def emitIFICMPLE(self, label):
        return JasminCode.INDENT + "if_icmple Label" + str(label) + JasminCode.END

    def emitIFICMPGT(self, label):
        return JasminCode.INDENT + "if_icmpgt Label" + str(label) + JasminCode.END

    def emitIFICMPGE(self, label):
        return JasminCode.INDENT + "if_icmpge Label" + str(label) + JasminCode.END

    def emitIFEQ(self, label):
        return JasminCode.INDENT + "ifeq Label" + str(label) + JasminCode.END

    def emitIFNE(self, label):
        return JasminCode.INDENT + "ifne Label" + str(label) + JasminCode.END

    def emitIFLT(self, label):
        return JasminCode.INDENT + "iflt Label" + str(label) + JasminCode.END

    def emitIFLE(self, label):
        return JasminCode.INDENT + "ifle Label" + str(label) + JasminCode.END

    def emitIFGT(self, label):
        return JasminCode.INDENT + "ifgt Label" + str(label) + JasminCode.END

    def emitIFGE(self, label):
        return JasminCode.INDENT + "ifge Label" + str(label) + JasminCode.END

    def emitLABEL(self, label):
        return "Label" + str(label) + ":" + JasminCode.END

    def emitGOTO(self, label):
        return JasminCode.INDENT + "goto Label" + str(label) + JasminCode.END

    def emitINEG(self):
        return JasminCode.INDENT + "ineg" + JasminCode.END

    def emitFNEG(self):
        return JasminCode.INDENT + "fneg" + JasminCode.END

    def emitDUP(self):
        return JasminCode.INDENT + "dup" + JasminCode.END

    def emitDUPX1(self):
        return JasminCode.INDENT + "dup_x1" + JasminCode.END

    def emitDUPX2(self):
        return JasminCode.INDENT + "dup_x2" + JasminCode.END

    def emitPOP(self):
        return JasminCode.INDENT + "pop" + JasminCode.END

    def emitI2F(self):
        return JasminCode.INDENT + "i2f" + JasminCode.END

    def emitNEW(self, lexeme):
        return JasminCode.INDENT + "new " + lexeme + JasminCode.END

    def emitNEWARRAY(self, lexeme):
        return JasminCode.INDENT + "newarray " + lexeme + JasminCode.END

    def emitANEWARRAY(self, lexeme):
        return JasminCode.INDENT + "anewarray " + lexeme + JasminCode.END

    def emitINVOKESTATIC(self, lexeme, typ):
        return JasminCode.INDENT + "invokestatic " + lexeme + typ + JasminCode.END

    def emitINVOKESPECIAL(self, lexeme=None, typ=None):
        if lexeme is None and typ is None:
            return (
                JasminCode.INDENT
                + "invokespecial java/lang/Object/<init>()V"
                + JasminCode.END
            )
        elif lexeme is not None and typ is not None:
            return JasminCode.INDENT + "invokespecial " + lexeme + typ + JasminCode.END

    def emitINVOKEVIRTUAL(self, lexeme, typ):
        return JasminCode.INDENT + "invokevirtual " + lexeme + typ + JasminCode.END

    def emitLIMITSTACK(self, in_):
        return ".limit stack " + str(in_) + JasminCode.END

    def emitFCMPL(self):
        return JasminCode.INDENT + "fcmpl" + JasminCode.END

    def emitLIMITLOCAL(self, in_):
        return ".limit locals " + str(in_) + JasminCode.END

    def emitVAR(self, in_, varName, inType, fromLabel, toLabel):
        return (
            ".var "
            + str(in_)
            + " is "
            + varName
            + " "
            + inType
            + " from Label"
            + str(fromLabel)
            + " to Label"
            + str(toLabel)
            + JasminCode.END
        )

    def emitMETHOD(self, lexeme, typ, isStatic):
        if isStatic:
            return (
                JasminCode.END
                + ".method public static "
                + lexeme
                + typ
                + JasminCode.END
            )
        else:
            return JasminCode.END + ".method public " + lexeme + typ + JasminCode.END

    def emitENDMETHOD(self):
        return ".end method" + JasminCode.END

    def emitSOURCE(self, lexeme):
        return ".source " + lexeme + JasminCode.END

    def emitCLASS(self, lexeme):
        return ".class " + lexeme + JasminCode.END

    def emitSUPER(self, lexeme):
        return ".super " + lexeme + JasminCode.END

    def emitRETURN(self):
        return JasminCode.INDENT + "return" + JasminCode.END

    def emitIRETURN(self):
        return JasminCode.INDENT + "ireturn" + JasminCode.END

    def emitFRETURN(self):
        return JasminCode.INDENT + "freturn" + JasminCode.END

    def emitARETURN(self):
        return JasminCode.INDENT + "areturn" + JasminCode.END
