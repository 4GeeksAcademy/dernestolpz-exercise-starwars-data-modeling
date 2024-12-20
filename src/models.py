import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    subscription_date = Column(DateTime, default=datetime.utcnow)

    
    favorites = relationship("Favorite", back_populates="user")

    
    comments = relationship("Comment", back_populates="user")


class Planet(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    climate = Column(String(250), nullable=False)
    terrain = Column(String(250), nullable=False)

   
    favorites = relationship("Favorite", back_populates="planet")

    
    comments = relationship("Comment", back_populates="planet")


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    height = Column(Integer, nullable=False)
    eye_color = Column(String(100), nullable=False)
    hair_color = Column(String(100), nullable=False)

    
    favorites = relationship("Favorite", back_populates="character")

    
    comments = relationship("Comment", back_populates="character")


class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)

    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="favorites")

    
    planet_id = Column(Integer, ForeignKey('planets.id'))
    planet = relationship("Planet", back_populates="favorites")

    
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character", back_populates="favorites")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    comment_date = Column(DateTime, default=datetime.utcnow)

    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="comments")

    
    planet_id = Column(Integer, ForeignKey('planets.id'))
    planet = relationship("Planet", back_populates="comments")

    
    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character", back_populates="comments")


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    postal_code = Column(String(250), nullable=False)

    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, backref='addresses')


engine = create_engine('sqlite:///starwars_blog.db')
Base.metadata.create_all(engine)


try:
    render_er(Base, 'diagram.png')
    print("Success! The diagram has been generated as diagram.png.")
except Exception as e:
    print("There was a problem generating the diagram.")
    raise e
