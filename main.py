import src.differential as diff
import asyncio


async def main():
    # Select a problem class
    problem_class = diff.DiffConstant
    # Generate raw problem with CAS
    inputs = problem_class.generate_random_inputs()
    problem = problem_class(**inputs)
    # Wrap the problem content with LLM
    await problem.wrap_with_llm()
    # Display the problem
    print(problem)


if __name__ == "__main__":
    asyncio.run(main())
