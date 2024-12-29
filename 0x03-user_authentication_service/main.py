#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

my_db = DB()

# Adding a user to the database
user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)

# Finding the user by email
find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)  # Should print the user's ID

# Attempting to find a non-existent user
try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")  # Expected output: "Not found"

# Attempting to use an invalid query argument (no_email is not a valid field)
try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")  # Expected output: "Invalid"
