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


def transform_into_expression(string, variables) -> list:
    """this function takes input string and empty variables dict as arguments, analysis if provided expression is valid and
     formats an expression by replacing variables with its values and reducing sequence of repittive math operators.
     otherwise an error message is printer"""
    if re.match(r"\A[-+]?\d+$", string):
        print(string.lstrip("+"))

    elif string[-1] in {"+", "-", "/", "*"}:
        print("Invalid expression")

    elif re.search(r"[a-z]+", string, flags=re.IGNORECASE):
        expr = handle_variables(string, variables)
        return expr

    elif re.search(r"(([-+]?)\d+( ?[-+*/]+ ?\d+)+)", string):
        """ this template take an expresion with already replaced variables with their values
        double or more * is not allowed, replace with ^ and add single * - rewrite regex"""
        """Splitting arguments and signs into the list"""
        str_as_lst = string.split(" ")
        for arg in range(len(str_as_lst)):
            if str_as_lst[arg] != " ":
                if re.match(r"[\-]+$", str_as_lst[arg]):
                    if len(str_as_lst[arg]) % 2 == 0:
                        str_as_lst[arg] = "+"
                    else:
                        str_as_lst[arg] = "-"
                elif re.match(r"\+{2,}", str_as_lst[arg]):
                    str_as_lst[arg] = "+"
        return str_as_lst
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
        assign_variable(arguments_str, variables)

        """ expression with variables """
    elif re.match(expr_template, arguments_str):
        expression_list = compute_var_operations(arguments_str, variables)
        if expression_list:
            exp_str = " ".join(expression_list)
            transformed_expr = transform_into_expression(exp_str, variables)
            return transformed_expr


def assign_variable(arguments_str, variables):
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


def compute_var_operations(arguments_str, variables) -> list:
    var_list = re.findall(r"[\w]+", arguments_str, flags=re.IGNORECASE)
    issue_counter = 0
    arguments_lst = arguments_str.strip(" ").split(" ")

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
        arguments_lst = transform_into_expression(" ".join(arguments_lst), variables)
        return arguments_lst


def compute_expression(math_expression):
    # math_expression = prioritized_computation(math_expression)  # turned of for the stage #6 as no prioritized operations for now
    if len(math_expression) < 3:
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
            expression_list = transform_into_expression(arguments_str, variables)
            if expression_list:
                expression_list = deque(expression_list)
                result = compute_expression(expression_list)
                print(result)
            else:
                pass


if __name__ == '__main__':
    main()
