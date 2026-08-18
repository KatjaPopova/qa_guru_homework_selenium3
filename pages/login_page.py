from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class LoginPage:
    URL = "https://demo.qa.guru/one-page-form/login.html"

    LOGIN_INPUT = (By.CSS_SELECTOR, "[data-testid='login-input']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='password-input']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Login']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='error-message']")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def perform_login(self, login="", password=""):
        login_input = self.driver.find_element(*self.LOGIN_INPUT)
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)

        login_input.clear()
        password_input.clear()

        if login:
            login_input.send_keys(login)
        if password:
            password_input.send_keys(password)

        login_button.click()

    def get_error_message(self, timeout=5) -> str:
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        ).text
