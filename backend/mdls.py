from sqlalchemy import *
from .database import Base
from sqlalchemy.orm import relationship




class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False) 

    feedbacks = relationship("Feedback", back_populates="user")

 
class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String(255), unique=True, nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(String(255), nullable=False)


    user = relationship("User", back_populates="feedbacks")