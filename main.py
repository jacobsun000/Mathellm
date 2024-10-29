import src.differential as diff


async def main():
    inputs = diff.DiffConstant.generate_random_inputs()
    problem = diff.DiffConstant(**inputs)
    await problem.wrap_with_llm()
    print(problem)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
