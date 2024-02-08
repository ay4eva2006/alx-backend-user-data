#!/usr/bin/env python3
"""5. Encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    return bcrypt.hashpw(password.encode('UTF-8'),
                         bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Uses bcrypt to validate that the provided password
    matches the hashed password."""
    return bcrypt.checkpw(password.encode('UTF-8'),
                          hashed_password)
