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
    
    procedure_body: "initiate and confirm step" step_num [declare_body] (assign_command | if_cond | init_comm)+ "end step;" ->step_name
    
    step_num: STRING

    declare_body: "declare" var_declaration+ "end declare" 
    
    var_declaration: "variable" STRING "of type" var_type
    var_type: STRING
    
    assign_command: assigned ":=" assignee ";"
    assigned: STRING
    assignee: ESCAPED_STRING | NUMBER

    if_cond: "if" condition "then" exec_comm "end if;"
    condition: first_cond "=" second_cond -> equality
              | first_cond "!=" second_cond -> inequality
    first_cond: STRING
    second_cond: STRING
    exec_comm: action ESCAPED_STRING ";"
    action: STRING
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

