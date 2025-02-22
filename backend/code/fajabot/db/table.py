from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class SqlTable(DeclarativeBase):
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def _asdict(self):
        data = dict(self.__dict__)
        del data["_sa_instance_state"]
        return data


class IdMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
