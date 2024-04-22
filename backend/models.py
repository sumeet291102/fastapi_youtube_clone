from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    profile_pic = Column(String, nullable=True, index=True)
    profile_cover = Column(String, nullable=True, index=True)
    user_description = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.now())
    videos = relationship("Video", back_populates="uploaded_by")
    comments = relationship("Comment", back_populates="commented_by")
    likes = relationship("Like", back_populates="liked_by")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    url = Column(String, index=True)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now())
    uploaded_by = relationship("User", back_populates="videos")
    comments = relationship("Comment", back_populates="commented_on")
    likes = relationship("Like", back_populates="liked_on")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    commented_on_id = Column(Integer, ForeignKey("videos.id"))
    commented_by_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String, index=True)
    commented_on = relationship("Video", back_populates="comments")
    commented_by = relationship("User", back_populates="comments")
    created_at = Column(DateTime, default=datetime.now())


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    liked_on_id = Column(Integer, ForeignKey("videos.id"))
    liked_by_id = Column(Integer, ForeignKey("users.id"))
    liked_on = relationship("Video", back_populates="likes")
    liked_by = relationship("User", back_populates="likes")
    created_at = Column(DateTime, default=datetime.now())


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True)
    subscriber_id = Column(Integer, ForeignKey("users.id"))
    subscribee_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now())
