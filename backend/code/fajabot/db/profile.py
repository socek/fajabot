from sqlalchemy import JSON
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from fajabot.db.table import IdMixin
from fajabot.db.table import SqlTable


class ProfileTable(SqlTable, IdMixin):
    __tablename__ = "profiles"

    user = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    hp = Column(Integer, nullable=True)
    defence = Column(Integer, nullable=True)
    attack = Column(Integer, nullable=True)
    experience = Column(Integer, nullable=True)
    active = Column(Boolean, nullable=True)


class CooldownTable(SqlTable, IdMixin):
    __tablename__ = "cooldowns"

    user = Column(String, nullable=False)
    channel = Column(String, nullable=False)

    command = Column(String, nullable=True)
    cooldown = Column(DateTime, nullable=True)


class ObsalertsTable(SqlTable, IdMixin):
    __tablename__ = "obsalerts"

    payload = Column(JSON, nullable=True)
