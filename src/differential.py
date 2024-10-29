import random
import sympy as sp
from typing import Union, List

from src.problem import Problem
from src.utils import SpRand


class DiffConstant(Problem):
    name = "Derivative of a Constant"
    description = "Calculate the derivative of a constant with respect to a variable."
    tags = ["differentiation", "basic", "constant"]

    def __init__(
        self,
        const_value: Union[sp.Integer, sp.Rational],
        level: int = 1,
        difficulty: int = 1,
    ):
        self.level = level
        self.difficulty = difficulty
        self.symbols = sp.symbols("x,")
        self.expression = sp.Derivative(const_value, self.symbols[0], evaluate=False)
        super().__init__()

    @staticmethod
    def generate_random_inputs():
        const_value, difficulty = SpRand.constant_with_difficulty()
        return {"const_value": const_value, "level": 1, "difficulty": difficulty}

    def solve_steps(self):
        constant = sp.symbols("C")
        derivative_expr = sp.Derivative(constant, *self.symbols)
        equation = sp.Eq(derivative_expr, 0)
        return [equation]

    def solve(self):
        return self.expression.doit()


class DiffBasicFunction(Problem):
    name = "Derivative of a basic Function"
    description = "Calculate the derivative of a function with respect to a variable."
    tags = ["differentiation", "basic", "function"]

    def __init__(self, func_class, level: int = 1, difficulty: int = 1):
        self.level = level
        self.difficulty = difficulty
        self.symbols = sp.symbols("x,")
        self.expression = sp.Derivative(
            func_class(*self.symbols), *self.symbols, evaluate=False
        )
        super().__init__()

    @staticmethod
    def generate_random_inputs():
        # (function, level, difficulty)
        def pow(power):
            return sp.Pow(sp.symbols("a"), power)

        FUNCS = [
            (sp.exp, 1, 4),
            (sp.log, 1, 5),
            (sp.sin, 1, 5),
            (sp.cos, 1, 5),
            (sp.tan, 1, 5),
            (sp.cot, 2, 1),
            (sp.sec, 2, 2),
            (sp.csc, 2, 2),
            (sp.atan, 2, 3),
            (sp.asin, 2, 4),
            (sp.acos, 2, 4),
            (pow, 2, 5),
        ]
        WEIGHTS = [1 / 12] * 12

        func, level, difficulty = random.choices(FUNCS, weights=WEIGHTS, k=1)[0]
        return {"func_class": func, "level": level, "difficulty": difficulty}

    def solve_steps(self):
        equation = sp.Eq(self.expression, self.solve())
        return [equation]

    def solve(self):
        return self.expression.doit()


class DiffMulScalar(Problem):
    name = "Derivative of a variable with Coefficient"
    description = "Calculate the derivative of a variable with a coefficient."
    tags = ["differentiation", "basic", "coefficient"]

    def __init__(
        self,
        expr,
        coefficient: Union[sp.Integer, sp.Rational],
        symbols: List[sp.Symbol],
        level: int = 1,
        difficulty: int = 1,
    ):
        self.level = level
        self.difficulty = difficulty
        self.symbols = symbols
        self.expression = sp.Derivative(coefficient * expr, symbols[0], evaluate=False)

        self.coefficient = coefficient
        self.expr = expr
        super().__init__()

    @staticmethod
    def generate_random_inputs():
        coefficient, difficulty = SpRand.constant_with_difficulty()
        symbols = SpRand.symbols(2)
        return {
            "expr": symbols[1],
            "coefficient": coefficient,
            "symbols": symbols,
            "level": 3,
            "difficulty": difficulty,
        }

    def solve_steps(self):
        equivalent = sp.Mul(
            self.coefficient, sp.Derivative(self.expr, self.symbols[0]), evaluate=False
        )
        return [sp.Eq(self.expression, equivalent, evaluate=False)]

    def solve(self):
        return self.expression.doit()


class DiffAdd(Problem):
    name = "Derivative of a Sum of Variables"
    description = "Calculate the derivative of a sum of variables."
    tags = ["differentiation", "basic", "sum"]

    def __init__(
        self,
        expr1,
        expr2,
        symbols: List[sp.Symbol],
        sign: int,
        level: int = 1,
        difficulty: int = 1,
    ):
        self.level = level
        self.difficulty = difficulty
        self.symbols = symbols
        self.sign = sign
        self.expression = sp.Derivative(
            sp.Add(expr1, sign * expr2, evaluate=False), symbols[0], evaluate=False
        )

        self.expr1 = expr1
        self.expr2 = expr2
        super().__init__()

    @staticmethod
    def generate_random_inputs():
        symbols = SpRand.symbols(3)
        sign = random.choice([-1, 1])
        return {
            "expr1": symbols[1],
            "expr2": symbols[2],
            "symbols": symbols,
            "sign": sign,
            "level": 3,
            "difficulty": -min(sign, 0) + 4,
        }

    def solve_steps(self):
        equivalent = sp.Derivative(
            self.expr1, self.symbols[0]
        ) + self.sign * sp.Derivative(self.expr2, self.symbols[0])
        return [sp.Eq(self.expression, equivalent)]

    def solve(self):
        return self.expression.doit()


class DiffProduct(Problem):
    name = "Derivative of a Product"
    description = "Calculate the derivative of a product of two functions."
    tags = ["differentiation", "product rule"]

    def __init__(self, expr1, expr2, symbols, level: int = 4, difficulty: int = 1):
        self.level = level
        self.difficulty = difficulty
        self.symbols = symbols
        self.expr1 = expr1
        self.expr2 = expr2
        self.expression = sp.Derivative(expr1 * expr2, symbols[0], evaluate=False)
        super().__init__()

    def solve_steps(self):
        derivative1 = sp.Derivative(self.expr1, self.symbols[0])
        derivative2 = sp.Derivative(self.expr2, self.symbols[0])
        product_rule = derivative1 * self.expr2 + self.expr1 * derivative2
        return [sp.Eq(self.expression, product_rule)]

    def solve(self):
        return self.expression.doit()


class DiffProductVariable(DiffProduct):
    name = "Derivative of a Product with Variables"
    description = "Calculate the derivative of a product of two variables."
    tags = ["differentiation", "product rule", "variables"]

    @staticmethod
    def generate_random_inputs():
        symbols = SpRand.symbols(3)
        expr1 = symbols[1]
        expr2 = symbols[2]
        return {
            "expr1": expr1,
            "expr2": expr2,
            "symbols": symbols,
            "level": 4,
            "difficulty": random.randint(1, 2),
        }


class DiffQuotient(Problem):
    name = "Derivative of a Quotient"
    description = "Calculate the derivative of a quotient of two functions."
    tags = ["differentiation", "quotient rule"]

    def __init__(self, expr1, expr2, symbols, level: int = 4, difficulty: int = 1):
        self.level = level
        self.difficulty = difficulty
        self.symbols = symbols
        self.expr1 = expr1
        self.expr2 = expr2
        self.expression = sp.Derivative(expr1 / expr2, symbols[0], evaluate=False)
        super().__init__()

    def solve_steps(self):
        derivative1 = sp.Derivative(self.expr1, self.symbols[0])
        derivative2 = sp.Derivative(self.expr2, self.symbols[0])
        quotient_rule = (
            derivative1 * self.expr2 - self.expr1 * derivative2
        ) / self.expr2**2
        return [sp.Eq(self.expression, quotient_rule)]

    def solve(self):
        return self.expression.doit()


class DiffQuotientVariable(DiffQuotient):
    name = "Derivative of a Quotient with Variables"
    description = "Calculate the derivative of a quotient of two variables."
    tags = ["differentiation", "quotient rule", "variables"]

    @staticmethod
    def generate_random_inputs():
        symbols = SpRand.symbols(3)
        expr1 = symbols[1]
        expr2 = symbols[2]
        return {
            "expr1": expr1,
            "expr2": expr2,
            "symbols": symbols,
            "level": 4,
            "difficulty": random.randint(3, 5),
        }


class DiffProductVariableMulScalar(Problem):
    name = "Derivative of a Product of Variable and Scalar"
    description = "Calculate the derivative of a product of a variable and a scalar."
    tags = ["differentiation", "product rule", "scalar"]

    def __init__(
        self, expr1, expr2, coefficient, symbols, level: int = 5, difficulty: int = 1
    ):
        self.level = level
        self.difficulty = difficulty
        self.symbols = symbols
        self.expression = sp.Derivative(
            coefficient * expr1 * expr2, symbols[0], evaluate=False
        )

        self.expr1 = expr1
        self.expr2 = expr2
        self.coefficient = coefficient
        super().__init__()

    @staticmethod
    def generate_random_inputs():
        symbols = SpRand.symbols(3)
        expr1 = symbols[1]
        expr2 = symbols[2]
        coefficient, difficulty = SpRand.constant_with_difficulty()
        return {
            "expr1": expr1,
            "expr2": expr2,
            "coefficient": coefficient,
            "symbols": symbols,
            "level": 4,
            "difficulty": int(difficulty / 2 + 0.5),
        }

    def solve_steps(self):
        step1 = DiffMulScalar(
            self.expr1 * self.expr2, self.coefficient, self.symbols
        ).solve_steps()
        step2 = DiffProduct(self.expr1, self.expr2, self.symbols).solve_steps()
        return step1 + step2

    def solve(self):
        return self.expression.doit()


class DiffQuotientVariableMulScalar(Problem):
    name = "Derivative of a Quotient of Variable and Scalar"
    description = "Calculate the derivative of a quotient of a variable and a scalar."
    tags = ["differentiation", "quotient rule", "scalar"]

    def __init__(
        self, expr1, expr2, coefficient, symbols, level: int = 5, difficulty: int = 1
    ):
        self.level = level
        self.difficulty = difficulty
        self.symbols = symbols
        self.expression = sp.Derivative(
            coefficient * expr1 / expr2, symbols[0], evaluate=False
        )
        self.expr1 = expr1
        self.expr2 = expr2
        self.coefficient = coefficient
        super().__init__()

    @staticmethod
    def generate_random_inputs():
        symbols = SpRand.symbols(3)
        expr1 = symbols[1]
        expr2 = symbols[2]
        coefficient, difficulty = SpRand.constant_with_difficulty()
        return {
            "expr1": expr1,
            "expr2": expr2,
            "coefficient": coefficient,
            "symbols": symbols,
            "level": 5,
            "difficulty": min(5, difficulty + 2),
        }

    def solve_steps(self):
        step1 = DiffMulScalar(
            self.expr1 / self.expr2, self.coefficient, self.symbols
        ).solve_steps()
        step2 = DiffQuotient(self.expr1, self.expr2, self.symbols).solve_steps()
        return step1 + step2

    def solve(self):
        return self.expression.doit()


class DiffChainRule(Problem):
    name = "Derivative of a Composite Function"
    description = (
        "Calculate the derivative of a composite function using the chain rule."
    )
    tags = ["differentiation", "chain rule"]

    def __init__(self, func, inner_func, symbols, level: int = 6, difficulty: int = 1):
        self.level = level
        self.difficulty = difficulty
        self.symbols = symbols
        self.func = func
        self.inner_func = inner_func
        self.expression = sp.Derivative(
            func(inner_func(symbols[0]), evaluate=False), symbols[0], evaluate=False
        )
        super().__init__()

    @staticmethod
    def generate_random_inputs():
        symbols = sp.symbols("x,")
        inner_func, difficulty1 = SpRand.function_with_difficulty()
        func, difficulty2 = SpRand.function_with_difficulty()
        return {
            "func": func,
            "inner_func": inner_func,
            "symbols": symbols,
            "level": 6,
            "difficulty": (difficulty1 + difficulty2) // 2,
        }

    def solve_steps(self):
        inner_derivative = sp.Derivative(
            self.inner_func(self.symbols[0]), self.symbols[0]
        )
        outer_derivative = (
            sp.Derivative(self.func(self.symbols[0]), self.symbols[0])
            .doit()
            .subs(self.symbols[0], self.inner_func(self.symbols[0]))
        )
        chain_rule = sp.Mul(outer_derivative, inner_derivative)
        step1 = sp.Eq(self.expression, chain_rule)
        step2 = sp.Eq(self.expression, chain_rule.doit())
        return [step1, step2]

    def solve(self):
        return self.expression.doit()
