from ..main_parser import Parser
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GuitarClubParser(Parser):
    url = "https://gitaraclub.ru"
    name = "Guitar Club"
    path = {"guitar": "/elektrogitary/", "bass": "/bas-gitary/"}

    def _parse(self, category: str):
        cat_url = self.url + self.path[category]
        self._driver.get(self.url + self.path[category])
        pagination = self._driver.find_elements(By.CLASS_NAME, "paginationEl")
        end = int(pagination[-1].text)
        print("END:", end)
        hrefs = []
        for i in range(1, end + 1):
            if i > 1: self._driver.get(f"{cat_url}?PAGEN_1={i}")
            articles = self._driver.find_elements(By.CLASS_NAME, "catalogEl")
            for art in articles:
                try:
                    hrefs.append(art.find_element(By.TAG_NAME,  "a").get_attribute("href"))
                except exceptions.NoSuchElementException:        
                    pass
            
            # next_page = self._driver.find_element(By.XPATH, f"//div[@class='pagination']//a[normalize-space(.)='{i + 1}']")
            # self._driver.execute_script("arguments[0].click();", next_page)

        for href in hrefs:
            try:
                self._driver.get(href)
                try:
                    element = self._driver.find_element(By.XPATH, "//div[@class='tabHeader']//span[@data-id='cardDetails']")
                    self._driver.execute_script("arguments[0].click();", element)
                except exceptions.NoSuchElementException:
                    continue
                except exceptions.ElementNotInteractableException:
                    pass

                characteristics = self._driver.find_elements(By.CLASS_NAME, "cardDetailsEl")
                data = {}
                data["Цена"] = self._driver.find_element(By.CLASS_NAME, "cardPriceCurrent").text
                data["Название"] = self._driver.find_element(By.XPATH, "//div[@class='cardTitle']").text
                for ch in characteristics:
                    title, value = ch.text.split(": ")
                    data[title] = value

                yield href, data
            except:
                pass

