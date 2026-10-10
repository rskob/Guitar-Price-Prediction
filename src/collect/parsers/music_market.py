from ..main_parser import Parser
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class MusicMarketParser(Parser):
    url = "https://music-market13.ru"
    name = "MUSIC MARKET"
    path = {"guitar": "/gitary/gitary-elektrogitary/"}

    def _parse(self, category):
        cat_url = self.url + self.path[category]
        self._driver.get(cat_url)
        hrefs = set()
        while True:
            articles = self._wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@class='cardnew']/a")))
            for art in articles:
                hrefs.add(art.get_attribute("href"))

            try:
                show_more_button = self._driver.find_element(By.ID, "showmore-button")
                show_more_button.click()
                # self._driver.execute_script("arguments[0].scrollIntoView();arguments[0].click();", show_more_button)
            except Exception as e:
                break

            print(len(hrefs))

        print(len(hrefs))
        for href in hrefs:
            try:
                self._driver.get(href)
                data = {}
                data["Название"] = self._driver.find_element(By.CLASS_NAME, "producttitle").text
                data["Цена"] = self._driver.find_element(By.XPATH, "//div[@class='price']/span").text
                try:
                    attr_button = self._driver.find_element(By.XPATH, "//button[@data-drawer-open='attributes']")
                    self._driver.execute_script("arguments[0].click();", attr_button)
                except Exception:
                    pass

                attributes = self._driver.find_elements(By.CLASS_NAME, "attribute")
                for attr in attributes:
                    div1, div2 = attr.find_elements(By.TAG_NAME, "div")
                    data[div1.text] = div2.text

                yield href, data
            except Exception as e:
                print("EXCEPTION:", e)
