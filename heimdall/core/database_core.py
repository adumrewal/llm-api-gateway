from sqlalchemy import create_engine, Column, String, Float, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/heimdall.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Config(Base):
    __tablename__ = "configs"

    user_id = Column(String, primary_key=True, index=True)
    model_preference = Column(JSON)
    system_prompt = Column(String)
    temperature = Column(Float)
    max_tokens = Column(Integer)


class LLMModel(Base):
    __tablename__ = "llm_models"

    name = Column(String, primary_key=True, index=True)
    provider = Column(String)
    description = Column(String)
    cost_per_million_tokens = Column(Float)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
