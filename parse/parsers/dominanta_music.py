from ..main_parser import Parser
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class DominantaMusicParser(Parser):
    url = "https://dominantamusic.ru"
    name = "ДОМИНАНТА МЬЮЗИК"
    path = {"guitar": "/catalog/elektrogitary/"}

    def _parse(self, category):
        cat_url = self.url + self.path[category]
        self._driver.get(cat_url)
        pages = int(self._driver.find_elements(By.CLASS_NAME, "number_page")[-1].text)
        hrefs = []
        print(pages)
        for i in range(1, pages + 1):
            if i > 1:
                self._driver.get(d := f"{cat_url}?PAGEN_1={i}")
                print(d)

            articles = self._driver.find_elements(By.XPATH, "//div[@id='section_tile']/div")
            for art in articles:
                try:
                    art.find_element(By.CLASS_NAME, "commodity_few")
                except exceptions.NoSuchElementException:
                    hrefs.append(art.find_element(By.CLASS_NAME, "commodity_link").get_attribute("href"))

        for href in hrefs:
            try:
                self._driver.get(href)

                data = {}
                data["Название"] = self._driver.find_element(By.CLASS_NAME, "element__title").text
                data["Цена"] = self._driver.find_element(By.CLASS_NAME, "element__price_summ").find_elements(By.TAG_NAME, "span")[-1].text

                characteristics = self._driver.find_elements(By.CLASS_NAME, "characteristics__row")
                for ch in characteristics:
                    td1, td2 = ch.find_elements(By.TAG_NAME, "td")
                    data[td1.text] = td2.text

                yield href, data
            except Exception as e:
                print(e)


