import re
import operator

from collections import deque


class Commands:
    @staticmethod
    def handle_command(command):
        if command == "/exit":
            print("Bye!")
            exit()
        elif command == "/help":
            print("""\nThe program calculates a given expression.
1. Acceptable math expressions: '+', '-', '/', '*', '^'
2. Additional functionality: you can use braces'( )' and variables.
3. Variables are case-sensetive, 'a' and 'A' is not the same, and can contain only latin letters.
4. To assign a variable use the syntax like: a = 1 \n""")
        else:
            print("Unknown command")


class MathExpression:
    def __init__(self, expression):
        self.expression = expression

    def compute_expression(self):
        if re.match(r"\A\s*[+-]?\d+$", self.expression):
            print(self.expression.lstrip("+"))
        elif re.search(r"\A[-+]?((\d+\s*[+-/*^)(\s]+\s*)*\d*)*", self.expression):
            self.postfix_from_infix()
            result = self.postfix_computation()
            print(result)
        else:
            print("Invalid Expression")

    def postfix_from_infix(self):
        """ add explanation"""
        priority = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        self.expression = self.expression.replace("(", "( ").replace(")", " )")
        infix_tokens = self.expression.split()
        op_stack, postfix = deque(), deque()
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
                # re-write this condition in such a way to make sure that operator is poped if it has both equal or less priority than current stack head
                try:
                    if priority[x] <= priority[op_stack[-1]]:
                        postfix.append(op_stack.pop())
                except(KeyError, IndexError):
                    op_stack.append(x)
                else:
                    op_stack.append(x)
        while op_stack:
            postfix.append(op_stack.pop())
        self.expression = " ".join(postfix)

    def postfix_computation(self):
        ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv, "^": operator.xor}
        calculated_expression = deque()
        for x in self.expression.split():
            if x.isdigit():
                calculated_expression.append(x)
            elif x in ops:
                arg2 = int(calculated_expression.pop())
                arg1 = int(calculated_expression.pop())
                try:
                    calculated_expression.append(ops[x](arg1, arg2))
                except ZeroDivisionError:
                    print("Division by zero is forbidden. Please try again.")
                    return main()
        return calculated_expression[-1]


class SmartCalculator(MathExpression):
    """ calculator reads the expression validates and evaluates it"""

    def is_valid_expression(self):
        # check for invalid symbols
        def has_invalid_symbols():
            return any([self.expression[-1] in {"+", "-", "/", "*"},
                        "**" in self.expression, "//" in self.expression,
                        "==" in self.expression,
                        re.search(r"[^\w^+-/*= ()\s+]", self.expression)])

        def has_braces_imbalance():
            if any(["(" in self.expression, ")" in self.expression]):
                braces = 0
                for symbol in self.expression:
                    if symbol == "(":
                        braces += 1
                    elif symbol == ")":
                        braces -= 1
                return braces != 0

        return not any([has_invalid_symbols(), has_braces_imbalance()])

    def expression_formatter(self):
        def convert_duplicate_chars():
            self.expression = re.sub(r"(\+-)|(-\+)", "-", self.expression)
            if re.search(r"\d\s*\(", self.expression):  # special case for expressions like a(b+c)...
                self.expression = re.sub(r"\(", r"* (", self.expression)
            self.expression = re.sub(r"\+{2,}", "+", self.expression)
            # replacing all minuse sequences with + or - based on their meaning
            if re.search(r"-{2,}", self.expression):
                sign = "+" if len(re.search(r"-{2,}", self.expression).group()) % 2 == 0 else "-"
                self.expression = re.sub(r"-{2,}", sign, self.expression)

        def divide_by_space():
            ops = {"+", "-", "/", "*", "(", ")", "^"}
            for x in self.expression:
                if x in ops:
                    self.expression = self.expression[0] + self.expression[1::].replace(x, " " + x + " ")  # this allows to fix bugs while inputing "+1 /-1"
            self.expression = re.sub(r"\s{2,}", " ", self.expression)
        convert_duplicate_chars()
        divide_by_space()

    def line_scanner(self):
        if self.is_valid_expression():
            self.expression_formatter()
            math_expression = ExpWithVariables(self.expression)
            return math_expression.compute_expression()
        else:
            print("Invalid Expression")


class ExpWithVariables(MathExpression):
    variables = {}

    def compute_expression(self):
        if self.is_assignment():
            return self.assign_variable()
        else:
            self.expression = self.replace_var_with_value()
        super().compute_expression()

    def is_assignment(self):
        return re.search(r"=", self.expression)

    def assign_variable(self):
        var_ass_template = re.compile(r"\A\s*[a-z]+\s*=\s*([a-z]+|[\d]+)\s*$", flags=re.IGNORECASE)
        if re.match(var_ass_template, self.expression):
            var, val = re.split(r"\s*=\s*", self.expression.replace(" ", ""))
            # assignment from scratch
            if val.isnumeric():
                self.variables[var] = int(val)
            # reassignment
            else:
                try:
                    self.variables[var] = self.variables[val]
                except KeyError:
                    print("Unknown variable")
        else:
            print("Invalid assignment")

    # replacing vars with their values:
    def replace_var_with_value(self):
        var_list = re.findall(r"[a-z]+", self.expression, flags=re.IGNORECASE)
        arguments_lst = self.expression.split()
        for i in range(int(len(arguments_lst))):
            if arguments_lst[i] in var_list and arguments_lst[i].isalpha():
                try:
                    arguments_lst[i] = str(self.variables[arguments_lst[i]])
                except KeyError:
                    print("Unknown variable")
                    return main()
        return " ".join(arguments_lst)


def main():
    while True:
        user_input = input().strip()
        if not user_input:
            continue
        elif user_input[0] == "/":
            Commands.handle_command(user_input)
        else:
            expression = SmartCalculator(user_input)
            expression.line_scanner()


if __name__ == '__main__':
    main()
