from pages.table_element_page_factory import TableElement


class TablesPage:
    URL = "https://the-internet.herokuapp.com/tables"

    def __init__(self, driver):
        self.driver = driver

        # ВАЖНО: локаторы в PageFactory-формате (строкой)
        self.table1 = TableElement(driver, ("ID", "table1"))
        self.table2 = TableElement(driver, ("ID", "table2"))

    def open(self):
        self.driver.get(self.URL)
        return self