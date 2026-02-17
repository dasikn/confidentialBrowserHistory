from abc import ABC, abstractmethod
from model import Website


class VSPort(ABC):

    @abstractmethod
    def insert_website_to_vs(self, website: Website) -> None:
        pass

    @abstractmethod
    def semantic_search(self, query: str) -> list:
        pass

    @abstractmethod
    def delete_by_date(self, date: str) -> int:
        pass

    @abstractmethod
    def delete_all(self) -> int:
        pass
