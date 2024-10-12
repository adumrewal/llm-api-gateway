from enum import Enum
from pydantic import BaseModel, Field


class BaseClient:
    def __init__(self) -> None:
        pass

    def api_call(
        self,
        model_name: str,
        system_prompt: str,
        user_prompt: str,
        json_response: bool = False,
        temperature: float = 0,
        max_tokens: int = 2000,
    ) -> str:
        raise NotImplementedError


class ClientsEnum(str, Enum):
    openai = "openai"
    azure_openai = "azure_openai"
    bedrock_claude = "bedrock_claude"


class ModelNameEnum(str, Enum):
    gpt_3_5_turbo = "gpt-3.5-turbo"
    gpt_4_turbo = "gpt-4-turbo"
    gpt_4o = "gpt-4o"
    gpt_4o_mini = "gpt-4o-mini"
    azure_gpt_3_5_turbo = "azure-gpt-3.5-turbo"
    azure_gpt_4_turbo = "azure-gpt-4-turbo"
    azure_gpt_4o = "azure-gpt-4o"
    azure_gpt_4o_mini = "azure-gpt-4o-mini"
    claude_3_opus = "anthropic.claude-3-opus-20240229-v1:0"
    claude_sonnet = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    claude_3_haiku = "anthropic.claude-3-haiku-20240307-v1:0"
    # Add more models as needed


model_client_mapping = {
    ModelNameEnum.gpt_3_5_turbo: ClientsEnum.openai,
    ModelNameEnum.gpt_4_turbo: ClientsEnum.openai,
    ModelNameEnum.gpt_4o: ClientsEnum.openai,
    ModelNameEnum.gpt_4o_mini: ClientsEnum.openai,
    ModelNameEnum.azure_gpt_3_5_turbo: ClientsEnum.azure_openai,
    ModelNameEnum.azure_gpt_4_turbo: ClientsEnum.azure_openai,
    ModelNameEnum.azure_gpt_4o: ClientsEnum.azure_openai,
    ModelNameEnum.azure_gpt_4o_mini: ClientsEnum.azure_openai,
    ModelNameEnum.claude_3_opus: ClientsEnum.bedrock_claude,
    ModelNameEnum.claude_sonnet: ClientsEnum.bedrock_claude,
    ModelNameEnum.claude_3_haiku: ClientsEnum.bedrock_claude,
}


class ClientCallDataModel(BaseModel):
    name_model: str = Field(
        description="The name of the model to use for the API call",
    )
    system_prompt: str = Field(
        description="The system prompt to use for the API call",
    )
    user_prompt: str = Field(
        description="The user prompt to use for the API call",
    )
    json_response: bool = Field(
        description="Whether to return a JSON response",
        default=False,
    )
    temperature: float = Field(
        description="The temperature to use for the API call",
        default=0,
    )
    max_tokens: int = Field(
        description="The maximum number of tokens to generate",
        default=2000,
    )
    preference: list[ModelNameEnum] = Field(
        description="The preference order of models to use for the API call",
        default=[
            ModelNameEnum.gpt_3_5_turbo,
            ModelNameEnum.claude_sonnet,
            ModelNameEnum.gpt_4_turbo,
            ModelNameEnum.azure_gpt_4_turbo,
        ],
    )
