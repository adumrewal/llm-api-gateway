from logzero import logger

from heimdall.core.clients.azure_openai.client import AzureOpenAIClient
from heimdall.core.clients.bedrock_claude.client import BedrockClaudeClient
from heimdall.core.clients.openai.client import OpenAIClient

from heimdall.typing import (
    BaseClient,
    ClientCallDataModel,
    ClientsEnum,
)


class LLMRouter:
    def __init__(self) -> None:
        self.openai_client = OpenAIClient()
        self.azure_openai_client = AzureOpenAIClient()
        self.bedrock_claude_client = BedrockClaudeClient()
    
    def model_call(self, data_model: ClientCallDataModel) -> str:
        for preference in data_model.preference:
            client: BaseClient | None = None
            if preference == ClientsEnum.openai:
                client = self.openai_client
            elif preference == ClientsEnum.azure_openai:
                client = self.azure_openai_client
            elif preference == ClientsEnum.bedrock_claude:
                client = self.bedrock_claude_client
            else:
                raise Exception("Invalid model preference")
            
            try:
                return self.client_call(client, data_model)
            except Exception as e:
                logger.error(f"Error calling {preference}: {e}")
        raise Exception("No model available")
    
    def client_call(self, client: BaseClient, data_model: ClientCallDataModel) -> str:
        return client.api_call(
            model_name=data_model.name_model,
            system_prompt=data_model.system_prompt,
            user_prompt=data_model.user_prompt,
            json_response=data_model.json_response,
            temperature=data_model.temperature,
            max_tokens=data_model.max_tokens,
        )