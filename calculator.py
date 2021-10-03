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
    elif re.search(r"(([-+]?)\d+( ?[-+*/]+ ?\d+)+)", string):
        """ this template take an expresion with already replaced variables with their values
        double or more * is not allowed, replace with ^ and add single * - rewrite regex"""
        """Splitting arguments and signs into the list"""
        str_as_lst = string.split(" ")
        for arg in range(len(str_as_lst)):
            if re.match(r"[\-]+$", str_as_lst[arg]):
                if len(str_as_lst[arg]) % 2 == 0:
                    str_as_lst[arg] = "+"
                else:
                    str_as_lst[arg] = "-"
            elif re.match(r"\+{2,}", str_as_lst[arg]):
                str_as_lst[arg] = "+"
        string = " ".join(str_as_lst)
        return string
    else:
        print("Invalid expression")


def handle_variables(arguments_str, variables):
    expr_template = re.compile(r"\A(\s*\w+\s*[-+*/]*\s*)+$")
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
        arguments_str = input().strip()  # removing all extra spaces on both sides of input
        if len(arguments_str) == 0:
            continue
        elif arguments_str.startswith("/"):
            handle_command(arguments_str)
        else:
            expression = transform_into_expression(arguments_str, variables)
            if expression:
                expression_deque = deque(expression.split(" "))
                result = compute_expression(expression_deque)
                print(result)


def postfix_algorigm(str_expression):

    tokens = str_expression.split(" ")

    operator_stack = deque()
    output_queue = deque()


    for element in tokens:
        """ if an element of the 'tokens' stack is digit"""
        if element.isdigit():
            output_queue.append(element)

        elif element in {"+", "-", "*", "/", "^"}:
            top = {"*", "/", "^"}
            if operator_stack:
                while operator_stack[-1] in top:
                    output_queue.append(operator_stack.pop())
                else:
                    operator_stack.append(element)  # check this line
            else:
                operator_stack.append(element)
        elif element == "(":
            operator_stack.append(element)
        elif element == ")":
            while operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            if operator_stack[-1] == "(":
                operator_stack.pop()

    print("output_queue:\n", output_queue)
    output = output_queue + operator_stack
    print(output)

if __name__ == '__main__':
    #main()
    arg_str = "2 * (3 + 4) + 1"
    arg_str = arg_str.replace("(", "( ").replace(")", " )")  # making braket a separate element
    print("ORIGINAL EXPRESSION:\n", arg_str)
    postfix_algorigm(arg_str)
