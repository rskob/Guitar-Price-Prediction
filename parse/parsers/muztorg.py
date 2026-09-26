from ..main_parser import Parser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions


class MuztorgParser(Parser):
    url = "https://www.muztorg.ru"
    name = "muztorg"
    path = {"guitar": "/category/elektrogitary", "bass": "/category/bas-gitary", "amplifier": "/category/usiliteli-dlya-gitar"}

    def _parse(self, category: str):
        cat_url = self.url + self.path[category]
        self._driver.get(cat_url)
        hrefs = []
        pagination = self._driver.find_element(By.CLASS_NAME, "pagination-container__list")
        pagination_next = WebDriverWait(pagination, 10).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))[-1]
        pages = int(pagination_next.find_element(By.XPATH, "preceding-sibling::*[1]").text)

        for i in range(1, pages + 1):
            if i > 1: self._driver.get(f"{cat_url}?page={i}")
            articles = self._driver.find_element(By.CLASS_NAME, "catalog-listing").find_elements(By.TAG_NAME, "article")
            for art in articles:
                try:
                    hrefs.append(art.find_element(By.TAG_NAME,  "link").get_attribute("href"))
                except exceptions.NoSuchElementException:        
                    pass
        
        for href in hrefs:
            try:
                url = href + "?view_tab=characteristics"
                self._driver.get(url)
                characteristics = WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "mt-product-characteristics__item")))
                data = {}
                data["Название"] = self._driver.find_element(By.CLASS_NAME, "title-2").text
                try:
                    data["Цена"] = self._driver.find_element(By.CLASS_NAME, "product-header-price__discounted-value").text
                except exceptions.NoSuchElementException:     
                    data["Цена"] = self._driver.find_element(By.CLASS_NAME, "mt-product-price__default-value").text

                for ch in characteristics:
                    title = ch.find_element(By.CLASS_NAME, "mt-product-characteristics__title").text
                    value = ch.find_element(By.CLASS_NAME, "mt-product-characteristics__value").text
                    data[title] = value

                yield url, data
            except Exception as e:
                print(e)
