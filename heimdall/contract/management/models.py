from enum import Enum
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from heimdall.core.database_core import get_db, LLMModel as DBLLMModel

router = APIRouter(
    on_startup=[],
    prefix="/api/management/models",
    tags=["models", "api"],
    responses={404: {"description": "Not found"}},
)


class LLMModel(BaseModel):
    name: str
    provider: str
    description: str
    cost_per_million_tokens: Optional[float] = Field(default=None)


class LLMModelProviderEnum(str, Enum):
    openai = "openai"
    azure_openai = "azure_openai"
    bedrock_claude = "bedrock_claude"


@router.get("/providers")
async def get_providers():
    return {"providers": [provider.value for provider in LLMModelProviderEnum]}


@router.get("")
async def get_models(db: Session = Depends(get_db)):
    models = db.query(DBLLMModel).all()
    return {"models": models}


@router.post("/create")
async def create_model(model: LLMModel, db: Session = Depends(get_db)):
    try:
        db_model = DBLLMModel(
            name=model.name,
            provider=model.provider,
            description=model.description,
            cost_per_million_tokens=model.cost_per_million_tokens,
        )
        db.add(db_model)
        db.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Model created successfully"}


@router.get("/{model_name}")
async def get_model(model_name: str, db: Session = Depends(get_db)):
    db_model = (
        db.query(DBLLMModel).filter(DBLLMModel.name == model_name).first()
    )
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return {"model": db_model}


@router.put("/{model_name}")
async def update_model(
    model_name: str, model: LLMModel, db: Session = Depends(get_db)
):
    db_model = (
        db.query(DBLLMModel).filter(DBLLMModel.name == model_name).first()
    )
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    db_model.name = model.name
    db_model.provider = model.provider
    db_model.description = model.description
    db_model.cost_per_million_tokens = model.cost_per_million_tokens
    db.commit()
    return {"message": "Model updated successfully"}


@router.delete("/{model_name}")
async def delete_model(model_name: str, db: Session = Depends(get_db)):
    db_model = (
        db.query(DBLLMModel).filter(DBLLMModel.name == model_name).first()
    )
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    db.delete(db_model)
    db.commit()
    return {"message": "Model deleted successfully"}
