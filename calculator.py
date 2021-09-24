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



        """single argument case (NEED TO RE-WRITE)"""
    elif re.search(r"[-+]?\d+$", string):
        return str_as_lst
            #print(str_as_lst)



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


if __name__ == '__main__':
    while True:
        arguments_str = input()
        #arguments_str = "100 +++++ 1 -- 10 --- 2 * 10"
        if arguments_str.startswith("/"):
            handle_command(arguments_str)
        elif len(arguments_str) == 0:
            continue
        else:
            if not arguments_str[-1].isnumeric():
                print("Invalid expression")

            else:
                expression_list = transform_into_expression(arguments_str)
                #print(eval(expression))  # this is a great build-in method to calculate the expression, but I need to try implement mine
                if len(expression_list) == 1:
                    print(expression_list[0])
                else:
                    expression_list = deque(expression_list)
                    result = compute_expression(expression_list)
                    print(result)

