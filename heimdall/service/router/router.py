from typing import Optional

from logzero import logger

from heimdall.core.clients.azure_openai.client import AzureOpenAIClient
from heimdall.core.clients.bedrock_claude.client import BedrockClaudeClient
from heimdall.core.clients.openai.client import OpenAIClient

from heimdall.typing import (
    BaseClient,
    ClientCallDataModel,
    ClientsEnum,
    ModelNameEnum,
    model_client_mapping,
)


class LLMRouter:
    def __init__(self) -> None:
        self.openai_client = OpenAIClient()
        self.azure_openai_client = AzureOpenAIClient()
        self.bedrock_claude_client = BedrockClaudeClient()

    def _get_client(self, client_enum: ClientsEnum) -> BaseClient:
        if client_enum == ClientsEnum.openai:
            return self.openai_client
        elif client_enum == ClientsEnum.azure_openai:
            return self.azure_openai_client
        elif client_enum == ClientsEnum.bedrock_claude:
            return self.bedrock_claude_client
        else:
            raise Exception("Invalid client preference")

    def _model_call(self, data_model: ClientCallDataModel) -> str:
        for model_enum in data_model.preference:
            client_enum = model_client_mapping[model_enum]
            client = self._get_client(client_enum)

            try:
                return self.client_call(client, data_model, model_enum)
            except Exception as e:
                logger.error(f"Error calling {model_enum}: {e}")
        raise Exception("No model available")

    def client_call(
        self,
        client: BaseClient,
        data_model: ClientCallDataModel,
        model_enum: Optional[ModelNameEnum] = None,
    ) -> str:
        return client.api_call(
            model_name=(
                model_enum.value if model_enum else data_model.name_model
            ),
            system_prompt=data_model.system_prompt,
            user_prompt=data_model.user_prompt,
            json_response=data_model.json_response,
            temperature=data_model.temperature,
            max_tokens=data_model.max_tokens,
        )

    async def model_call(self, data_model: ClientCallDataModel) -> str:
        return self._model_call(data_model)
