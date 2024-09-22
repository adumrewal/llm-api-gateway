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


class ClientApiCall(BaseModel):
    model_name: str = Field(
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