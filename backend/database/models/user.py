from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

Model = declarative_base()


def get_utc_now():
    return datetime.utcnow()


class User(Model):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    full_name = Column(String(200), nullable=True)
    password = Column(String(400), nullable=False)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)
    updated_at = Column(DateTime, onupdate=get_utc_now, nullable=False)
    user_log_info = relationship("UserLogInfo", back_populates='user', uselist=False, passive_deletes=True)

    def __repr__(self):
        return f"{self.username} - {self.full_name}"


class UserLogInfo(Model):
    __tablename__ = 'user_log_info'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    user_log_info = relationship("User", back_populates='user_log_info')
    session_id = Column(String(100), unique=True, nullable=False)
    last_login = Column(DateTime, default=get_utc_now, nullable=False)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)

    def __repr__(self):
        return f"{self.session_id} - {self.last_login}"
