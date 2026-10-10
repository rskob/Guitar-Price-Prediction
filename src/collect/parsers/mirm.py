from ..main_parser import Parser
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC

class MIRMParser(Parser):
    url = "https://mirm.ru"
    name = "Мир музыки"
    path = {"guitar" :"/catalog/gitari/elektrogitari/?ybaip=1"}

    def _parse(self, category):
        cat_url = self.url + self.path[category]
        print(cat_url)
        self._driver.get(cat_url)
        pages = int(self._driver.find_element(By.CLASS_NAME, "pagination").find_elements(By.TAG_NAME, "li")[-2].text)
        print(pages)
        hrefs = []
        for i in range(1, pages + 1):
            if i > 1:
                self._driver.get(f"{cat_url}&PAGEN_1={i}")

            articles = self._driver.find_element(By.CLASS_NAME, "showcase-list").find_elements(By.CLASS_NAME, "showcase-item-basic")
            for art in articles:
                try:
                    hrefs.append(art.find_element(By.TAG_NAME, "a").get_attribute("href"))
                except exceptions.NoSuchElementException:
                    pass

        for href in hrefs:
            try:
                self._driver.get(href)
                data = {}
                text = self._driver.find_element(By.CLASS_NAME, "mobile-tabler-content-in").get_attribute("innerHTML")
                data["Название"] = self._driver.find_element(By.XPATH, "//div[@class='inner']/h1").text
                data["Цена"] = self._driver.find_element(By.XPATH, "//div[@id='results-price']/span[not(@class)]").text

                for line in text.splitlines():
                    line = line.strip()
                    if ":" in line:
                        key, value = line.split(":", 1)
                        data[key] = value
                self._wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='tabler-nav-item']/span[contains(text(), 'Характеристики')]"))).click()
                trs = self._driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
                for el in trs:
                    td1, td2 = el.find_elements(By.TAG_NAME, "td")
                    data[td1.text] = td2.text

                yield href, data
            except Exception as e:
                print(e)
