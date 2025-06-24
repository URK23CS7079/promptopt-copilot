from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Updated connection string for async SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./promptopt.db")

# Async engine configuration
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=True  # Remove in production
)

# Async session factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

class Prompt(Base):
    __tablename__ = "prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000), nullable=False)  # Added length constraint
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)  # Timezone-aware
    parameters = Column(JSON, nullable=True)  # Explicit nullable
    parent_id = Column(Integer, ForeignKey("prompts.id"), nullable=True)  # Proper FK

    # Relationship for SQLAlchemy 2.0
    versions = relationship("Prompt", back_populates="parent")
    parent = relationship("Prompt", remote_side=[id], back_populates="versions")

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), index=True)
    metrics = Column(JSON, nullable=False)
    test_data_hash = Column(String(64), nullable=False)  # SHA-256 length
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationship
    prompt = relationship("Prompt", backref="evaluations")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    """Dependency for FastAPI"""
    async with SessionLocal() as session:
        yield session