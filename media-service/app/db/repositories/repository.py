from sqlalchemy.ext.asyncio import AsyncSession
from app.db.index_model import AttachmentModel, TypeAttachmentModel
from app.db.repositories.base import BaseRepository

class TypeAttachmentRepository(BaseRepository[TypeAttachmentModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(TypeAttachmentModel, db)

class AttachmentRepository(BaseRepository[AttachmentModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(AttachmentModel, db)