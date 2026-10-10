from ..main_parser import Parser
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class GuitarLavkaParser(Parser):
    url = "https://guitarlavka.ru"
    name = "Guitar Lavka"
    path = {"guitar": "/gitaryi/elektrogitaryi"}

    def _parse(self, category):
        cat_url = self.url + self.path[category]
        self._driver.get(cat_url)

        last_page_href = self._driver.find_elements(By.XPATH, "//div[@class='pagination']/ul/li/a")[-1].get_attribute("href")
        pages = int(last_page_href[last_page_href.find("page=") + len("page="):])
        hrefs = []
        for i in range(13, pages + 1):
            if i > 1:
                self._driver.get(f"{cat_url}?page={i}")

            articles = self._driver.find_elements(By.XPATH, "//form[@method='post']/a")
            for art in articles:
                hrefs.append(art.get_attribute("href"))

        for href in hrefs:
            try:
                self._driver.get(href)
                data = {}
                data["Название"] = self._driver.find_element(By.CLASS_NAME, "product__title").text
                data["Цена"] = self._driver.find_element(By.XPATH, "//div[@class='product-group-price']/span[@class='product__title _price']/span").text

                chars_button = self._wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='product-tab']/li/a[@class='tablink product-tab__link']")))
                self._driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", chars_button)

                characteristics = self._driver.find_elements(By.XPATH, "//div[@class='tab-tab-product-characteristics']/div")
                for ch in characteristics:
                    value = ch.find_element(By.TAG_NAME, "p")
                    key = value.find_element(By.XPATH, "./preceding-sibling::*[1]")
                    data[key.text] = value.text

                yield href, data
            except Exception:
                pass


            
