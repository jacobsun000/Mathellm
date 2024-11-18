import os
from openai import AsyncClient as OpenAI


class Client:
    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4o",
        api_key: str = os.getenv("OPENAI_API_KEY", ""),
        api_url: str = os.getenv("OLLAMA_API_URL", "http://localhost:11434/v1"),
    ):
        self.provider = provider
        self.model = model
        if provider == "openai":
            self.client = OpenAI(api_key=api_key)
        elif provider == "ollama":
            self.client = OpenAI(api_key="ollama", base_url=api_url)
        else:
            raise ValueError(
                "Unsupported provider. Choose either 'openai' or 'ollama'."
            )

    async def chat(self, messages, max_retries: int = 3):
        for _ in range(max_retries):
            try:
                content = await self._chat(messages)
                if content:
                    return content
            except Exception as e:
                print(f"Chat: Error: {e}")
        raise Exception("Failed to generate response.")

    async def _chat(self, messages):
        completion = await self.client.chat.completions.create(
            model=self.model, messages=messages
        )
        return completion.choices[0].message.content
