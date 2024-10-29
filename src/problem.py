import sympy as sp
import os
from latex2sympy2 import latex2sympy
from typing import List, Dict
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Problem:
    name: str = ""
    description: str = ""
    level: int = 0
    difficulty: int = 0
    tags: List[str] = []
    content: str = ""

    expression: sp.Basic
    symbols: List[sp.Symbol]

    def __init__(self):
        self.steps = self.solve_steps()
        self.answer = self.solve()

    @staticmethod
    def generate_random_inputs() -> Dict:
        raise NotImplementedError("Subclasses must implement this method.")

    def solve_steps(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def solve(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def check(self, answer):
        try:
            answer = latex2sympy(answer)
        except Exception as e:
            print(e)
            return False
        return sp.simplify(answer).equals(self.evaluate_sym())

    def evaluate_sym(self):
        return sp.simplify(self.answer)

    def evaluate_num(self):
        return self.answer.evalf()

    def latex_expression(self):
        return sp.latex(self.expression)

    def latex_solution(self):
        return [sp.latex(step) for step in self.steps]

    def latex_answer(self):
        symbolic = sp.latex(self.evaluate_sym())
        numeric = sp.latex(self.evaluate_num())
        if numeric == symbolic:
            numeric = None
        return {"symbolic": symbolic, "numeric": numeric}

    def json(self):
        return {
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "difficulty": self.difficulty,
            "tags": self.tags,
            "expression": self.latex_expression(),
            "solution": self.latex_solution(),
            "answer": self.latex_answer(),
        }

    async def wrap_with_llm(self):
        model = "gpt-4o"
        system_prompt = (
            "You are a math teacher creating context-rich math problems. "
            "Each problem should have a real-world context. "
            "The raw expression and answer of the problem are given."
            "Please wrap the problem with meaningful context."
            "Please output one raw latex string only, the problem content."
        )
        user_prompt = (
            f"Generate one math problem with the following details:\n"
            f"{self.__repr__()}"
        )
        messages = [
            ChatCompletionSystemMessageParam(
                {"role": "system", "content": system_prompt}
            ),
            ChatCompletionUserMessageParam({"role": "user", "content": user_prompt}),
        ]

        max_retries = 3
        n_retries = 0
        while n_retries < max_retries:
            n_retries += 1
            content = None
            try:
                completion = client.chat.completions.create(
                    model=model, messages=messages
                )
                content = completion.choices[0].message.content
                if not content:
                    continue
                print(f"Generator: Generated {self.name} in {n_retries} retries.")
                self.content = content
                return
            except Exception as e:
                print(f"Generate Problem: Error: {e}, return: {content}")
                continue
        raise Exception("Failed to generate problems.")

    def __repr__(self):
        return f"""\
Problem: {self.name}
    Description: {self.description}
    Level: {self.level}
    Difficulty: {self.difficulty}
    Tags: {self.tags}
    Expression: {self.latex_expression()}
    Solution: {self.latex_solution()}
    Answer: {self.latex_answer()}
    Content: {self.content}\
"""
