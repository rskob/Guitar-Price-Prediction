from parse.main_parser import Parser, SubParser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions


class MuztorgSubParser(SubParser):
    def parse(self):
        hrefs = []
        pagination = self._driver.find_element(By.CLASS_NAME, "pagination-container__list")
        pagination_next = WebDriverWait(pagination, 10).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))[-1]
        count = 1
        while True:
            articles = self._driver.find_element(By.CLASS_NAME, "catalog-listing").find_elements(By.TAG_NAME, "article")
            for art in articles:
                try:
                    hrefs.append(art.find_element(By.TAG_NAME,  "link").get_attribute("href"))
                except exceptions.NoSuchElementException:        
                    pass
        
            pagination = self._driver.find_element(By.CLASS_NAME, "pagination-container__list")   
            print("Page:", count)                 
            pagination_next = WebDriverWait(pagination, 10).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))[-1]
            if pagination_next.get_attribute("class") == "pagination-container__item _next _disabled":
                break
    
            pagination_next.click()
            count += 1
    
        c, l = 1, len(hrefs)
        for href in hrefs:
            print(f"Item: {c}/{l}")
            c += 1
            url = href + "?view_tab=characteristics"
            self._driver.get(url)
            characteristics = WebDriverWait(self._driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "mt-product-characteristics__item")))
            data = {}
            data["Название"] = WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "title-2"))).text
    
            for ch in characteristics:
                title = ch.find_element(By.CLASS_NAME, "mt-product-characteristics__title").text
                value = ch.find_element(By.CLASS_NAME, "mt-product-characteristics__value").text
                data[title] = value
    
            yield url, data
            
    
    def __enter__(self):
        wait = WebDriverWait(self._driver, 10)
        search_field = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mt-header__search")))
        search_field.click()
        search_field.find_element(By.TAG_NAME, "input").send_keys(self._query + Keys.ENTER)

        checkbox_in_stock = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='checkbox-in-stock']/..")))
        ActionChains(self._driver).move_to_element(checkbox_in_stock).click().perform()
    
        checkbox_pre_order = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='checkbox-pre-order']/..")))
        ActionChains(self._driver).move_to_element(checkbox_pre_order).click().perform()
    
        return self