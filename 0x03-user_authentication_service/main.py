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
email = 'test@test.com'
hashed_password = "hashedPwd"

user = my_db.add_user(email, hashed_password)
print(f"User ID: {user.id}")  # Expect user ID to be printed

# Updating the user's password
try:
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
except ValueError as e:
    print(f"Error: {e}")

# Trying to update with an invalid attribute
try:
    my_db.update_user(user.id, non_existent_field="value")
except ValueError as e:
    print(f"Error: {e}")  # Should print an error about invalid attribute

# Verify the update was successful
updated_user = my_db.find_user_by(id=user.id)
print(f"Updated password: {updated_user.hashed_password}")
