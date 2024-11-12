from typing import AsyncGenerator
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DatabaseError
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from contextlib import asynccontextmanager

# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
# Création de l'engine asynchrone
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)

# Création du sessionmaker pour les sessions asynchrones
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

async def get_db()-> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error")
    except DatabaseError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    # except SQLAlchemyError:
    #     await db.rollback()
    #     raise
    finally:
        await db.close()