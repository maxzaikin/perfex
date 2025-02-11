from src.db.db_adapter import Model

from sqlalchemy import (
    Table,
    String,
    Text,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import(
    Mapped,
    mapped_column,
    relationship
)
from datetime import datetime

class Post(Model):
    __tablename__='posts'
    
    id: Mapped[int]= mapped_column(primary_key=True)
    publication_date: Mapped[datetime]= mapped_column(default=datetime.utcnow, index=True)
    title: Mapped[str]= mapped_column(String(255))
    content: Mapped[str]= mapped_column(Text)
    
    comments: Mapped[list['Comment']]= relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    
class Comment(Model):
    __tablename__='comments'
    
    id: Mapped[int]= mapped_column(primary_key=True)
    post_id: Mapped[int]=mapped_column(ForeignKey('posts.id', ondelete='CASCADE'), index=True)
    publication_date:Mapped[datetime]= mapped_column(default=datetime.utcnow, index=True)
    content: Mapped[str]= mapped_column(Text)
    
    post: Mapped['Post']= relationship('Post',back_populates='comment')
    
class User(Model):
    __tablename__='users'
    
    id: Mapped[int]= mapped_column(primary_key=True)
    email: Mapped[str]= mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str]= mapped_column(String(255), nullable=False)
    
    token: Mapped['Token']= relationship('Token',back_populates='user',uselist=False, cascade='all, delete-orphan')
    
class Token(Model):
    __tablename__='tokens'
    
    id: Mapped[int]= mapped_column(primary_key=True)
    user_id:Mapped[int]= mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True, unique=True)
    access_token: Mapped[str]= mapped_column(String(255), nullable=False)
    expiration_date: Mapped[datetime]= mapped_column(DateTime, nullable=False)
    
    user: Mapped['User']= relationship('User',back_populates='token')