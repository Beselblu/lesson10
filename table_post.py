from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, desc, ForeignKey, DateTime, select
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)

class User(Base):
    __tablename__ = "user" 
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    exp_group  = Column(Integer)
    gender = Column(Integer)
    id = Column(Integer, primary_key=True)
    os = Column(String)
    source = Column(String)


class Feed_Action(Base):
    __tablename__ = "feed_action"

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    user = relationship(User)
    post_id = Column(Integer, ForeignKey(Post.id))
    post = relationship(Post)
    action = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)


if __name__ == "__main__":
    session = SessionLocal()

    for action in (session.query(User.exp_group)
        .filter(User.exp_group == 3)
        .limit(10)
        .all()):

        print(action)

