
from lark import Lark, Transformer, v_args

try:
    input = raw_input
except NameError:
    pass

dsl_code = """
            repeat 10 print \"hello world\"
            repeat 20 print \"My name is Vidit\"
        """

dsl_py_grammar = """
    start : value+
    value: "repeat" NUMBER -> iter
         | "print" STRING  -> print_comm

    %import common.ESCAPED_STRING -> STRING
    %import common.NUMBER -> NUMBER
    %import common.WS
    %ignore WS 
    """

@v_args(inline = True)
class dsl_py(Transformer):
    def iter(self, NUMBER):
        return "for i in range(" + str(NUMBER) + "):"
    def print_comm(self, STRING):
        return "    print(" + STRING + ")"

dsl_py_parser = Lark(dsl_py_grammar, parser = "lalr", transformer = dsl_py())
py_code = dsl_py_parser.parse

def test():
    py_code_str = ""
    code_tree = py_code(dsl_code)
    for i in code_tree.children:
        py_code_str += i + "\n"
    print(py_code_str)
    

if __name__ == '__main__':
    test()


# output:

# for i in range(10):
#     print("hello world")
# for i in range(20):
#     print("My name is Vidit")






