from app.db.database import Base
from sqlalchemy.orm import relationship, backref

from app.db.models.user_model import UserModel
from app.db.models.user_info_model import UserInfoModel
from app.db.models.device_model import DeviceModel
from app.db.models.otp_model import OtpModel
from app.db.models.session_model import SessionModel


UserModel.user_info = relationship('UserInfoModel', backref=backref('user', uselist=False), cascade="all, delete-orphan")

SessionModel.user = relationship('UserModel')
SessionModel.device = relationship('DeviceModel')

DeviceModel.user = relationship("UserModel")

OtpModel.user = relationship('UserModel')