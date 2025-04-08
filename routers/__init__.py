from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from deps.db import get_db

DB_Dependency = Annotated[Session, Depends(get_db)]
