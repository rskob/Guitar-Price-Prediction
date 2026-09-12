from ..main_parser import SubParser
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains


class GuitarParser(SubParser):
    def parse(self):
        pass

    def __enter__(self):
        wait = WebDriverWait(self._driver, 10)
        self._driver: Chrome
        search_field = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mt-header__search")))
        search_field.click()
        search_field.find_element(By.TAG_NAME, "input").send_keys("Электрогитары" + Keys.ENTER)

        sleep(1)

        checkbox_in_stock = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='checkbox-in-stock']/..")))
        ActionChains(self._driver).move_to_element(checkbox_in_stock).click().perform()

        checkbox_pre_order = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='checkbox-pre-order']/..")))
        ActionChains(self._driver).move_to_element(checkbox_pre_order).click().perform()

        sleep(5)
        


    def __exit__(self, exc_type, exc, tb):
        return super().__exit__(exc_type, exc, tb)
