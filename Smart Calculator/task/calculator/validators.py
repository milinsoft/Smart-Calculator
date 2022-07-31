import re


class MathExpression:
    def __init__(self, expression):
        self.expression = expression

    def _ends_with_sign(self):
        return self.expression[-1] in ("+", "-", "/", "*")

    def _has_repitive_symbols(self):
        return any(("**" in self.expression,
                    "//" in self.expression,
                    "==" in self.expression)
                   )

    def _has_special_sybmols(self):
        """ returns false if expression contrains any sybmols except alphanumeric, braces, digits and whitespaces"""
        return re.search(r"[^\w^+-/*= ()\s+]", self.expression)

    def _has_braces_imbalance(self):
        return self.expression.count('(') != self.expression.count(')')

    def is_valid_expression(self):
        return not any((self._ends_with_sign(),
                        self._has_repitive_symbols(),
                        self._has_special_sybmols(),
                        self._has_braces_imbalance(),
                        ))

    @staticmethod
    def is_float(val: str) -> bool:
        try:
            float(val)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float_without_decimal_part(val: (str, float, int)) -> bool:
        return float(val) % 1 == 0


class MathExpressionFormatter:
    def __init__(self, expression):
        self.expression = expression

    def _convert_duplicate_chars(self):
        self.expression = re.sub(r"(\+-)|(-\+)", "-", self.expression)
        if re.search(r"\d\s*\(", self.expression):  # special case for expressions like a(b+c)...
            self.expression = re.sub(r"\(", r"* (", self.expression)
        self.expression = re.sub(r"\+{2,}", "+", self.expression)
        # replacing all minuse sequences with + or - based on their meaning
        if re.search(r"-{2,}", self.expression):
            sign = "+" if len(re.search(r"-{2,}", self.expression).group()) % 2 == 0 else "-"
            self.expression = re.sub(r"-{2,}", sign, self.expression)

    def _split_by_space(self):
        ops = {"+", "-", "/", "*", "(", ")", "^"}
        for x in self.expression:
            if x in ops:
                self.expression = self.expression[0] + self.expression[1::].replace(x, " " + x + " ")  # this allows to fix bugs while inputing "+1 /-1"
        self.expression = re.sub(r"\s{2,}", " ", self.expression)

    def get_formatted_expression(self):
        self._convert_duplicate_chars()
        self._split_by_space()
        return self.expression
