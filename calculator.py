import re


from collections import deque


def handle_command(command:"reading string command starting with '/'") -> None:
    #print(handle_command.__annotations__)
    if command == "/exit":
        print("Bye!")
        exit()
    elif command == "/help":
        print("The program calculates a given expression, acceptable operations: '+', '-', '/', '*' ")
    else:
        print("Unknown command")



def space_delimited_format(user_expression:"") -> str:
    if re.search(r"\+", user_expression):
        user_expression = re.sub(r"\+", r" + ", user_expression)
    if re.search(r"-", user_expression):
        user_expression = re.sub(r"-", r" - ", user_expression)
    if re.search(r"/", user_expression):
        user_expression = re.sub(r"/", r" / ", user_expression)
    if re.search(r"\*", user_expression):
        user_expression = re.sub(r"\*", r" * ", user_expression)
    if re.search(r"\(", user_expression):
        user_expression = re.sub(r"\(", r"( ", user_expression)
    if re.search(r"\)", user_expression):
        user_expression = re.sub(r"\)", r" )", user_expression)
    return user_expression


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
    elif re.search(r"\A[-+]?((\d+\s*[+-/*)(\s]+\s*)*\d*)*", string):
        """ this template take an expresion with already replaced variables with their values
        double or more * is not allowed, replace with ^ and add single * - rewrite regex"""
        """Splitting arguments and signs into the list"""
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


def handle_variables(arguments_str, variables) -> None:
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
        expression_str = replace_var_with_value(arguments_str, variables)
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


def replace_var_with_value(arguments_str, variables) -> str:
    var_list = re.findall(r"[\w]+", arguments_str, flags=re.IGNORECASE)
    issue_counter = 0
    arguments_lst = arguments_str.split(" ")
    """test just this function with the complex variable + int expression"""
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
                    op_stack.append(x)  # while operator with greater priority pused to the postfix queue, the operator with lower priotiry still needs to be appended
                else:
                    op_stack.append(x)
            else:  # if not op_stack
                op_stack.append(x)
    while op_stack:
        postfix.append(op_stack.pop())
    return " ".join(postfix)


def postfix_computation(postfix_expression) -> int:
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
        arguments_str = input().strip()  # removing all extra spaces on both sides of input
        if not arguments_str:
            continue
        elif arguments_str.startswith("/"):
            handle_command(arguments_str)
        else:
            expression = transform_into_expression(arguments_str, variables)
            if expression:
                expression = space_delimited_format(expression)
                postfix_format = postfix_algorigm(expression)
                result = postfix_computation(postfix_format)
                print(result)


if __name__ == '__main__':
    main()
