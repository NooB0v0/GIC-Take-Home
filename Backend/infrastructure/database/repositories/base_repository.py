from sqlalchemy.orm import Session
from abc import ABC

class BaseRepository(ABC):
    def __init__(self, session: Session):
        self.session = session