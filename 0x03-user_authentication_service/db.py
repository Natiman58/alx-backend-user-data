#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            Add a user to the the db
            and returns the user object
        """
        # create a new user object with the given email and pwd
        user = User(email=email, hashed_password=hashed_password)

        # add the user to the current session
        self._session.add(user)

        # commit the changes to the database
        self._session.commit()

        # return the User object the was added to the DB
        return user

    def find_user_by(self, **kwargs) -> User:
        """
            finds the user and returns the first row found in
            the 'users' table
        """
        try:
            # serarch the user from the session and return the first match
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user was found with the given filters")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid request")
