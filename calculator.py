import re


from collections import deque


def transform_into_expression(string) -> list:
    """Splitting arguments and signs into the list"""
    str_as_lst = string.split(" ")
    if re.search(r"(([-\+]?)\d+( ?[-\+\*/]+ ?\d+)+)", string):
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
            # dict realization doesn't work

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
    math_expression = prioritized_computation(math_expression)
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
    expr_template = re.compile(r"(\A\w+(\s*[-\+*/]\s*\w+)+$)")
    """Print variable value scenario"""
    if re.match(r"\a[a-z]+$", arguments_str, flags=re.IGNORECASE):
        if arguments_str in variables.keys():
            print(variables[arguments_str])
        else:
            print("Unknown variable")

    elif re.search("=", arguments_str):
        var_assignment(arguments_str, variables)

    elif re.match(expr_template, arguments_str):
        expression_list = var_operations(arguments_str)
        expression_list = deque(expression_list)
        return expression_list


def var_assignment(arguments_str, variables):
    var_ass_template = re.compile(r"\A[a-z]+\s*=\s*\d+$", flags=re.IGNORECASE)
    if re.match(var_ass_template, arguments_str):
        """ scenario for var = int/float only """
        var, val = re.split(r"\s*=\s*", arguments_str)
        if val.isnumeric():
            variables[var] = val
        else:
            """reassignment"""
            if val in variables.keys():
                variables[var] = val
            else:
                print("Unknown variable")

    else:
        print("Invalid assignment")



def var_operations(arguments_str) -> list:
    var_list = re.findall(r"[a-z]+", arguments_str, flags=re.IGNORECASE)
    issue_counter = 0
    for v in var_list:
        if v not in variables.keys():
            issue_counter += 1
        if issue_counter != 0:
            print("Unknown variable")
        else:
            arguments_lst = arguments_str.split(" ")
            for vl in var_list:
                for i in range(len(arguments_str)):
                    if arguments_lst[i] == v and vl in variables.keys():
                        arguments_lst[i] = variables[vl]
            return arguments_lst


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
        elif arguments_str[0].isalpha():
            expression_list = var_handler(arguments_str, variables)
            """ if there is an assignment here, expression_list will have no value
            need to fix removing assigning stucture here"""

            if len(expression_list) == 1:
                print(expression_list[0].lstrip("+"))
            else:
                expression_list = deque(expression_list)
                result = compute_expression(expression_list)
                print(result)
        else:
            expression_list = transform_into_expression(arguments_str)
            #print(eval(expression))  # this is a great build-in method to calculate the expression, but I need to try implement mine
            if len(expression_list) == 1:
                print(expression_list[0].lstrip("+"))
            else:
                expression_list = deque(expression_list)
                result = compute_expression(expression_list)
                print(result)




# test with input like just 1 positive number
