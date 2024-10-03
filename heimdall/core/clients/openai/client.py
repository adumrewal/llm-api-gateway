from openai import OpenAI, NotGiven

from heimdall.typing import BaseClient

OPENAI_API_KEY = ""


class OpenAIClient(BaseClient):
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def api_call(
        self,
        model_name: str,
        system_prompt: str,
        user_prompt: str,
        json_response: bool = False,
        temperature: float = 0,
        max_tokens: int = 2000,
    ) -> str:
        response = self.client.chat.completions.create(
            model=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=(
                {"type": "json_object"} if json_response else NotGiven
            ),
        )
        return response.choices[0].message.content
