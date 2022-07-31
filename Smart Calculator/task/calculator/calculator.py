import re
import operator

from collections import deque
from validators import MathExpression, MathExpressionFormatter
from special_commands import SpecialCommand


class SmartCalculator(MathExpression):
    variables = dict()

    def _is_assignment(self):
        return re.search(r"=", self.expression)

    def compute_expression(self):
        if self.is_valid_expression():

            expr = MathExpressionFormatter(self.expression)
            self.expression = expr.get_formatted_expression()

            if self._is_assignment():
                return self._assign_variable()
            else:
                # replacing variables with its values *if any
                self.expression = self._replace_var_with_value()

            if re.match(r"\A\s*[+-]?\d+$", self.expression):
                print(self.expression.lstrip("+"))  # strip head plus *if any, but leaving minus

            elif re.search(r"\A[-+]?((\d+\s*[+-/*^)(\s]+\s*)*\d*)*", self.expression):
                self._postfix_from_infix()  # converting from infix to postfix.
                result = self._postfix_computation()
                print(result)
            else:
                print("Invalid Expression")
        else:
            print("Invalid Expression")


    def _assign_variable(self):
        var_ass_template = re.compile(r"\A\s*[a-z]+\s*=\s*([a-z]+|[\d\.]+)\s*$", flags=re.IGNORECASE)
        if re.match(var_ass_template, self.expression):
            var, val = re.split(r"\s*=\s*", self.expression.replace(" ", ""))  # searching in expression without spaces
            # assignment from scratch
            if val.isnumeric() or self.is_float(val):
                self.variables[var] = float(val)
            # reassignment
            else:
                try:
                    self.variables[var] = self.variables[val]
                except KeyError:
                    print("Unknown variable")
        else:
            print("Invalid assignment")

    def _postfix_from_infix(self):
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

    def _postfix_computation(self):
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

        result = float(calculated_expression[-1])  # the only remaining element in array

        if self.is_float_without_decimal_part(result):
            result: float = int(result)  # converting results like (-)x.00 to x
        else:
            result = round(result, 2)  # fixing cases like 0.3 + 0.6
        return result

    # replacing vars with their values:
    def _replace_var_with_value(self):
        var_list = re.findall(r"[a-z]+", self.expression, flags=re.IGNORECASE)
        arguments_lst = self.expression.split()
        for i in range(int(len(arguments_lst))):
            if arguments_lst[i] in var_list:
                try:
                    arguments_lst[i] = str(self.variables[arguments_lst[i]])
                except KeyError:
                    print("Unknown variable")
                    return main()

        return " ".join(arguments_lst)


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
            math_expr.compute_expression()


def main():
    while True:
        user_input = input()
        UserInputProcessor.process_input(user_input)


if __name__ == '__main__':
    main()
