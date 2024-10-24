import os

from openai import AzureOpenAI, NOT_GIVEN

from heimdall.typing import BaseClient

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2021-09-01")
AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT", "")


class AzureOpenAIClient(BaseClient):
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_API_ENDPOINT,
        )

    def api_call(
        self,
        model_name: str,
        system_prompt: str,
        user_prompt: str,
        json_response: bool = False,
        temperature: float = 0,
        max_tokens: int = 2000,
    ) -> str:
        # Azure OpenAI API expects model names without the "azure-" prefix
        if model_name.startswith("azure-"):
            model_name = model_name.replace("azure-", "", 1)

        response = self.client.chat.completions.create(
            model=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=(
                {"type": "json_object"} if json_response else NOT_GIVEN
            ),
        )
        return (
            response.choices[0].message.content or ""
            if response.choices
            else ""
        )
