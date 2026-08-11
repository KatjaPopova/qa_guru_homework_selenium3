from selenium.webdriver.common.by import By

from pages.table_element import TableElement


class TablesPage:
    URL = "https://the-internet.herokuapp.com/tables"

    def __init__(self, driver):
        self.driver = driver

        self.table1 = TableElement(driver, (By.ID, "table1"))
        self.table2 = TableElement(driver, (By.ID, "table2"))

    def open(self):
        self.driver.get(self.URL)
