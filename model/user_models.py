from model.model_settings import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=True, unique=True)
    tg_channel_id = Column(String, nullable=True, unique=True)

    def __str__(self):
        return f"{self.id} {self.user_name}"
