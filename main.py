from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
import asyncio

import src.differential as diff
from src.differential import problem_classes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/topic", response_model=Any)
def get_topics():
    topics = [{"id": id, "name": problem_classes[id].name} for id in problem_classes]
    return topics


@app.get("/problem/{topic_id}")
async def generate_problem(topic_id: int):
    if topic_id not in problem_classes:
        raise HTTPException(status_code=404, detail="Invalid topic ID")

    problem_class = problem_classes[topic_id]

    inputs = problem_class.generate_random_inputs()
    problem = problem_class(**inputs)
    await problem.wrap_with_llm()
    return problem.json()


async def main():
    # Select a problem class
    problem_class = diff.DiffProductVariable
    # Generate raw problem with CAS
    inputs = problem_class.generate_random_inputs()
    problem = problem_class(**inputs)
    # Wrap the problem content with LLM
    await problem.wrap_with_llm()
    # Display the problem
    print(problem)


if __name__ == "__main__":
    asyncio.run(main())
