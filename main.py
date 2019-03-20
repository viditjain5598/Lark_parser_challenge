
try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass

import turtle

from lark import Lark

print_grammar = """
    start: instruction+
    instruction: "repeat" NUMBER -> no_iter
               | "print" string  -> prnt_comm
 
    string : ESCAPED_STRING
    %import common.ESCAPED_STRING
    %import common.INT -> NUMBER    
    %import common.WS
    %ignore WS

"""

parser = Lark(print_grammar)

def run_instruction_print(t):
    if t.data == 'no_iter':
        print("for i in range(" + str(*t.children) + "):")  
    elif t.data == 'prnt_comm':
        # str1 = ""
        # str1.join(*t.children)
        print("    print(\"\")")

    else:
        raise SyntaxError('Unknown instruction: %s' % t.data)

def run_print(program):
    parse_tree = parser.parse(program)
    for inst in parse_tree.children:
        run_instruction_print(inst)

def test():
    text = """
        repeat 20 print "hello"
    """
    run_print(text)

if __name__ == '__main__':
    test()

#  output:
#  
#  for i in range(20):
#     print("")



