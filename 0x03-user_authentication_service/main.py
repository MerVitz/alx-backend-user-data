#!/usr/bin/env python3
"""
Main file for testing find_user_by
"""
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

my_db = DB()

# Add a user
user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)

# Find user by email
find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)

# Handle case where no user is found
try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")

# Handle invalid query
try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")
