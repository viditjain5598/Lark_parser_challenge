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
                end step;
            end procedure
        """
PLUTO_code_1 = """ procedure
    initiate and confirm step step1
        declare
            variable CMD_TM_LINK_VALUE of type string,
            variable TRSP2_RECEIVER_STATUS of type string
        end declare
        
        CMD_TM_LINK_VALUE := "TM FLOW";
        TRSP2_RECEIVER_STATUS := "TC tracking";
            
        if value of CMD_TM_LINK != CMD_TM_LINK_VALUE then
            log "There is no TM FLOW.";
        end if; 

        if NTR80220 != TRSP2_RECEIVER_STATUS then
            log "TRSP2 is " + NTR80220;
        end if;

    end step;
    
    initiate and confirm step step2
        initiate and confirm ZDW17001;
    end step;

end procedure
"""

PLUTO_grammar = """
    start : procedure
    procedure: "procedure" procedure_body "end procedure"  -> procedure_body
    procedure_body: "initiate and confirm step" STRING [declare_body] "end step;" ->step_name
    declare_body: "declare" var_declaration+ "end declare"
    var_declaration: "variable" STRING "of type" STRING 
    %import common.CNAME -> STRING
    %import common.NUMBER -> NUMBER
    %import common.WS
    %ignore WS 
    """

parser = Lark(PLUTO_grammar)

def run_print(program):
    parse_tree = parser.parse(program)
    print(parse_tree)

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
