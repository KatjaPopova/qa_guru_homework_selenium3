from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TableElement:

    def __init__(self, driver, locator, timeout=5):
        self.driver = driver
        self.locator = locator
        self.timeout = timeout

    def wait_visible(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.locator)
        )
        return self

    @property
    def element(self):
        return self.driver.find_element(*self.locator)

    def is_displayed(self):
        return self.element.is_displayed()

    def get_headers(self) -> list[str]:
        """Возвращает список заголовков таблицы."""
        headers = self.element.find_elements(By.CSS_SELECTOR, "thead th")
        return [header.text for header in headers]

    def get_row_data(self, row_index: int) -> list[str]:
        """Возвращает данные конкретной строки по её индексу (начиная с 0)."""
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        return [cell.text for cell in cells]

    def get_cell_value(self, row_index: int, column_index: int) -> str:
        """Возвращает значение конкретной ячейки."""
        row_data = self.get_row_data(row_index)
        return row_data[column_index]

    def get_rows_count(self) -> int:
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        return len(rows)

    def get_columns_count(self) -> int:
        columns = self.element.find_elements(By.CSS_SELECTOR, "thead th")
        return len(columns)

    def user_with_due_exists(self, amount):
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells[3].text == amount:
                return True

        return False

    def all_rows_have_buttons_edit_and_delete(self):
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            action_cell = cells[5].text.lower()

            if "edit" not in action_cell or "delete" not in action_cell:
                return False

        return True

    def get_all_emails(self):
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        emails = []

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            emails.append(cells[2].text)

        return emails

    def user_exists(self, last_name):
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells[0].text == last_name:
                return True

        return False
