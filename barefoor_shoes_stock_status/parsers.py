from typing import Set
from selenium import webdriver


class VivoParser:
    url: str
    driver: webdriver.Firefox

    def __init__(self, url: str):
        self.url = url
        self._init_driver()

    def _open(self):
        self.driver.get(self.url)

    def _close(self):
        self.driver.close()

    def _init_driver(self):
        driver = webdriver.Firefox()
        self.driver = driver

    def load_site(self) -> str:
        try:
            self._open()
            page_source = self.driver.page_source
        finally:
            self._close()
        return page_source

    def load_stock(self) -> Set[str]:
        try:
            self._open()
            driver = self.driver
            size_select_elem = driver.find_element_by_class_name("select")
            sizes = size_select_elem.find_elements_by_tag_name("option")
            stock = {size.get_attribute("text") for size in sizes}
            stock = {size for size in stock if not size.startswith("Size")}
        finally:
            self._close()
        return stock
