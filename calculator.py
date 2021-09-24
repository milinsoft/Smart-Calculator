import re


from collections import deque


def transform_into_expression(string) -> list:
    """Splitting arguments and signs into the list"""
    str_as_lst = string.split(" ")
    if re.search(r"(([-\+]?)\d+( ?[-\+\*/]+ ?\d+)+)", string):
        """looks like this regex doesnt work with mixed expression"""

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

        """single argument case (NEED TO RE-WRITE) or even remove"""


    #elif re.search(r"[-+]?\d+$", string):
    #    return str_as_lst


    else:
        print("Invalid expression")


def handle_command(command):
    if command == "/exit":
        print("Bye!")
        exit()
    elif command == "/help":
        print("The program calculates a given expression")
    else:
        print("Unknown command")


def prioritized_computation(math_expression):
    first_pr_operators = {"/", "*", "**"}
    for pr_operation in first_pr_operators:
        if pr_operation in math_expression:
            priority_index = math_expression.index(pr_operation)
            arg1 = int(math_expression.pop(math_expression[priority_index - 1]))  # minus one as we need the arg 1 before priority operator
            sign = math_expression.pop(math_expression[priority_index - 1])  # as arg1 already popped, now sign changed it's index
            arg2 = int(math_expression.pop(math_expression[priority_index - 1]))  # as sign already popped, now arg2 changed it's index
            if sign == "/":
                operation_result = arg1 / arg2
            elif sign == "*":
                operation_result = arg1 * arg2
            elif sign == "**":
                operation_result = arg1 ** arg2

            math_expression.insert(priority_index - 1, str(operation_result))
            return prioritized_computation(math_expression)
        else:
            return math_expression


# potentially merge top and not top calculations later on

def compute_expression(math_expression):
    # math_expression = prioritized_computation(math_expression)  # turned of for the stage #6 as no prioritized operations for now
    operators = {"-", "+"}
    if len(math_expression) < 3:
        return "".join(math_expression)
    else:
        arg1 = math_expression.popleft()
        sign = math_expression.popleft()
        arg2 = math_expression.popleft()
        arg1 = int(arg1)
        arg2 = int(arg2)

        if sign == "-":
            math_expression.appendleft(str(arg1 - arg2))
        elif sign == "+":
            math_expression.appendleft(str(arg1 + arg2))

        return compute_expression(math_expression)


def var_handler(arguments_str, variables):
    expr_template = re.compile(r"\A(\s*\w+\s*[-+*/]*\s*)+$")
    """Print variable value scenario"""
    if re.match(r"\A\s*[a-z]+$", arguments_str, flags=re.IGNORECASE):
        if arguments_str in variables.keys():
            print(variables[arguments_str])
        else:
            print("Unknown variable")
        """ASSIGNMENT SCENARIO"""
    elif re.search(r"=", arguments_str):
        var_assignment(arguments_str, variables)

        """ expression with variables """
    elif re.match(expr_template, arguments_str):
        expression_list = var_operations(arguments_str)
        if expression_list != 1:
            exp_str = " ".join(expression_list)
            transformed_expr = transform_into_expression(exp_str)
            return transformed_expr
        else:
            return 1


def var_assignment(arguments_str, variables):
    var_ass_template = re.compile(r"\A\s*[a-z]+\s*=\s*([a-z]+|[\d]+)\s*$", flags=re.IGNORECASE)
    if re.match(var_ass_template, arguments_str):

        """ scenario for var = int/float only """
        var, val = re.split(r"\s*=\s*", arguments_str.replace(" ", ""))
        var = var.strip(" ")
        val = val.strip(" ")
        if val.isnumeric():
            variables[var] = val
            return 0
        else:
            """reassignment"""
            if val in variables.keys():
                variables[var] = variables[val]
                return 0
            else:
                print("Unknown variable")


    elif re.match(r"\w+", arguments_str):
        print("Invalid identifier")
        return 1
    else:
        print("Invalid assignment")
        return 1



def var_operations(arguments_str) -> list:
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
    if issue_counter != 0:
        print("Unknown variable")
        return 1
    else:
        arguments_lst = transform_into_expression(" ".join(arguments_lst))
        #print(arguments_lst)
        return arguments_lst


def print_result(expression_list):
    if not expression_list:
        pass
    elif len(expression_list) == 1:
        print(expression_list[0].lstrip("+"))
    else:
        expression_list = deque(expression_list)
        result = compute_expression(expression_list)
        print(result)


if __name__ == '__main__':
    variables = dict()
    while True:
        arguments_str = input()
        #arguments_str = "100 +++++ 1 -- 10 --- 2 * 10"
        if len(arguments_str) == 0:
            continue
        elif arguments_str.startswith("/"):
            handle_command(arguments_str)
        elif arguments_str[-1] in {"+", "-", "/", "*"}:
            print("Invalid expression")


        elif arguments_str.lstrip()[0].isalpha():
            expr = var_handler(arguments_str, variables)
            if expr != 1:
                print_result(expr)
            else:
                continue
        else:
            expression_list = transform_into_expression(arguments_str)
            print_result(expression_list)


# test with input like just 1 positive number
