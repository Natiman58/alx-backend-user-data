#!/usr/bin/env python3
"""
    SQLAlchemy ORM model 'User' for a database table named 'user'
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# A declarative base class to map a class to DB tables
Base = declarative_base()

class User(Base):
    """
        A User class that represents a db table 'user'
        with the following columns defined
    """
    # describe the db table name
    __tablename__ = 'users'

    # describe the columns
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
    