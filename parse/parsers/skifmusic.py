from ..main_parser import Parser
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC


class SkifMusicParser(Parser):
    url = "https://skifmusic.ru"
    name = "SKIFMUSIC"
    path = {"guitar": "/catalog/elektrogitaryi-12?f-condition-new=1"}

    def _parse(self, category):
        cat_url = self.url + self.path[category]
        self._driver.get(cat_url)

        hrefs = []
        while True:
            articles = self._driver.find_elements(By.CLASS_NAME, "product-card__image")

            for art in articles:
                hrefs.append(art.get_attribute("href"))

            try:
                pagination_next = self._driver.find_element(By.CLASS_NAME, "pagination__button-text")
            except exceptions.NoSuchElementException:
                break

            self._driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", pagination_next)
            self._wait.until(EC.staleness_of(articles[0]))

        for href in hrefs:
            try:
                self._driver.get(href)
                data = {}
                data["Название"] = self._driver.find_element(By.CLASS_NAME, "product-card-info__title").text
                try:
                    data["Цена"] = self._driver.find_element(By.CLASS_NAME, "product-card-info__price").text
                except exceptions.NoSuchElementException:
                    continue
                ch_button = self._driver.find_element(By.XPATH, "//div[@class='card-info-list']/a")
                self._driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", ch_button)
                characteriscs = self._wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@id='parameters']/div/div/ul/li")))
                for ch in characteriscs:
                    sp1, sp2 = ch.find_elements(By.TAG_NAME, "span")
                    data[sp1.text] = sp2.text

                yield href, data
            except Exception as e:
                print(e)

