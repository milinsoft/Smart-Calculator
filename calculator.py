import re

from collections import deque


# done
def handle_command(command: dict(description="special command'/help' or '/exit'", type=str)):
    if command == "/exit":
        print("Bye!")
        exit()
    elif command == "/help":
        print("""The program calculates a given expression.\nAcceptable math operations: '+', '-', '/', '*', '^'
Additional functionality: you can use braces'( )' and variables. 
Variables are case-sensetive, 'a' and 'A' is not the same, and can contain only latin letters.
To assign a variable use the syntax like: a = 1 """)
    else:
        print("Unknown command")


# done
def is_invalid_expression(expression_string: str) -> bool:
    if any([expression_string[-1] in {"+", "-", "/", "*"}, "**" in expression_string, "//" in expression_string]):
        return True
    if re.search(r"[^\w^\+\-/\*= \(\)]", expression_string):
        return True
    return False


# done
def space_delimited_format(expression: str) -> str:
    if re.search(r"\+", expression):
        expression = re.sub(r"\+", r" + ", expression)
    if re.search(r"-", expression):
        expression = re.sub(r"-", r" - ", expression)
    if re.search(r"/", expression):
        expression = re.sub(r"/", r" / ", expression)
    if re.search(r"\*", expression):
        expression = re.sub(r"\*", r" * ", expression)
    if re.search(r"\(", expression):
        expression = re.sub(r"\(", r"( ", expression)
    if re.search(r"\)", expression):
        expression = re.sub(r"\)", r" )", expression)
    if re.search(r"\^", expression):
        expression = re.sub(r"\^", r" ^ ", expression)
    return expression


def repetitive_signs_amendment(expression_string) -> str:
    if re.search(r"\+-", expression_string):
        expression_string = re.sub(r"\+-", "-", expression_string)
    if re.search(r"-\+", expression_string):
        expression_string = re.sub(r"-\+", "-", expression_string)
    if re.search(r"\+{2,}", expression_string):
        expression_string = re.sub(r"\+{2,}", "+", expression_string)
        # replacing all minuse sequences with + or - based on their meaning
    if re.search(r"-{2,}", expression_string):
        if len(re.search(r"-{2,}", expression_string).group()) % 2 == 0:
            expression_string = re.sub(r"-{2,}", "+", expression_string)
        else:
            expression_string = re.sub(r"-{2,}", "-", expression_string)
    if re.search(r"\s+", expression_string):
        expression_string = re.sub(r"\s+", " ", expression_string)

    return expression_string


def braces_balance(expression_string) -> bool:
    braces = deque()
    if "(" in expression_string or ")" in expression_string:
        for symbol in expression_string:
            if symbol == "(":
                braces.append(symbol)
            elif symbol == ")":
                if not braces:
                    return False
                else:
                    braces.popleft()
    if len(braces) != 0:
        return False
    return True


def transform_into_expression(expression_string: str, variables: "empty dict to fill out, storing variables") -> str:
    # expression with variable(s) case

    if re.search(r"[a-z]+", expression_string, flags=re.IGNORECASE):
        return handle_variables(expression_string, variables)


    # numeric expression case
    elif re.search(r"\A[-+]?((\w+\s*[+-/*^)(\s]+\s*)*\w*)*", expression_string):
        if braces_balance(expression_string):
            expression_string = repetitive_signs_amendment(expression_string)
            expression_string = space_delimited_format(expression_string)
            return expression_string
        else:
            print("Invalid expression")
    else:
        print("Invalid expression")


def handle_variables(user_input, variables: dict) -> str:
    expr_template = re.compile(r"\A[-+]?(\w+\s*[+-/*)(\s]+\s*)*")
    # assignment
    if re.search(r"=", user_input):  # errors will be checked later
        assign_variable(user_input, variables)
       # print variable's value
    elif re.match(r"\A\s*[a-z]+$", user_input, flags=re.IGNORECASE):
        if user_input in variables.keys():
            print(variables[user_input])
        else:
            print("Unknown variable")
    # replacing variables with their values:
    elif re.match(expr_template, user_input):
        expression_str = replace_var_with_value(user_input, variables)
        if expression_str:
            return transform_into_expression(expression_str, variables)


# done
def assign_variable(user_input: str, variables: dict):
    var_ass_template = re.compile(r"\A\s*[a-z]+\s*=\s*([a-z]+|[\d]+)\s*$", flags=re.IGNORECASE)
    if re.match(var_ass_template, user_input):
        var, val = re.split(r"\s*=\s*", user_input.replace(" ", ""))
        # assignment from scratch
        if val.isnumeric():
            variables[var] = val
        # reassignment
        elif val in variables.keys():
            variables[var] = variables[val]
        # error
        else:
            print("Unknown variable")
    else:
        print("Invalid assignment")


# done
def replace_var_with_value(user_input, variables) -> str:
    var_list = re.findall(r"[\w]+", user_input, flags=re.IGNORECASE)
    arguments_lst = user_input.split(" ")
    """test just this function with the complex variable + int expression"""
    for i in range(int(len(arguments_lst))):
        if arguments_lst[i] in var_list:
            if arguments_lst[i] in variables.keys():
                arguments_lst[i] = str(variables[arguments_lst[i]])
            else:
                if arguments_lst[i].isdigit():
                    arguments_lst[i] = str(arguments_lst[i])
                else:
                    print("Unknown variable")
                    break
    return " ".join(arguments_lst)


def postfix_algorigm(str_expression) -> str:
    """ add explanation"""
    priority = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    str_expression = str_expression.replace("(", "( ").replace(")", " )")
    infix_tokens = str_expression.split(" ")
    op_stack = deque()
    postfix = deque()
    for x in infix_tokens:
        if x.isdigit():
            postfix.append(x)
        elif x == "(":
            op_stack.append(x)
        elif x == ")":
            while op_stack:
                if op_stack[-1] != "(":
                    postfix.append(op_stack.pop())
                else:
                    op_stack.pop()
                    break
        elif x in {'+', '-', '*', '/', '^'}:
            if op_stack:
                # re-write this condition in such a way to make sure that operator is poped if it has both equal or less priority than current stack head
                if op_stack[-1] == "(":
                    op_stack.append(x)
                elif priority[x] <= priority[op_stack[-1]]:
                    postfix.append(op_stack.pop())
                    op_stack.append(
                        x)  # while operator with greater priority pused to the postfix queue, the operator with lower priotiry still needs to be appended
                else:
                    op_stack.append(x)
            else:  # if not op_stack
                op_stack.append(x)
    while op_stack:
        postfix.append(op_stack.pop())
    return " ".join(postfix)


# done
def postfix_computation(postfix_expression: dict(description="A expression_string expression in postfix format", type=str)) -> int:
    calculated_expression = deque()
    for x in postfix_expression.split(" "):
        if x.isdigit():
            calculated_expression.append(x)
        elif x in {"+", "-", "*", "/", "^"}:
            if x == "+":
                arg2 = int(calculated_expression.pop())
                arg1 = int(calculated_expression.pop())
                calculated_expression.append(arg1 + arg2)
            elif x == "-":
                arg2 = int(calculated_expression.pop())
                arg1 = int(calculated_expression.pop())
                calculated_expression.append(arg1 - arg2)
            elif x == "*":
                arg2 = int(calculated_expression.pop())
                arg1 = int(calculated_expression.pop())
                calculated_expression.append(arg1 * arg2)
            elif x == "/":
                arg2 = int(calculated_expression.pop())
                arg1 = int(calculated_expression.pop())
                calculated_expression.append(arg1 / arg2)
            elif x == "^":
                arg2 = int(calculated_expression.pop())
                arg1 = int(calculated_expression.pop())
                calculated_expression.append(arg1 ** arg2)
    return calculated_expression[-1]


def main():
    variables = dict()
    while True:
        user_input = input().strip()  # removing all extra spaces on both sides of input
        if not user_input:
            continue
        elif user_input.startswith("/"):
            handle_command(user_input)
        elif re.match(r"\A[-+]?\d+$", user_input):  # single number/digit case
            print(user_input.lstrip("+"))
        elif is_invalid_expression(user_input):
            print("Invalid expression")

        else:
            expression = transform_into_expression(user_input, variables)
            if expression:
                postfix_format = postfix_algorigm(expression)
                result = postfix_computation(postfix_format)
                print(result)


if __name__ == '__main__':
    main()
    """annotations implemented: example of usage:
    print(handle_command.__annotations__) """
