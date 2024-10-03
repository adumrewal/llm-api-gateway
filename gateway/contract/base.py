from logzero import logger
from fastapi import APIRouter

from gateway.service.router.router import LLMRouter


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