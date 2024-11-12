from typing import List
from sqlalchemy import ARRAY, Column, Integer, String, ForeignKey, DateTime, Boolean, Time, Date
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class ScheduleModel(Base):
    __tablename__= f"{service}_schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    notification_id = Column(Integer, ForeignKey(f"{service}_notifications.id"), nullable=True)
    frequency = Column(Integer, nullable=True)  # Ex: toutes les 2 semaines
    days_of_week = Column(ARRAY(Integer), nullable=True)  # Ex : [1, 3, 5] pour lundi, mercredi, vendredi
    time_of_day = Column(Time, nullable=True)  # Heure d'envoi (Ex : 08:00)
    start_date = Column(DateTime, nullable=True)  # Date de début de la récurrence
    end_date = Column(DateTime, nullable=True)  # Date de fin de la récurrence
    repeat = Column(Boolean, default=False)  # Si la notification est répétée
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)