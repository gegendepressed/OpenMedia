"""
    models.py, this module contains class declaration for all the
    database entities that are used in the app
"""

from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.orm import DeclarativeBase, column_property, Mapped, mapped_column, relationship
from flask_login import UserMixin


class Base(DeclarativeBase): # pylint: disable=too-few-public-methods
    """
    The Base class that holds the metadata/schema for the database
    """
    pass


class User(Base, UserMixin): # pylint: disable=too-few-public-methods
    """
    The User class whose object represents a user of app, user_account table
    """
    __tablename__ = "user_account"

    username: Mapped[str] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    profile_pic_url: Mapped[Optional[str]] = mapped_column(default="user.png")
    posts: Mapped[List["Posts"]] = relationship(back_populates="owner")

    def __str__(self) -> str:
        return (
            f"\nUsername: {self.username}"
            f"\nEmail: {self.email}"
            f"\nPassword: {self.password}"
            f"\nName: {self.fullname}"
            f"\nProfile pic: {self.username}"
        )

    def get_id(self):
        return self.username


class Likes(Base): # pylint: disable=too-few-public-methods
    """
    The Likes class whose object represents a Like for a post
    """
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    liked_post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Posts"] = relationship(back_populates="likes")
    liked_by_id: Mapped[str] = mapped_column(ForeignKey("user_account.username"))
    user: Mapped["User"] = relationship()

    def __str__(self):
        return (
            f"\nPost ID: {self.liked_post_id}"
            f"\nLiked By: {self.liked_by_id}"
        )


class Posts(Base): # pylint: disable=too-few-public-methods
    """
    The Post class whose object represents a post made by the user
    Can contain Title, text and optionally image
    """
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[Optional[str]] = mapped_column()
    likes: Mapped[List["Likes"]] = relationship(back_populates="post")
    timestamp: Mapped[int] = mapped_column(nullable=False)
    owner_id: Mapped[str] = mapped_column(ForeignKey("user_account.username"))
    owner: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comments"]] = relationship(back_populates="post")
    no_of_likes = column_property(
        select(func.count(Likes.id))
        .where(Likes.liked_post_id == id)
        .scalar_subquery()
    )

    def __str__(self) -> str:
        return (
            f"\nPost ID: {self.id}"
            f"\nText: {self.text}"
            f"\nImage: {self.image}"
            f"\nLikes: {self.no_of_likes}"
            f"\nTimestamp: {self.timestamp}"
        )


class Comments(Base): # pylint: disable=too-few-public-methods
    """
    The Comments class whose object represents a comment on a Post object
    """
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    creator_id: Mapped[str] = mapped_column(ForeignKey("user_account.username"))
    created_by: Mapped["User"] = relationship()
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Posts"] = relationship()

    def __str__(self) -> str:
        return (
            f"\nComment ID: {self.id}"
            f"\ntext: {self.text}"
            f"\nPost ID: {self.post_id}"
        )


# The db object which is used to access database
db = SQLAlchemy(model_class=Base)
