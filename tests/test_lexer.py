"""
Lexer test cases for TyC compiler
TODO: Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer

    
""" CHARSET """
def test_001():
    input = " "
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_002():
    input = """                 




    """
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_003():
    input = "\t\t\t"
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_004():
    input = "\n\n\n"
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_005():
    input = "\r\r\r"
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_006():
    input = """\n\r\t \r\n\t"""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_007():
    input = "\a\b"
    expect = "Error Token "
    assert Tokenizer(input).get_tokens_as_string().startswith(expect)

def test_008():
    input = "\v\v\v"
    expect = "Error Token "
    assert Tokenizer(input).get_tokens_as_string().startswith(expect)

def test_009():
    input = " \t\n\r\f"
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_010():
    input = ""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

""" --- Comment --- """
def test_011():
    input = "// This is a comment line \n"
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_012():
    input = """// @ूाीू  /̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿     \\n \\t \\n \\t \\n  ▄︻デ══━一💥"""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect


def test_013():
    input = """// This is a comment line \\n with endline escape"""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_014():
    input = """
    // This is a comment line \\n continue the comment line
    // This is a comment line \\r\\n continue the comment line
    // int a = 5;
    // string s = "an truong";    
"""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_015():
    input = """
    // This is a comment line // This is the part in the comment line
"""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_016():
    input = """
                                                              //    _____//                  ------
        //\\       |\\   ||       ======   |===\\     ||     ||    /_______\    |\\   ||    /______|
       //  \\      ||\\  ||         ||     ||   ))    ||     ||    ||     ||    ||\\  ||    ||
      //====\\     || \\ ||         ||     ||__//     ||     ||    ||     ||    || \\ ||    ||   ====
     //      \\    ||  \\||         ||     ||   \\    ||_____||    ||_____||    ||  \\||    ||____||
    //        \\   ||   \||         ||     ||    \\   \_______/    \_______/    ||   \||    \______|
    
    // \\n \\r \\a \\b \\t " '' int float struct MYID DIT ME CUOC SONG, exit goto EOF ERROR raise ERROR     
"""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_017():
    input = """
    // HELLO MOI NGUOI TOI LA AN TRUONG 
    DAY KHONG PHAI COMMENT LINE
"""
    expect = "DAY,KHONG,PHAI,COMMENT,LINE,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_018():
    input = "/ This is not a comment line"
    expect = "/,This,is,not,a,comment,line,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_019():
    input = "/ This is also not a comment line /"
    expect = "/,This,is,also,not,a,comment,line,/,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_020():
    input = " This is not // a Comment //"
    expect = "This,is,not,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_021():
    input = """
    /*
        This is a block comment
    */
"""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_022():
    input = """
    /*

    ░░░░F░E░E░L░░T░H░E░░░░
    ▀██▀─▄███▄▀██─██▀██▀▀█
    ─██─▐██─██▌██─██─██▄█─
    ─██─▐██─██▌▐█▄█▌─██▀█─
    ▄██▄█▀███▀──▀█▀─▄██▄▄█ 

                                               %%%***                                               
                                            %%%%%%******                                            
                                         %%%%%%%%%*********                                         
                                      %%%%%%%%%%%%************                                      
                                   %%%%%%%%%%%%%%%***************                                   
                               %%%%%%%%%%%%%%%%%%%*******************                               
                            %%%%%%%%%%%%%%%%%%%%%%**********************                            
                         %%%%%%%%%%%%%%%%%%%%%%%%%*************************                         
                        %%%%%%%%%%%%%%%%%%%%%%%%%%**************************                        
                        %%%%%%%%%%%%%%%%%%%%%%%%%%**************************                        
                        %%%%%%%%%%%%%%%%%%%%%%%%%%**************************                        
                        %%%%%%%%%%%%%%%%%%%%%%%%%%**************************                        
                        %%%%%%%%%%%%%%%%%%%%%%%%%%**************************                        
                        %%%%%%%%%%%%%%%%%%%%%%%%%%**************************                        
                        %%%%%%%%%%%%%%%%%%%%%%%%%%**************************                        
                        %%%%%%%%%%%%%%%%%%%%%%%%%%**************************                        
                        %%%%%%%%%%%%%%%%%%%%%%%%%  *************************                        
                        %%%%%%%%%%%%%%%%%%%%%%        **********************                        
                        %%%%%%%%%%%%%%%%%%                ******************                        
                        %%%%%%%%%%%%%%%                      ***************                        
                        %%%%%%%%%%%%                            ************                        
                        %%%%%%%%                                    ********                        
                        %%%%%%                                        ******                        
                        *#%      %%%%%%%%%%         %%%%      %%%%%%     +*%                        
                     *****      %%%%%%%%%%%%%%%     %%%%     %%%%%%       %%%%%                     
                 *********      %%%%%%%%%%%%%%%%    %%%%   %%%%%%         %%%%%%%%%                 
               ***********      %%%%%      %%%%%    %%%% %%%%%%%          %%%%%%%%%%%%              
            **************      %%%%%%%%%%%%%%%     %%%%%%%%%%            %%%%%%%%%%%%%%            
        ******************      %%%%%%%%%%%%%%%     %%%%%%%%%%%           %%%%%%%%%%%%%%%%%%        
     *********************      %%%%%    %%%%%%%    %%%%%%%%%%%%          %%%%%%%%%%%%%%%%%%%%%     
  ************************      %%%%%       %%%%    %%%%    %%%%%         %%%%%%%%%%%%%%%%%%%%%%%%  
**************************      %%%%%%%%%%%%%%%%    %%%%     %%%%%%       %%%%%%%%%%%%%%%%%%%%%%%%%%
**************************      %%%%%%%%%%%%%%%     %%%%      %%%%%%      %%%%%%%%%%%%%%%%%%%%%%%%%%
**************************       %%%%%%%%%%%%       %%%%       %%%%%      %%%%%%%%%%%%%%%%%%%%%%%%%%
**************************                                                %%%%%%%%%%%%%%%%%%%%%%%%%%
**************************      *************  **  ********* *** ***      %%%%%%%%%%%%%%%%%%%%%%%%%%
**************************        ***  ******  *********  **********      %%%%%%%%%%%%%%%%%%%%%%%%%%
**************************        ***  *****   *********     *******      %%%%%%%%%%%%%%%%%%%%%%%%%%
**************************        ***  ***  *****  ********* *******      %%%%%%%%%%%%%%%%%%%%%%%%%%
************************#%%                                              ***%%%%%%%%%%%%%%%%%%%%%%%%
*********************%%%%%%%%%                                        *********%%%%%%%%%%%%%%%%%%%%%
*****************#%%%%%%%%%%%%%%%%                                ****************#%%%%%%%%%%%%%%%%%
**************#%%%%%%%%%%%%%%%%%%%%%%                          **********************#%%%%%%%%%%%%%%
***********%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                    ****************************#%%%%%%%%%%%
********%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%              **********************************#%%%%%%%%
****#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%      *****************************************#%%%%%
*#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  ***********************************************%%
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%**************************************************
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%      ********************************************   
       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%            **************************************      
          %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                    ******************************          
             %%%%%%%%%%%%%%%%%%%%%%%%                          ************************             
                %%%%%%%%%%%%%%%%%%                                ******************                
                    %%%%%%%%%%                                        **********                    
                       %%%%%                                             ****      

                       

                        _         FUCK YOU        _
                       |_|                       |_|
                       | |         /^^^\         | |
                      _| |_      (| "o" |)      _| |_
                    _| | | | _    (_---_)    _ | | | |_
                   | | | | |' |    _| |_    | `| | | | |
                   |          |   /     \   |          |
                    \        /  / /(. .)\ \  \        /
                      \    /  / /  | . |  \ \  \    /
                        \  \/ /    ||Y||    \ \/  /
                         \__/      || ||      \__/
                                   () ()
                                   || ||
                                  ooO Ooo          PPL

    */
"""

    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_023():
    input = """
    /*

        // \n \n \n \n \n
        int float struct void auto string
        "string", "FFFF" "0xFF"
    */
"""

    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_024():
    input = """
    /*
        /*
            HELLO
        \r\n
    */
"""

    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_025():
    input = """
    /*
        #include <iostream>

        int main() {
            std::cout << "HELLO WORLD" << std::endl;
        }
    */
"""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_026():
    input = """
    /* /* /* /* /* /* /*
        \\r\\n
    */ 
"""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_027():
    input = """
    /*
        /*
            Hello
        */
    */
"""
    expect = "*,/,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_028():
    input = """
    /* /* */ FAILED */
"""

    expect = "FAILED,*,/,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_029():
    input = """
    /*
        FAILED
"""
    expect = "/,*,FAILED,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_030():
    input = """
    Failed
    */
"""
    expect = "Failed,*,/,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_031():
    input = """
    varID \t\t\n asdasd PPL \t\t\t      intValue                  \n\t                   floatValue
"""
    expect = "varID,asdasd,PPL,intValue,floatValue,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_032():
    input = """
    _int
    _float
    _value
            _
            ppl_HCMUT
            myLover_
            _______
        hk_252
            mssv2252013

    // This is a comment line
"""
    expect = "_int,_float,_value,_,ppl_HCMUT,myLover_,_______,hk_252,mssv2252013,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_033():
    input = """
    @var
"""
    expect = "Error Token"
    assert Tokenizer(input).get_tokens_as_string().startswith(expect)

def test_034():
    input = """
    var1\\nvar2
"""
    expect = "var1,Error Token"
    assert Tokenizer(input).get_tokens_as_string().startswith(expect)

def test_035():
    input = """
    ab//
"""

    expect = "ab,<EOF>"
    assert Tokenizer(input).get_tokens_as_string().startswith(expect)

def test_036():
    input = "myVar\\r\\nmyVar"
    expect = "myVar,Error Token"
    assert Tokenizer(input).get_tokens_as_string().startswith(expect)

def test_037():
    input = "252HCMUT"
    expect = "252,HCMUT,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_038():
    input = "ूाीू "
    expect = "Error Token"
    assert Tokenizer(input).get_tokens_as_string().startswith(expect)

# --- Keyword ---#
def test_039():
    input = "int intVAR"
    expect = "int,intVAR,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_040():
    input = "auto _auto \n autoo"
    expect = "auto,_auto,autoo,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_041():
    input = "autobreakcasecontinue"
    expect = "autobreakcasecontinue,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_042():
    input = "36auto thanh hoa"
    expect = "36,auto,thanh,hoa,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_043():
    input = "return RetAn"
    expect = "return,RetAn,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_044():
    input = """
    /*
        if (antruong is Student as student)
            return antruong.Study();
    */
"""
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_045():
    input = "// int mssv = 2252013;"
    expect = "<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_046():
    input = """auto \r\n
    break\r\n
    case\r\n
    continue\r\n
    default\r\n
    else\r\n
    float\r\n
    for\r\n
    if\r\n
    int\r\n
    return\r\n
    string\r\n
    struct\r\n
    switch\r\n
    void\r\n
    while\r\n
    """

    expect = "auto,break,case,continue,default,else,float,for,if,int,return,string,struct,switch,void,while,<EOF>"

    assert Tokenizer(input).get_tokens_as_string() == expect

def test_047():
    input = """
    auto\\r\\n//
"""
    expect = "auto,Error Token"
    assert Tokenizer(input).get_tokens_as_string().startswith(expect)

def test_048():
    input = """
    // struct
    struct
    if
    intfloat
    _int
    _float
    _struct
    Sstruct
    Iint
    @struct
"""
    expect = "struct,if,intfloat,_int,_float,_struct,Sstruct,Iint,Error Token"
    assert Tokenizer(input).get_tokens_as_string().startswith(expect)

# --- Operator --- #
def genOpInput(op : str):
    return f"""
    {op}
    intNum1 {op} intNum2
    intNum1{op}intNum2
    {op}intNum1
    {op} \r\n\t intNum1
    // intNum1 {op} intNum2
    /* intNum1 {op} intNum2 */
"""

def genOpExpect(op : str):
    return f"{op},intNum1,{op},intNum2,intNum1,{op},intNum2,{op},intNum1,{op},intNum1,<EOF>"

def test_049():
    input = genOpInput('+')
    expect = genOpExpect('+')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_050():
    input = genOpInput('-')
    expect = genOpExpect('-')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_051():
    input = genOpInput('*')
    expect = genOpExpect('*')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_052():
    input = genOpInput('/')
    expect = genOpExpect('/')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_053():
    input = genOpInput('%')
    expect = genOpExpect('%')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_054():
    input = genOpInput('%')
    expect = genOpExpect('%')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_055():
    input = genOpInput('==')
    expect = genOpExpect('==')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_056():
    input = """
    ==
            ==
                ===   
            = 
"""
    expect = "==,==,==,=,=,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_057():
    input = """
    = myVar = + =            =
"""
    expect = "=,myVar,=,+,=,=,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_058():
    input = genOpInput('!=')
    expect = genOpExpect('!=')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_059():
    input = "===== \r\n\t ! \r\n\t  \n\n\n        =    !="
    expect = "==,==,=,!,=,!=,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_060():
    input = genOpInput('<')
    expect = genOpExpect('<')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_061():
    input = genOpInput('>')
    expect = genOpExpect('>')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_062():
    input = genOpInput('<=')
    expect = genOpExpect('<=')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_063():
    input = "<< \r\n\r\n == \n \n \n         \t \t \t   <="
    expect = "<,<,==,<=,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_064():
    input = "<<=== YASUO GANK TEAM 15GG === >>"
    expect = "<,<=,==,YASUO,GANK,TEAM,15,GG,==,=,>,>,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_065():
    input = """
      /-------/
          +
          +
          O
        //||\\
       // || \\  ME AFTER LEARNING PPL
         //\\
        //  \\
"""
    expect = "/,--,--,--,-,/,+,+,O,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_066():
    input = genOpInput('>=')
    expect = genOpExpect('>=')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_067():
    input = """
    >

                ==
    >>>>>==    
"""
    expect = ">,==,>,>,>,>,>=,=,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_068():
    input = genOpInput('||')
    expect = genOpExpect('||')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_069():
    input = """
//      ,         ,
//      |\\\\ ////|
//      | \\\V/// |
        |  |---|  |
        |  |===|  |
        |  |P  |  |
        |  | P |  |
//       \ |  L| /
//        \|===|/
//         '---'
    
    """

    expect = "Error Token"
    assert Tokenizer(input).get_tokens_as_string().startswith(expect)

def test_070():
    input = genOpInput('&&')
    expect = genOpExpect('&&')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_071():
    input = genOpInput('!')
    expect = genOpExpect('!')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_072():
    input = genOpInput('++')
    expect = genOpExpect('++')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_073():
    input = """
             ()
             ||
    ()=======||++++++++++++++++++++>
             ||
             ()
"""
    expect = "(,),||,(,),==,==,==,=,||,++,++,++,++,++,++,++,++,++,++,>,||,(,),<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_074():
    input = genOpInput('--')
    expect = genOpExpect('--')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_075():
    input = """
             ()
             ||
    ()=======||-------------------->
             ||
             ()
"""
    expect = "(,),||,(,),==,==,==,=,||,--,--,--,--,--,--,--,--,--,--,>,||,(,),<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_076():
    input = genOpInput('=')
    expect = genOpExpect('=')
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_077():
    input = genOpInput('.')
    expect = genOpExpect('.')
    assert Tokenizer(input).get_tokens_as_string() == expect


def test_078():
    input = """
    ((.)(.))
"""
    expect = "(,(,.,),(,.,),),<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_079():
    input = """
    (
        1,
        2,
        3
    )    
"""
    expect = "(,1,,,2,,,3,),<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_080():
    input = """
    {
        value : 5,
        vector : (1,2,3)
    };
"""
    expect = "{,value,:,5,,,vector,:,(,1,,,2,,,3,),},;,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_081():
    input = """
    0 5 10 01 00005
"""
    expect = "0,5,10,01,00005,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_082():
    input = """
    0. 0.2 0.23 -0.23 +.23 -.23
"""
    expect = "0.,0.2,0.23,-,0.23,+,.23,-,.23,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_083():
    input = """
    .e5
"""
    expect = ".,e5,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_084():
    input = """
    e5 1.e5 .1e5 e-5 10.e-5 -10.e-5 10.5e5 10.e+5
"""
    expect = "e5,1.e5,.1e5,e,-,5,10.e-5,-,10.e-5,10.5e5,10.e+5,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_085():
    input = """
    1.                      5
"""
    expect = "1.,5,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_086():
    input = """
    *.5e*3
"""
    expect = "*,.5,e,*,3,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_087():
    input = """
    1.3e++5
"""
    expect = "1.3,e,++,5,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_088():
    input = """
    1.e----5
"""
    expect = "1.,e,--,--,5,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_089():
    input = """
    "Hello World \\n Hello World"
"""
    expect = "Hello World \\n Hello World,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_090():
    input = """
    "This is a string containing tab \\t"
    "He asked me: \\"Where is John?\\""
"""
    expect = """This is a string containing tab \\t,He asked me: \\"Where is John?\\",<EOF>"""
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_091():
    input =  """
    "@2252013AnTruong"
"""
    expect = "@2252013AnTruong,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_092():
    input = """
    "✧˚ ༘⋆2026✧˚ ༘ ⋆"
"""
    expect = "✧˚ ༘⋆2026✧˚ ༘ ⋆,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_093():
    input = """
    "This is just a string // not a comment"
"""
    expect = "This is just a string // not a comment,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_094():
    input = """
    "This is unclosed string
"""
    expect = "Unclosed String: This is unclosed string"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_095():
    input = """
    This is also unclosed string"
"""
    expect = "This,is,also,unclosed,string,Unclosed String: "
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_096():
    input = """
    "\\b\\f\\r\\n\\t\\"\\\\"    
"""
    expect = """\\b\\f\\r\\n\\t\\"\\\\,<EOF>"""
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_097():
    input = """
    "HELLO
    WORLD"
"""
    expect = "Unclosed String: HELLO"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_098():
    input = """
    "invalid escape \\a can't be here"
"""
    expect = "Illegal Escape In String: invalid escape \\a"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_099():
    input = """
    "invalid escapes \\a\\a\\a can't be here"
"""
    expect = "Illegal Escape In String: invalid escapes \\a"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_100():
    input = """
    "I said: 'HCMUT'"    
"""
    expect = "I said: 'HCMUT',<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_101():
    input = """"Check valid here" not come here"
    """
    expect = "Check valid here,not,come,here,Unclosed String: "
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_102():
    input = """
    "int \\n + auto \\n struct \\n"
    // "
    /* " */
"""
    expect = "int \\n + auto \\n struct \\n,<EOF>"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_103():
    input = """"text"""
    expect = "Unclosed String: text"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_104():
    input = """
    "Invalid escape first \\a
    // OK
"""
    expect = "Illegal Escape In String: Invalid escape first \\a"
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_105():
    input = """
    "AnTruong\\\\ \\ "
"""
    expect = 'Illegal Escape In String: AnTruong\\\\ \\ '
    assert Tokenizer(input).get_tokens_as_string() == expect

def test_106():
    input = """"m\\"""
    expect = "Unclosed String: m\\"
    assert Tokenizer(input).get_tokens_as_string() == expect
