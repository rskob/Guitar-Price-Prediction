from abc import ABC, abstractmethod


class SubParser(ABC):
    def __init__(self, query: str, driver):
        self._query = query
        self._driver = driver

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, tb):
        self._driver.close()
        return True