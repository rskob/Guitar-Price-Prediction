
from selenium.webdriver.common.by import By
from time import sleep
from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from .sub_parser import SubParser


class Parser(ABC):
    start_url: str
    name: str
    categories_and_queries: dict[str, str]
    sub_parser: SubParser

    def __init__(self, driver, db_worker):
        self._driver = driver
        self._db_worker = db_worker
        for attr in ("start_url", "name", "categories_and_queries", "sub_parser"):
            if not hasattr(self, attr):
                raise NotImplementedError(f"Attribute {attr} must be implemented.")

        self._parsers = {i: self.sub_parser(j, driver) for i, j in self.categories_and_queries.items()}


    def run(self, categories: list[str]):
        self._driver.get(self.start_url)
        self._prepare()

        stats = dict.fromkeys(self._parsers, 0)
        for cat in categories:
            if cat not in self._parsers:
                continue

            with self._parsers[cat] as parser:
                for url, data in parser.parse():
                    try:
                        print(data)
                        stats[cat] += self._db_worker.save(self.name, cat, url, data)
                        pass
                    except Exception as e:
                        print(e)

        return stats

    @abstractmethod
    def _prepare(self):
        pass



