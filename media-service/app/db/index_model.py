from app.db.database import Base
from sqlalchemy.orm import relationship

from app.db.models.type_attachment_model import TypeAttachmentModel
from app.db.models.attachment_model import AttachmentModel

AttachmentModel.type_attachment = relationship('TypeAttachmentModel')