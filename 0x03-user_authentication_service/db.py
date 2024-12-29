#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """DB class to interact with the database."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the user.

        Returns:
            User: The first user matching the filter.

        Raises:
            NoResultFound: If no user matches the filter criteria.
            InvalidRequestError: If invalid filter criteria are provided.
        """
        # Check if all the keys in kwargs are valid User columns
        # Get all valid column names of the User model
        valid_columns = {column.name for column in User.__table__.columns}
        # Find invalid columns
        invalid_columns = [key for key in kwargs if key not in valid_columns]

        if invalid_columns:
            raise InvalidRequestError(
                f"Invalid columns: {', '.join(invalid_columns)}")

        # Query the user with the provided filters
        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound("No user found matching the criteria.")

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates attr based on the provided user_id and keyword arguments.

        Args:
            user_id (int): The ID of the user to be updated.
            **kwargs: Arbitrary keyword arguments to update user attributes.

        Raises:
            ValueError: If an invalid attribute is provided in kwargs.
        """
        # Find the user using the provided user_id
        user = self.find_user_by(id=user_id)

        # List of valid user attributes
        valid_attributes = {column.name for column in User.__table__.columns}

        # Check for invalid attributes in kwargs
        for key in kwargs:
            if key not in valid_attributes:
                raise ValueError(f"Invalid attribute: {key}")

        # Update user attributes with the provided kwargs
        for key, value in kwargs.items():
            setattr(user, key, value)

        # Commit the changes to the database
        self._session.commit()
