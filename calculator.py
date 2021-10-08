import re


from collections import deque


def handle_command(command):
    if command == "/exit":
        print("Bye!")
        exit()
    elif command == "/help":
        print("The program calculates a given expression")
    else:
        print("Unknown command")


def transform_into_expression(string, variables) -> str:
    """this function takes input string and empty variables dict as arguments, analysis if provided expression is valid and
     formats an expression by replacing variables with its values and reducing sequence of repittive math operators.
     otherwise an error message is printer"""
    if re.match(r"\A[-+]?\d+$", string):
        print(string.lstrip("+"))
    elif string[-1] in {"+", "-", "/", "*"}:
        print("Invalid expression")
    elif re.search(r"[a-z]+", string, flags=re.IGNORECASE):


        return handle_variables(string, variables)

    elif "**" in string or "//" in string:

        """ if there is a sequence of * or /, the program must print error message """
        print("Invalid expression")

    # r"(([-+]?)\d+( ?[-+*/]+ ?\d+)+)"
    elif re.search(r"\A[-+]?((\d+\s*[+-/*)(\s]+\s*)*\d*)*", string):
        """ this template take an expresion with already replaced variables with their values
        double or more * is not allowed, replace with ^ and add single * - rewrite regex"""
        """Splitting arguments and signs into the list"""

        #print("LINE 36 works")
        # replacing sequences of + with a single plus
        if re.search(r"\+{2,}", string):
            string = re.sub(r"\+{2,}", "+", string)
        # replacing all minuse sequences with + or - based on their meaning
        if re.search(r"-{2,}", string):
            if len(re.search(r"-{2,}", string).group()) % 2 == 0:
                string = re.sub(r"-{2,}", "+", string)
            else:
                string = re.sub(r"-{2,}", "-", string)


        braces = deque()
        if "(" in string or ")" in string:
            # braces = deque()
            for symbol in string:
                if symbol == "(":
                    braces.append(symbol)
                elif symbol == ")":
                    if not braces:
                        print("Invalid expression")
                        return ""
                    else:
                        braces.popleft()

        if len(braces) != 0:
            print("Invalid expression")
        else:
            return string
    else:
        print("Invalid expression")


def handle_variables(arguments_str, variables):
    expr_template = re.compile(r"\A[-+]?(\w+\s*[+-/*)(\s]+\s*)*")
    """Print variable value scenario"""
    if re.match(r"\A\s*[a-z]+$", arguments_str, flags=re.IGNORECASE):
        if arguments_str in variables.keys():
            print(variables[arguments_str])
        else:
            print("Unknown variable")
        """ASSIGNMENT SCENARIO"""
    elif re.search(r"=", arguments_str):
        return assign_variable(arguments_str, variables)
    elif re.match(expr_template, arguments_str):
        """ expression with variables """
        expression_str = compute_var_operations(arguments_str, variables)
        if expression_str:
            return transform_into_expression(expression_str, variables)


def assign_variable(arguments_str, variables) -> None:
    var_ass_template = re.compile(r"\A\s*[a-z]+\s*=\s*([a-z]+|[\d]+)\s*$", flags=re.IGNORECASE)
    if re.match(var_ass_template, arguments_str):
        """ scenario for var = int/float only """
        var, val = re.split(r"\s*=\s*", arguments_str.replace(" ", ""))
        var = var.strip(" ")
        val = val.strip(" ")
        if val.isnumeric():
            variables[var] = val
        else:
            """reassignment"""
            if val in variables.keys():
                variables[var] = variables[val]
            else:
                print("Unknown variable")
    elif re.match(r"\w+", arguments_str):
        print("Invalid identifier")
    else:
        print("Invalid assignment")


def compute_var_operations(arguments_str, variables) -> str:
    var_list = re.findall(r"[\w]+", arguments_str, flags=re.IGNORECASE)
    issue_counter = 0
    arguments_lst = arguments_str.split(" ")

    """ test just this function with the complex variable + int expression"""
    for i in range(int(len(arguments_lst))):
        if arguments_lst[i] in var_list:
            if arguments_lst[i] in variables.keys():
                arguments_lst[i] = str(variables[arguments_lst[i]])
            else:
                if arguments_lst[i].isdigit():
                    arguments_lst[i] = str(arguments_lst[i])
                else:
                    issue_counter += 1
                    # concider replacing the line above with error message
    if issue_counter:
        print("Unknown variable")
    else:
        return " ".join(arguments_lst)


def compute_expression(math_expression) -> str:
    """takes deque object representing math expression and recursively calculates until answer is ready, then returns the answer as a str """
    # math_expression = prioritized_computation(math_expression)  # turned of for the stage #6 as no prioritized operations for now
    if len(math_expression) == 1:
        return "".join(math_expression)
    else:
        arg1 = int(math_expression.popleft())
        sign = math_expression.popleft()
        arg2 = int(math_expression.popleft())
        if sign == "-":
            math_expression.appendleft(str(arg1 - arg2))
        elif sign == "+":
            math_expression.appendleft(str(arg1 + arg2))
        return compute_expression(math_expression)


def main():
    variables = dict()
    while True:
        arguments_str = input().strip().replace("(", "( ").replace(")", " )")  # removing all extra spaces on both sides of input
        if len(arguments_str) == 0:
            continue
        elif arguments_str.startswith("/"):
            handle_command(arguments_str)
        else:
            expression = transform_into_expression(arguments_str, variables)
            if expression:
                # expression_deque = deque(expression.split(" "))
                # print("EXPRESSION IS:\n", expression)
                # result = compute_expression(expression_deque)
                result = int(eval(expression))
                print(result)


def postfix_algorigm(str_expression):

    str_expression = str_expression.replace("(", "( ").replace(")", " )")

    tokens = str_expression.split(" ")

    operator_stack = deque()
    output_queue = deque()

    for element in tokens:
        """ if an element of the 'tokens' stack is digit"""
        if element.isdigit():
            output_queue.append(element)
        # if element is an operator
        elif element in {"+", "-", "*", "/", "^"}:
            top = {"*", "/", "^"}  # top priority operators

            if operator_stack:  # check if there is at least one element in operator_stack
                while operator_stack and operator_stack[-1] in top:  # if top operator in stack has higher priority than current iterated element - pushing elements from
                    # stack to output queue
                    output_queue.append(operator_stack.pop())
                # else adding ot the operator_stack
                operator_stack.append(element)

            # if there are no elements in operator_stack - appending, not additional checks required
            else:
                operator_stack.append(element)

        elif element == "(":
            operator_stack.append(element)
        elif element == ")":
            while operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            if operator_stack[-1] == "(":
                operator_stack.pop()
                # these lines can be deleted
                while operator_stack:
                    output_queue.append(operator_stack.pop())

    while operator_stack:
        output_queue.append(operator_stack.pop())
    print("output_queue:\n", " ".join(output_queue))
    """ at this moment result is like:
        ORIGINAL EXPRESSION:
     2 * (3 + 4) + 1 + 2 ^ 2
    output_queue:
     2 3 4 + * 1 2 2 ^ + +
     
     but the one required is: 
     2 3 4 + * 1 + 2 2 ^ +
     """
    # output = " ".join(output_queue)


if __name__ == '__main__':
    #remove_redundand_signs()
    main()
    # arg_str = "2 * (3 + 4) + 1 + 2 ^ 2"
    # making braket a separate element
    # print("ORIGINAL EXPRESSION:\n", arg_str)
    # postfix_algorigm(arg_str)



