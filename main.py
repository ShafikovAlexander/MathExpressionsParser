from colorama import Fore

"""Returns priority of the operation"""


def get_priority(operator):
    if operator == "+" or operator == "-":
        return 1
    elif operator == "*" or operator == "/":
        return 2
    elif operator == "^":
        return 3
    else:
        return 0


"""Calculate parsed math expression"""


def calculate(parsed):
    if len(parsed) == 3:
        operator = parsed[0]
        left = calculate(parsed[1])
        right = calculate(parsed[2])

        if operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            return left / right
        elif operator == "^":
            return left ** right
        else:
            raise RuntimeError("Unknown binary operator. Expected '+', '-', '*', '/', '^'")

    elif len(parsed) == 2:
        operator = parsed[0]
        right = calculate(parsed[1])
        if operator == "+":
            return +right
        elif operator == "-":
            return -right
        else:
            raise RuntimeError("Unknown unary operator. Expected '+', '-'")

    elif len(parsed) == 1:
        return float(parsed[0])

    else:
        raise RuntimeError("Unknown operations")


""" Parse math expression for the next calculation.
    Support next operators:
    binary - '+' '-' '*' '/' '^'
    unary - '+' '-'
    other - '(' ')'

    expr -- string with math expression.

"""


class Parser:
    def __init__(self, expr):
        self.expr = expr + "="
        self.pos = 0  # Current position in expression
        self.operators = ["+", "-", "/", "*", "^", "(", ")", "="]

    """Parse simple tokens, like numbers or operators and increment self.pos"""

    def _parse_token(self):

        if self.expr[self.pos].isnumeric():
            number = ""
            while self.expr[self.pos].isnumeric() or self.expr[self.pos] == '.':
                number += self.expr[self.pos]
                self.pos += 1
                if self.pos > len(self.expr) - 1:
                    break
            return number

        if self.expr[self.pos] in self.operators:
            operator = self.expr[self.pos]
            self.pos += len(self.expr[self.pos])
            return operator

        return None

    """Parse simple expressions and wrap them into list. 
       Can parse: numbers, unary operations and expressions in () """

    def _parse_simple_expression(self):
        token = self._parse_token()

        if token is None:
            raise RuntimeError("Invalid expression")

        if token == "(":
            result = self.parse()
            if self._parse_token() != ")":
                raise RuntimeError("Expected ) after (, but ) not found")
            return result  # expressions in ()

        if token[0].isnumeric():
            return [token]  # number

        return [token, self._parse_simple_expression()]  # unary operation

    """Parse binary operations. Binary operation contains:
       1)Left part - simple expression
       2)Operator
       3)Right part - simple expression.
       Since binary operations have different priority, 
       function parse left part of the operation and the operator.
       If current operator has lower or equal priority then maximum from previous
       it will return current left part of the expression"""

    def _parse_binary_expression(self, priority):
        left_part = self._parse_simple_expression()
        while True:
            operator = self._parse_token()
            prior = get_priority(operator)
            if prior <= priority:
                self.pos -= len(operator)
                return left_part
            right_part = self._parse_binary_expression(prior)
            left_part = [operator, left_part, right_part]

    """Public function for parsing expressions. Calls with priority 0"""

    def parse(self):
        return self._parse_binary_expression(0)

    """Parse and calculate result of the expression"""

    def calculate(self):
        parsed = self.parse()
        return calculate(parsed)


def test(expression, expected):
    parser = Parser(expression)
    calc = parser.calculate()
    if calc == expected:
        result = "OK"
        color = Fore.GREEN
    else:
        result = "WRONG"
        color = Fore.RED
    print(Fore.WHITE + "expression:{}={} expected:{}".format(expression, calc, expected))
    print(color + "Result:{}".format(result))


if __name__ == '__main__':
    pregeneratedTestFlag = input("Do you want to run pregenerated tests or test by yourself?\nType 1 or 2\n") == "1"
    if pregeneratedTestFlag:
        test("1+2", 3)
        test("1+2+3", 6)
        test("1+2+3*2", 9)
        test("1+2^2-5*2", -5)
        test("2*(2+3)", 10)
        test("2/2+3*(1+2*(1+2)^2-5)", 43)
        test("1.5+2", 3.5)
        test("0.5*2", 1)
        test("10+1254", 1264)
        test("+0+0.5", 0.5)
    else:
        while True:
            expr = input("Input mathematical expression. You can use this operators [+;-;/;*;^;()] and any numbers\n"
                         "Please do not use whitespaces in your expressions\nYour expression: ")
            expected = float(input("Input expected result of your expression: "))
            test(expr, expected)
            if input("press q if your want to stop program\n") == "q":
                break
