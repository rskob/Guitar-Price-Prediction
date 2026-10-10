from ..main_parser import Parser
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class LegatoParser(Parser):
    url = "https://www.legato.su"
    name = "Legato"
    path = {"guitar": "/catalog/gitary/elektrogitary/"}

    def _parse(self, category):
        cat_url = self.url + self.path[category]
        self._driver.get(cat_url)
        next_page_button = self._driver.find_element(By.CLASS_NAME, "next")
        pages = int(next_page_button.find_element(By.XPATH, "./preceding-sibling::*[1]").text)
        hrefs = []
        for i in range(1, pages + 1):
            print(i)
            if i > 1:
                self._driver.get(f"{cat_url}?PAGEN_1={i}")

            articles = self._driver.find_elements(By.CLASS_NAME, "tile-product")
            for art in articles: 
                hrefs.append(art.find_element(By.CLASS_NAME, "image").get_attribute("href"))

        for href in hrefs:
            try:
                self._driver.get(href)
                data = {}
                data["Название"] = self._driver.find_element(By.XPATH, "//div[@class='txt']/h1").text
                try:
                    data["Цена"] = self._driver.find_element(By.CLASS_NAME, "new-price").text
                except exceptions.NoSuchElementException:
                    data["Цена"] = self._driver.find_element(By.CLASS_NAME, "normal-price").text

                show_more_button = self._driver.find_element(By.XPATH, "//a[@class='link-details collapsed']") 
                self._driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", show_more_button)

                characteristics = self._driver.find_elements(By.XPATH, "//tbody/tr")
                for ch in characteristics:
                    p1, p2 = ch.find_elements(By.XPATH, "td/p")
                    data[p1.text] = p2.text

                yield href, data

            except Exception as e:
                print(e)

