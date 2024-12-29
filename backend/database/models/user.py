from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Model


def get_utc_now():
    return datetime.utcnow()


class User(Model):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    full_name = Column(String(200), nullable=True)
    password = Column(String(400), nullable=False)
    channel = relationship("Channel", uselist=False)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)
    updated_at = Column(DateTime, onupdate=get_utc_now, nullable=True)
    user_log_info = relationship(
        "UserLogInfo", back_populates="user", uselist=False, passive_deletes=True
    )

    def __repr__(self):
        return f"{self.username} - {self.full_name}"


class UserLogInfo(Model):
    __tablename__ = "user_log_info"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    user = relationship("User", back_populates="user_log_info")
    session_id = Column(String(100), unique=True, nullable=False)
    last_login = Column(DateTime, default=get_utc_now, nullable=False)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)

    def __repr__(self):
        return f"{self.session_id} - {self.last_login}"


# Association Table
playlist_video_association = Table(
    "playlist_video",
    Model.metadata,
    Column(
        "playlist_id",
        Integer,
        ForeignKey("playlists.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "video_id",
        Integer,
        ForeignKey("videos.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Playlist(Model):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    visibility = Column(String(10), default="private")
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    video = relationship(
        "Video", secondary=playlist_video_association, back_populates="playlists"
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.id


class Video(Model):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(80), nullable=False)
    video_type = Column(String(20), default="long_video", nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    description = Column(String, nullable=True)
    file_name = Column(String(40), nullable=False)
    file_url = Column(String(150), nullable=False)
    thumbnail_name = Column(String(40), nullable=True)
    thumbnail_url = Column(String(150), nullable=True)
    audience = Column(Boolean, default=False)  # False means it's not made for kids
    age_restriction = Column(
        Boolean, default=False
    )  # False means don't restrict the video
    language = Column(String(50), default="not-applicable", nullable=True)
    playlists = relationship(
        "Playlist", secondary=playlist_video_association, back_populates="video"
    )
    subtitle = relationship(
        "Subtitle", back_populates="video", uselist=False, passive_deletes=True
    )
    monetization = Column(Boolean, default=False)
    visibility = Column(Boolean, default=False)  # False means private
    schedule_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.title


class Subtitle(Model):
    __tablename__ = "subtitles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    file_name = Column(String(40), nullable=False)
    file_url = Column(String(150), nullable=False)
    video_id = Column(
        Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False
    )
    video = relationship("Video", back_populates="subtitle")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.title


class Community(Model):
    __tablename__ = "communities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    community_text = Column(String(200), nullable=False)
    image_name = Column(String(200), nullable=True)
    image_url = Column(String(400), nullable=True)

    def __repr__(self):
        return self.community_text


class Channel(Model):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    banner_img_url = Column(String(200), nullable=True)
    profile_picture_url = Column(String(200), nullable=True)
    video_watermark_url = Column(String(200), nullable=True)
    name = Column(String(200), nullable=True)
    unique_identifier = Column(String(100), nullable=True)
    description = Column(String(500), nullable=True)
    contact_email = Column(String(100), nullable=True)

    def __repr__(self):
        return f"{self.owner_id} Channel"
