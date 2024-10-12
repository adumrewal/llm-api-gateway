from fastapi import APIRouter

from pydantic import BaseModel

router = APIRouter(
    on_startup=[],
    prefix="/config",
    tags=["config"],
    responses={404: {"description": "Not found"}},
)


class Config(BaseModel):
    user_id: str
    model_preference: list[str]
    system_prompt: str
    temperature: float
    max_tokens: int


@router.post("/create")
async def create_config(config: Config):
    # TODO: Implement config creation logic
    return {"message": "Config created successfully"}


@router.get("/{user_id}")
async def get_config(user_id: str):
    # TODO: Implement config retrieval logic
    return {"user_id": user_id, "config": {}}


@router.put("/{user_id}")
async def update_config(user_id: str, config: Config):
    # TODO: Implement config update logic
    return {"message": "Config updated successfully"}


@router.delete("/{user_id}")
async def delete_config(user_id: str):
    # TODO: Implement config deletion logic
    return {"message": "Config deleted successfully"}
