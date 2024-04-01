from typing import List, Optional
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.orm import DeclarativeBase, column_property, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
  pass



class User(Base):
    # The User class whose object represents a user of app, user_account table
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


# This table establishes many to many relation between posts table and likes table
"""
likes_association_table = Table(
    "likes_association_table",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id")),
    Column("like_id", ForeignKey("likes.id")),
)
"""


class Likes(Base):
    # Table that stores Likes information.
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


class Posts(Base):
    # The Post class whose object represents Posts made by users
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column()
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


class Comments(Base):
    # The comments class whose objects are post comments
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
