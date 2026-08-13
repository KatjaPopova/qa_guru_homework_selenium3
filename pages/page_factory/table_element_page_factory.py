from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory


class TableElement(PageFactory):

    def __init__(self, driver, table_locator=("CSS", "table"), timeout=5):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

        how, what = table_locator
        self.locators = {
            "table": (how, what)
        }

    def wait_visible(self):
        self.wait.until(EC.visibility_of(self.table))
        return self

    @property
    def element(self):
        return self.table

    def is_displayed(self) -> bool:
        return self.element.is_displayed()

    def get_headers(self) -> list[str]:
        headers = self.element.find_elements(By.CSS_SELECTOR, "thead th")
        return [h.text for h in headers]

    def get_row_data(self, row_index: int) -> list[str]:
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        return [c.text for c in cells]

    def get_cell_value(self, row_index: int, column_index: int) -> str:
        return self.get_row_data(row_index)[column_index]

    def get_rows_count(self) -> int:
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        return len(rows)

    def get_columns_count(self) -> int:
        cols = self.element.find_elements(By.CSS_SELECTOR, "thead th")
        return len(cols)

    def user_with_due_exists(self, amount: str) -> bool:
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells[3].text == amount:
                return True
        return False

    def all_rows_have_buttons_edit_and_delete(self) -> bool:
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            action_cell = cells[5].text.lower()
            if "edit" not in action_cell or "delete" not in action_cell:
                return False
        return True

    def get_all_emails(self) -> list[str]:
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        return [row.find_elements(By.TAG_NAME, "td")[2].text for row in rows]

    def user_exists(self, last_name: str) -> bool:
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells[0].text == last_name:
                return True
        return False