from fastapi import Depends

from app.domain.services.attachment_service import AttachmentService
from app.domain.services.type_attachment_service import TypeAttachmentService

from app.db.repositories.repository import AttachmentRepository, TypeAttachmentRepository

from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

# Dans certains cas, vous pourriez vouloir faire appel à une fonction
# ou une factory pour créer le service, et donc vous pourriez avoir :

def get_attachment_service(session: AsyncSession = Depends(get_db)):
    attachment_repository = AttachmentRepository(session)
    return AttachmentService(attachment_repository)

def get_type_attachment_service(session: AsyncSession = Depends(get_db)):
    type_attachment_repository = TypeAttachmentRepository(session)
    return TypeAttachmentService(type_attachment_repository)