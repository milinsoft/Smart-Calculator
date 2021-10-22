import re

from collections import deque


class MathExpression():
    def __init__(self, expression):
        self.expression = expression

    def math_expr_handler(self):
        if re.match(r"\A[-+]?\d+$", self.expression):
            print(self.expression.lstrip("+"))
        else:
            return self.compute_expression()

    def compute_expression(self):
        if re.search(r"\A[-+]?((\d+\s*[+-/*^)(\s]+\s*)*\d*)*", self.expression):
            self.expression = self.postfix_from_infix()
            self.expression = self.postfix_computation()
            print(self.expression)


    def postfix_from_infix(self):
        """ add explanation"""
        priority = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        self.expression = self.expression.replace("(", "( ").replace(")", " )")
        infix_tokens = self.expression.split(" ")
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

    def postfix_computation(self: dict(description="A expression_string expression in postfix format", type=str)) -> int:
        calculated_expression = deque()
        for x in self.expression.split(" "):
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


class SmartCalculator(MathExpression):

    """ calculator reads the expression validates and evaluates it"""

    def is_valid_expression(self):
        # check for invalid symbols
        def has_invalid_symbols(self):
            return any([self.expression[-1] in {"+", "-", "/", "*"}, "**" in self.expression, "//" in self.expression, "==" in self.expression, re.search(r"[^\w^\+\-/\*= \(\)\s+]", self.expression)])

        def has_braces_imbalance(self):
            if any(["(" in self.expression, ")" in self.expression]):
                braces = deque()
                for symbol in self.expression:
                    if symbol == "(":
                        braces.append(symbol)
                    elif symbol == ")":
                        if not braces:
                            return True
                        else:
                            braces.popleft()
                if len(braces) != 0:
                    return True
            return False

        if has_invalid_symbols(self):
            return False

        elif has_braces_imbalance(self):
            return False

        return True

    def expression_formatter(self):
        def convert_duplicate_chars(self):
            if re.search(r"\+-", self.expression):
                self.expression = re.sub(r"\+-", "-", self.expression)
            if re.search(r"-\+", self.expression):
                self.expression = re.sub(r"-\+", "-", self.expression)

            if re.search(r"\+{2,}", self.expression):
                  self.expression = re.sub(r"\+{2,}", "+", self.expression)
            # replacing all minuse sequences with + or - based on their meaning
            if re.search(r"-{2,}", self.expression):
                if len(re.search(r"-{2,}", self.expression).group()) % 2 == 0:
                    self.expression = re.sub(r"-{2,}", "+", self.expression)
                else:
                    self.expression = re.sub(r"-{2,}", "-", self.expression)

        def divide_by_space(self):
            if re.search(r"\+", self.expression):
                self.expression = self.expression[0] + re.sub(r"\+", r" + ", self.expression[1:])  # replacing only starting with second occurence to avoid changes in cases like "+1|-1"
            if re.search(r"-", self.expression):
                self.expression = self.expression[0] + re.sub(r"-", r" - ", self.expression[1:])
            if re.search(r"/", self.expression):
                self.expression = re.sub(r"/", r" / ", self.expression)
            if re.search(r"\*", self.expression):
                self.expression = re.sub(r"\*", r" * ", self.expression)
            if re.search(r"\(", self.expression):
                self.expression = re.sub(r"\(", r"( ", self.expression)
            if re.search(r"\)", self.expression):
                self.expression = re.sub(r"\)", r" )", self.expression)
            if re.search(r"\^", self.expression):
                self.expression = re.sub(r"\^", r" ^ ", self.expression)
            if re.search(r"\s+", self.expression):
                self.expression = re.sub(r"\s+", r" ", self.expression)  # replacing multiple spaces with one only

        convert_duplicate_chars(self)
        divide_by_space(self)

    def line_scanner(self):
        if Commands.is_command(self):
            return Commands.handle_command(self)

        else:

            if self.is_valid_expression():
                self.expression_formatter()

                if ExpWithVariables.is_expression_with_variable(self):
                    # Maybe It's time create a var object?
                    expression = ExpWithVariables(self.expression)
                    return expression.var_handler()

                else:
                    # else - this is a math expression
                    math_expression = MathExpression(self.expression)
                    return math_expression.math_expr_handler()
            else:
                print("Invalid Expression")

class Commands(SmartCalculator):

    def is_command(self):
        if self.expression[0] == "/":
            return True
        return False

    def handle_command(self):
        if self.expression == "/exit":
            print("Bye!")
            exit()
        elif self.expression == "/help":
            print("""\nThe program calculates a given expression.\nAcceptable math expressions: '+', '-', '/', '*', '^'
Additional functionality: you can use braces'( )' and variables.
Variables are case-sensetive, 'a' and 'A' is not the same, and can contain only latin letters.
To assign a variable use the syntax like: a = 1 \n""")
        else:
            print("Unknown command")

class ExpWithVariables(MathExpression):
    variables = {}

    expr_template = re.compile(r"\A[-+]?(\w+\s*[+-/*)(\s]+\s*)*")

    def compute_expression(self):
        # replacing vars with their values:
        def replace_var_with_value(self) -> str:
            var_list = re.findall(r"[\w]+", self.expression, flags=re.IGNORECASE)
            arguments_lst = self.expression.split(" ")
            """test just this function with the complex variable + int expression"""
            for i in range(int(len(arguments_lst))):
                if arguments_lst[i] in var_list:
                    if arguments_lst[i] in self.variables.keys():
                        arguments_lst[i] = str(self.variables[arguments_lst[i]])
                    else:
                        if arguments_lst[i].isdigit():
                            arguments_lst[i] = str(arguments_lst[i])
                        else:
                            print("Unknown variable")
                            break
            return " ".join(arguments_lst)
        self.expression = replace_var_with_value(self)
        super().compute_expression()


    def is_expression_with_variable(self):
        if re.search(r"[\+-]*[a-z]+", self.expression, flags=re.IGNORECASE):
            return True
        return False

    def assign_variable(self):
        var_ass_template = re.compile(r"\A\s*[a-z]+\s*=\s*([a-z]+|[\d]+)\s*$", flags=re.IGNORECASE)

        if re.match(var_ass_template, self.expression):
            var, val = re.split(r"\s*=\s*", self.expression.replace(" ", ""))
            # assignment from scratch
            if val.isnumeric():
                self.variables[var] = int(val)
            # reassignment
            elif val in self.variables.keys():
                self.variables[var] = self.variables[val]
            # error
            else:
                print("Unknown variable")
        else:
            print("Invalid assignment")


    def output_variable_value(self):
        # consider replacing with default values
        if self.expression.lstrip("+") in self.variables.keys():
            x = self.variables[self.expression.lstrip("+")]
            print(x)
        elif self.expression.lstrip("-") in self.variables.keys():
            x = self.variables[self.expression.lstrip("-")]
            print(f"-{x}")

        else:
            print("Unknown variable")


    """ function for var computation """


    def var_handler(self):

        def is_assignment_expression(self):
            if re.search(r"=", self.expression):
                return True
            return False

        def is_var_call(self):
            if re.match(r"\A[-|\+]?\s*[a-z]+$", self.expression, flags=re.IGNORECASE):
                return True
            return False


        if is_assignment_expression(self):
            return self.assign_variable()
        elif is_var_call(self):
            return self.output_variable_value()
        else:
            return self.compute_expression()


def main():
    while True:
        user_input = input().strip()
        if not user_input:
            continue
        else:
            expression = SmartCalculator(user_input)
            expression.line_scanner()


if __name__ == '__main__':
    main()
