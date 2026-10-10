from ..main_parser import Parser
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class ShopAvallonParser(Parser):
    url = "https://shop-avallon.ru/"
    name = "Аваллон"
    path = {"guitar": "/catalog/guitars/electricguitars"}

    def _parse(self, category):
        cat_url = self.url + self.path[category]
        page_num = 1
        hrefs = []
        while True:
            self._driver.get(f"{cat_url}/{page_num}/?cur_cc=122")

            articles = self._driver.find_elements(By.CLASS_NAME, "main__hits-card")
            for art in articles: 
                hrefs.append(art.find_element(By.TAG_NAME, "a").get_attribute("href"))

            try:
                self._driver.find_element(By.XPATH, "//div[@class='pagination__block pagination-next']")
                break
            except exceptions.NoSuchElementException:
                pass

            page_num += 1
            print(page_num)

        print(len(hrefs))

        for href in hrefs:
            try:
                self._driver.get(href)
                data = {}
                data["Название"] = self._driver.find_element(By.XPATH, "//div[@class='template__title card__title']/h1").text
                data["Цена"] = self._driver.find_element(By.CLASS_NAME, "card__price").text
                self._driver.get(href)
                characteristics = self._driver.find_elements(By.XPATH, "//table[@class='specs']/tbody/tr")
                for ch in characteristics:
                    key = ch.find_element(By.TAG_NAME, "th").text
                    value = ch.find_element(By.TAG_NAME, "td").text
                    data[key] = value

                yield href, data

            except Exception:
                pass
