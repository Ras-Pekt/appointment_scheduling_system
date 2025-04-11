from uuid import uuid4


def generate_uuid():
    """
    Generate a new UUID.

    Returns:
        str: A new UUID.
    """
    return str(uuid4())
