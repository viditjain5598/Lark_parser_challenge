from lark import Lark, Transformer, v_args

try:
    input = raw_input
except NameError:
    pass

PLUTO_code = """
            procedure 
                initiate and confirm step step1
                    declare
                        variable CMD_TM_LINK_VALUE of type string
                        variable TRSP2_RECEIVER_STATUS of type string
                    end declare
        
                    CMD_TM_LINK_VALUE := "TM FLOW";
                    TRSP2_RECEIVER_STATUS := "TC tracking";

                    if CMD_TM_LINK != CMD_TM_LINK_VALUE then
                        log "There is no TM FLOw.";
                    end if;
                end step;
                initiate and confirm step step2
                    initiate and confirm ZDW17001;
                end step;

            end procedure
        """
PLUTO_grammar = """
    start : procedure
    procedure: "procedure" procedure_body+ "end procedure"  -> procedure_body
    procedure_body: "initiate and confirm step" STRING [declare_body] (assign_command | if_cond | init_comm)+ "end step;" ->step_name
    declare_body: "declare" var_declaration+ "end declare" 
    var_declaration: "variable" STRING "of type" STRING
    assign_command: STRING ":=" ESCAPED_STRING ";"
    if_cond: "if" condition "then" exec_comm "end if;"
    condition: STRING ("!=" | "=") STRING
    exec_comm: "log" ESCAPED_STRING ";"
    init_comm: "initiate and confirm" STRING ";"

    %import common.ESCAPED_STRING  
    %import common.CNAME -> STRING
    %import common.NUMBER -> NUMBER
    %import common.WS
    %ignore WS 
    """
parser = Lark(PLUTO_grammar)
def run_print(program):
    parse_tree = parser.parse(program)
    print(parse_tree.pretty())

def test():
    run_print(PLUTO_code)

def main():
    while True:
        code = input('> ')
        try:
            run_turtle(code)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    test()
    # main()


#output:
"""
start
  procedure_body
    step_name
      step1
      declare_body
        var_declaration
          CMD_TM_LINK_VALUE
          string
        var_declaration
          TRSP2_RECEIVER_STATUS
          string
      assign_command
        CMD_TM_LINK_VALUE
        "TM FLOW"
      assign_command
        TRSP2_RECEIVER_STATUS
        "TC tracking"
      if_cond
        condition
          CMD_TM_LINK
          CMD_TM_LINK_VALUE
        exec_comm       "There is no TM FLOw."
    step_name
      step2
      init_comm ZDW17001

"""

