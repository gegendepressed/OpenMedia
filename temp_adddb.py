from app import app
from models import *
from sqlalchemy import select
from form import User


with app.app_context():
    db.create_all()

    """
    u1 = User(
    username="frost",
    fullname="Yash Patil",
    email="test@example.com",
    password='1234',
    )

    u2 = User(
        username="gegendepressed",
        fullname="Sairaj Pai",
        email="test2@example.com",
        password='1234',
    )

    db.session.add(u1)
    db.session.add(u2)
    
    db.session.add(Posts(
        id="1",
        title="1stp",
        image="none",
        timestamp="12345",
        text="First Post!",
        owner_id="gegendepressed",
    ))

    db.session.add(Posts(
        id="2",
        image="none",
        title="2ndp",
        timestamp="12345",
        text="Second Post!",
        owner_id="frost",
    ))

    result = db.session.get(Posts, "1")

    db.session.add(Likes(
        id="1001",
        liked_post_id="1",
        liked_by_id="gegendepressed"
    ))
    db.session.add(Likes(
        id="1002",
        liked_post_id="1",
        liked_by_id="frost"
    ))

    likeddata = db.session.get(Likes, 1001)
    postdata = db.session.get(Posts, 1)
    postdata.likes.append(likeddata)

    db.session.add(Comments(
        id="1001",
        text="First Comment",
        creator_id="gegendepressed",
        post_id="1",
    ))
    db.session.add(Comments(
        id="1002",
        text="Second Comment",
        creator_id="frost",
        post_id="1"
    ))

    comment1 = db.session.get(Comments, "1001")
    comment2 = db.session.get(Comments, "1002")
    postdata.comments.append(comment1)
    postdata.comments.append(comment2)

    db.session.commit()

    """
"""post1 = db.session.get(Posts, "1")
    for like in post1.likes:
        print(like)
    for comment in post1.comments:
        print(comment)"""

stmt = select(User).where(User.c.name == "spongebob")
print(stmt)