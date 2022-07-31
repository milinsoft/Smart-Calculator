import re


class MathExpressionValidator:
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
    def is_float_without_decimal_part(val: (float, int)) -> bool:
        return val % 1 == 0
