from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome


class Parser(ABC):
    url: str
    name: str
    path: dict[str, str]

    def __init__(self, driver, db_worker):
        self._driver = driver
        self._db_worker = db_worker
        for attr in ("url", "name", "path"):
            if not hasattr(self, attr):
                raise NotImplementedError(f"Attribute {attr} must be implemented.")
        
        self._wait = WebDriverWait(self._driver, 10)

    def run(self, categories: list[str]):
        self._driver: Chrome
        self._driver.maximize_window()

        stats = {i: 0 for i in set(categories) & set(self.path.keys())}
        for cat in categories:
            if cat not in self.path:
                return

            try:
                for url, data in self._parse(cat):
                    print(data)
                    try:
                        stats[cat] += self._db_worker.save(self.name, cat, url, data)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)


        return stats

    @abstractmethod
    def _parse(self, category: str):
        pass
