import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from app.main import app
from app.db.index_model import Base  # Assurez-vous que ce chemin est correct
from app.db.database import get_db  # Assurez-vous que ce chemin est correct

# Configuration de la base de données SQLite en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Dépendance pour remplacer `get_db` avec une session in-memory
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

# Application de l'override pour l'application FastAPI
app.dependency_overrides[get_db] = override_get_db

# Fixture pour la base de données qui est automatiquement appliquée à chaque test
@pytest.fixture(scope="function", autouse=True)
async def setup_and_teardown():
    # Configuration d'Alembic
    alembic_cfg = Config("alembic.ini")  # Assurez-vous que le chemin vers le fichier alembic.ini est correct
    alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

    async with engine.begin() as conn:
        # Appliquer les migrations
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(lambda conn: command.upgrade(alembic_cfg, "head"))
    
    yield  # Les tests s'exécutent ici

    async with engine.begin() as conn:
        # Suppression des tables après les tests
        await conn.run_sync(Base.metadata.drop_all)

# Fixture pour le client HTTP asynchrone
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
