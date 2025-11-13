from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

class ICafeRepository(ABC):
    @abstractmethod
    def get_all_cafes(self, location: Optional[str] = None) -> List[dict]:
        pass

    @abstractmethod
    def get_cafe_by_id(self, cafe_id: UUID) -> dict:
        pass

    @abstractmethod
    def add_cafe(self, cafe_data: dict) -> dict:
        pass

    @abstractmethod
    def update_cafe(self, cafe_id: UUID, cafe_data: dict) -> dict:
        pass

    @abstractmethod
    def delete_cafe(self, cafe_id: UUID) -> None:
        pass

