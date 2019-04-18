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
                        log "There is no TM FLOW.";
                    end if;
                    if NTR80220 != TRSP2_RECEIVER_STATUS then
                        log "TRSP2 is + NTR80220";
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
py_code = parser.parse

def run_convert(parse_tree):
    pyth_str = ""
    if hasattr(parse_tree, 'data'):
        if parse_tree.data == "step_name":
            pyth_str += "def " + str(parse_tree.children[0].children[0]) + ":\n" 
        if parse_tree.data == "var_declaration":
            pyth_str += "    " + str(parse_tree.children[0]) + " = \"\"\n"
        if parse_tree.data == "assign_command":
            pyth_str += "    " + str(parse_tree.children[0].children[0]) \
            + " = " + str(parse_tree.children[1].children[0]) + "\n"
        if parse_tree.data == "if_cond":
            pyth_str += "    if " + str(parse_tree.children[0].children[0].children[0])
            if str(parse_tree.children[0].data) == "inequality":
                pyth_str += " != "
            elif str(parse_tree.children[0].data) == "equality":
                pyth_str += " == "
            pyth_str += str(parse_tree.children[0].children[1].children[0]) + ":\n"
            if parse_tree.children[1].data == "exec_comm":
                pyth_str += "        log(" + str(parse_tree.children[1].children[1]) + ")\n"
        if parse_tree.data == "init_comm":
            pyth_str += "    initiate(" + str(parse_tree.children[0]) + ")\n"
    if hasattr(parse_tree, 'children'):
        for i in parse_tree.children:
            pyth_str += run_convert(i);
    return pyth_str
def test():
    parse_tree = py_code(PLUTO_code)
    #print(parse_tree.pretty())
    pyth_str = run_convert(parse_tree)
    print(pyth_str)

def main():
    while True:
        code = input('> ')
        try:
            run_convert(code)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    test()
    # main()


#output:
"""
def step1:
    CMD_TM_LINK_VALUE = ""
    TRSP2_RECEIVER_STATUS = ""
    CMD_TM_LINK_VALUE = "TM FLOW"
    TRSP2_RECEIVER_STATUS = "TC tracking"
    if CMD_TM_LINK != CMD_TM_LINK_VALUE:
        log("There is no TM FLOW.")
    if NTR80220 != TRSP2_RECEIVER_STATUS:
        log("TRSP2 is  + NTR80220")
def step2:
    initiate(ZDW17001)
"""

