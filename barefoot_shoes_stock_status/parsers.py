from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from barefoot_shoes_stock_status.models import StockItem, StockStatus


class VivoParser:
    url: str
    driver_class = webdriver.Firefox

    def __init__(self, url: str):
        self.url = url

    def load_site(self) -> str:
        try:
            driver = self.driver_class()
            driver.get(self.url)
            page_source = driver.page_source
        finally:
            driver.close()
        return page_source

    def load_stock(self) -> StockStatus:
        try:
            driver = self.driver_class()
            driver.get(self.url)
            size_select_elem = driver.find_element_by_class_name("select")
            sizes = size_select_elem.find_elements_by_tag_name("option")
            stock = {size.get_attribute("text") for size in sizes}
            stock = {
                StockItem.from_vivo_str(size)
                for size in stock
                if not size.startswith("Size")
            }
        finally:
            driver.close()
        return StockStatus(stock, url=self.url)
