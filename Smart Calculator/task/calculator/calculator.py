import re
import operator

from collections import deque
from validators import MathExpressionValidator
from special_commands import SpecialCommand


class SmartCalculator(MathExpressionValidator):
    variables = {}

    def calculate_expression(self):
        if not self.is_valid_expression():
            print("Invalid Expression")
        else:
            self.expression_formatter()
            return self.compute_expression()

    def _is_assignment(self):
        return re.search(r"=", self.expression)

    def assign_variable(self):
        var_ass_template = re.compile(r"\A\s*[a-z]+\s*=\s*([a-z]+|[\d\.]+)\s*$", flags=re.IGNORECASE)
        if re.match(var_ass_template, self.expression):
            var, val = re.split(r"\s*=\s*", self.expression.replace(" ", ""))  # searching in expression without spaces
            # assignment from scratch
            if val.isnumeric():
                self.variables[var] = int(val)
            elif self.is_float(val):
                self.variables[var] = float(val)
            # reassignment
            else:
                try:
                    self.variables[var] = self.variables[val]
                except KeyError:
                    print("Unknown variable")
        else:
            print("Invalid assignment")

    def compute_expression(self):
        if self._is_assignment():
            return self.assign_variable()
        else:
            self.expression = self.replace_var_with_value()
        
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
            if x.isdigit() or self.is_float(x):
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
        ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv, "^": operator.pow}
        calculated_expression = deque()

        for x in self.expression.split():

            if x.isdigit() or self.is_float(x):
                calculated_expression.append(x)

            elif x in ops:
                arg2 = float((calculated_expression.pop()))
                arg1 = float((calculated_expression.pop()))
                try:
                    calculated_expression.append(ops[x](arg1, arg2))
                except ZeroDivisionError:
                    print("Division by zero is forbidden. Please try again.")
                    return main()

        result = calculated_expression[-1]  # the only remaining element in array

        if self.is_float_without_decimal_part(result):
            result: float = int(result)  # converting results like (-)x.00 to x
        else:
            result = round(result, 2)  # fixing cases like 0.3 + 0.6
        return result

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

        def split_by_space():
            ops = {"+", "-", "/", "*", "(", ")", "^"}
            for x in self.expression:
                if x in ops:
                    self.expression = self.expression[0] + self.expression[1::].replace(x, " " + x + " ")  # this allows to fix bugs while inputing "+1 /-1"
            self.expression = re.sub(r"\s{2,}", " ", self.expression)
        convert_duplicate_chars()
        split_by_space()


class UserInputProcessor:

    @staticmethod
    def process_input(user_input):
        user_input = user_input.strip()

        if not user_input:
            return True  # exit function
        elif user_input[0] == '/':
            SpecialCommand.execute(user_input)
        else:
            math_expr = SmartCalculator(user_input)
            math_expr.calculate_expression()


def main():
    while True:
        user_input = input()
        UserInputProcessor.process_input(user_input)


if __name__ == '__main__':
    main()
