import sympy as sp
import random
from typing import List


class SpRand:
    @staticmethod
    def integer_pos(max_val=100):
        return sp.Integer(sp.randprime(1, max_val))

    @staticmethod
    def integer(min_val=-100, max_val=100):
        return sp.Integer(sp.randprime(min_val, max_val))

    @staticmethod
    def rational_pos(max_val=100):
        return sp.Rational(sp.randprime(1, max_val), sp.randprime(1, max_val))

    @staticmethod
    def rational(min_val=-100, max_val=100):
        return sp.Rational(sp.randprime(min_val, max_val), sp.randprime(1, max_val))

    @staticmethod
    def constant_pos_with_difficulty():
        # first element is the function to generate the value
        # second element is the difficulty level [1-3]
        population = [
            (SpRand.integer_pos, 1),
            (SpRand.rational_pos, 2),
            (lambda: sp.pi, 2),
            (lambda: sp.E, 3),
        ]
        weights = [0.5, 0.3, 0.1, 0.1]

        choice = random.choices(population, weights=weights, k=1)[0]
        return choice[0](), choice[1]

    @staticmethod
    def constant_pos():
        population = [
            SpRand.integer_pos,
            SpRand.rational_pos,
            lambda: sp.pi,
            lambda: sp.E,
        ]
        weights = [0.5, 0.3, 0.1, 0.1]

        choice = random.choices(population, weights=weights, k=1)[0]
        return choice()

    @staticmethod
    def constant_with_difficulty():
        # first element is the function to generate the value
        # second element is the difficulty level [1-4]
        sign = random.choice([-1, 1])
        difficulty_offset = 1 if sign < 0 else 0
        value, difficulty = SpRand.constant_pos_with_difficulty()
        return sign * value, difficulty + difficulty_offset

    @staticmethod
    def constant():
        sign = random.choice([-1, 1])
        return sign * SpRand.constant_pos()

    @staticmethod
    def symbols(n: int) -> List[sp.Symbol]:
        SYMBOLS = "a b r s t u v w x y z".split()
        if n > len(SYMBOLS):
            raise ValueError("Not enough symbols to generate.")
        while True:
            selected = random.choices(SYMBOLS, k=n)
            if len(set(selected)) == n:
                break
        return list(map(sp.Symbol, selected))

    @staticmethod
    def function_with_difficulty():
        def pow(power, evaluate=False):
            return sp.Pow(sp.symbols("a"), power)

        def linear(symbol, evaluate=False):
            return SpRand.constant() * symbol

        # (function, difficulty)
        FUNCS = [
            (linear, 1),
            (sp.exp, 2),
            (sp.log, 2),
            (sp.sin, 3),
            (sp.cos, 3),
            (sp.tan, 3),
            (sp.cot, 4),
            (sp.sec, 4),
            (sp.csc, 4),
            (sp.atan, 5),
            (sp.asin, 5),
            (sp.acos, 5),
            (pow, 5),
        ]
        WEIGHTS = [1 / 13] * 13
        return random.choices(FUNCS, weights=WEIGHTS, k=1)[0]
