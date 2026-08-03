import hashlib
import os


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${digest}"


def verify_password(password, stored_hash):
    try:
        salt, digest = stored_hash.split("$", 1)
    except (ValueError, AttributeError):
        return False
    check = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return check == digest