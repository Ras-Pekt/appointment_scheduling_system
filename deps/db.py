from core.database import SessionLocal


def get_db():
    """
    Get a database session.

    Returns:
        Session: A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
