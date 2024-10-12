from typing import Annotated
from fastapi import APIRouter, Body
from logzero import logger

from heimdall.service.router.router import LLMRouter
from heimdall.typing import ClientCallDataModel


llm_router: LLMRouter


def startup():
    global llm_router
    logger.info("Loading decoder model")
    llm_router = LLMRouter()
    logger.info("Loaded decoder model")


router = APIRouter(
    on_startup=[startup],
    prefix="/base",
    tags=["base"],
    responses={404: {"description": "Not found"}},
)


@router.post("/model_call")
async def model_call(
    request: Annotated[
        ClientCallDataModel,
        Body(
            examples=[
                {
                    "name_model": "gpt-3.5-turbo",
                    "system_prompt": "The system prompt to use for the API call",
                    "user_prompt": "The user prompt to use for the API call",
                    "json_response": False,
                    "temperature": 0,
                    "max_tokens": 2000,
                    "preference": [
                        "gpt-3.5-turbo",
                        "anthropic.claude-3-5-sonnet-20240620-v1:0",
                        "gpt-4-turbo",
                        "azure-gpt-4-turbo",
                    ],
                }
            ]
        ),
    ]
) -> str:
    return await llm_router.model_call(request)
