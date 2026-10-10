from ..main_parser import Parser
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class MusikRoomParser(Parser):
    url = "https://muzikroom.ru"
    name = "Muzik Room"
    path = {"guitar": "/shop/elektrogitary/instock/"}

    def _parse(self, category):
        cat_url = self.url + self.path[category]
        self._driver.get(cat_url)

        last_page_href = self._driver.find_element(By.XPATH, "//a[@style='text-decoration: none;']").get_attribute("href")
        pages = int(last_page_href.replace(f"{cat_url}page-", "")[:-1])

        hrefs = []
        for i in range(1, pages + 1):
            print(i)
            if i > 1:
                self._driver.get(f"{cat_url}page-{i}")

            articles = self._driver.find_elements(By.XPATH, "//div[@class='catalog-list']/div")
            for art in articles:
                hrefs.append(art.get_attribute("data-url"))


        print(len(hrefs))
        for href in hrefs:
            try:
                url = self.url + href
                self._driver.get(url)

                data = {}
                data["Название"] = self._driver.find_element(By.CLASS_NAME, "name").text
                data["Цена"] = self._driver.find_element(By.CLASS_NAME, "price").text

                params_button = self._driver.find_element(By.XPATH, "//a[@data-id='params']")
                self._driver.execute_script("arguments[0].click();", params_button)

                show_all_button = self._driver.find_element(By.CLASS_NAME, "js-show-all")
                self._driver.execute_script("arguments[0].click();", show_all_button)
                
                params = self._driver.find_elements(By.CLASS_NAME, "params-row")
                
                for param in params:
                    key = param.find_element(By.CLASS_NAME, "param-name").text
                    value = param.find_element(By.CLASS_NAME, "param-val").text
                    data[key] = value

                yield url, data
            except Exception as e:
                print(e)
