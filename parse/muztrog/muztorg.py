from parse.main_parser import Parser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from time import sleep


class MuztorgParser(Parser):
    start_url = "https://www.muztorg.ru/"

    def _prepare(self):
        wait = WebDriverWait(self._driver, 10)

        self._driver: Chrome
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "js-header-city"))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-select2-id="3"]'))).click()

        search_field = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-search__field")))
        search_field.send_keys("Москва")
        sleep(0.1)
        search_field.send_keys(Keys.ENTER)

