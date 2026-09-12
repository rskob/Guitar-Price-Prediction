from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from abc import ABC, abstractmethod

class Parser(ABC):
    start_url = None

    def __init__(self, driver, parsers: dict):
        self._driver = driver
        self._parsers = parsers

    def run(self, categories: list[str]):
        self._driver.get(self.start_url)
        self._prepare()

        for cat in categories:
            if cat not in self._parsers:
                continue

            with self._parsers[cat] as parser:
                for data in parser.parse():
                    try:
                        # self._save(cat, data)
                        pass
                    except Exception as e:
                        print(e)

    @abstractmethod
    def _prepare(self):
        pass



class SubParser(ABC):
    def __init__(self, driver):
        self._driver = driver

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc, tb):
        pass

