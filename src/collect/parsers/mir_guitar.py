from ..main_parser import Parser
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class MirGuitarParser(Parser):
    url = "https://mirguitar.ru"
    name = "МИР ГИТАР"
    path = {"guitar": "/products/category/electric-guitars"}

    def _parse(self, category):
        cat_url = self.url + self.path[category]
        self._driver.get(cat_url)
        pages = int(self._driver.find_elements(By.CLASS_NAME, "pagination__item")[-1].text)
        hrefs = []
        for i in range(1, pages + 1):
            if i > 1:
                self._driver.get(f"{cat_url}?page={i}")

            articles = self._driver.find_elements(By.CLASS_NAME, "product-item-grid__preview")
            for art in articles:
                hrefs.append(art.find_element(By.TAG_NAME, "a").get_attribute("href"))

        for href in hrefs:
            try:
                self._driver.get(href)
                data = {}
                data["Название"] = self._driver.find_element(By.CLASS_NAME, "new-product__title").text
                data["Цена"] = self._driver.find_element(By.CLASS_NAME, "product-price-data").text

                characteristics_1 = self._driver.find_elements(By.XPATH, "//div[@class='new-product__desc new-product__desc--mobile user-inner']/p/span")[1:]
                for ch in characteristics_1:
                    key = ch.text

                    value = ch.find_element(By.XPATH, "//span[contains(@style, 'font-weight: bold')]").text.strip()
                    if not value:
                        key, value = key.split(":")
                    data[key] = value

                characteristics_2 = self._driver.find_elements(By.XPATH, "//div[@class='new-product-specifications__wrapper']/div")
                for ch in characteristics_2:
                    key = ch.find_element(By.XPATH, "div[@class='new-product-specifications__name']").text
                    value = ch.find_element(By.CLASS_NAME, "new-product-specifications__value").text
                    data[key] = value

                yield href, data

            except Exception as e:
                print(e)


