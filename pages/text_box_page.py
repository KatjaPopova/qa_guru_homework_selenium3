from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TextBoxPage:
    URL = "https://demo.qa.guru/one-page-form/text-box.html"

    USER_NAME = (By.ID, "userName")
    USER_EMAIL = (By.ID, "userEmail")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    PERMANENT_ADDRESS = (By.ID, "permanentAddress")

    SUBMIT = (By.ID, "submit")
    OUTPUT = (By.ID, "output")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def fill_text_form(self, name="", email="", current_address="", permanent_address=""):
        name_element = self.driver.find_element(*self.USER_NAME)
        email_element = self.driver.find_element(*self.USER_EMAIL)
        current_address_element = self.driver.find_element(*self.CURRENT_ADDRESS)
        permanent_address_element = self.driver.find_element(*self.PERMANENT_ADDRESS)

        name_element.clear()
        name_element.send_keys(name)

        email_element.clear()
        email_element.send_keys(email)

        current_address_element.clear()
        current_address_element.send_keys(current_address)

        permanent_address_element.clear()
        permanent_address_element.send_keys(permanent_address)

    def submit_text_form(self):
        self.driver.find_element(*self.SUBMIT).click()
        self.wait.until(
            EC.visibility_of_element_located(self.OUTPUT)
        )

    def submit_without_wait(self):
        self.driver.find_element(*self.SUBMIT).click()

    def submit_text_form_with_name_payload(self, payload):
        self.fill_text_form(
            name=payload,
            email="petrov@example.com",
            current_address="Москва",
            permanent_address="Санкт-Петербург"
        )
        self.submit_text_form()

    def get_result_box(self):
        return self.wait.until(EC.visibility_of_element_located(self.OUTPUT))

    def get_result_text(self) -> str:
        return self.get_result_box().text

    def get_email_validation_message(self) -> str:
        return self.driver.find_element(*self.USER_EMAIL).get_attribute("validationMessage")

    def submit_filled_form(self, name="", email="", current_address="", permanent_address="") -> str:
        self.fill_text_form(
            name=name,
            email=email,
            current_address=current_address,
            permanent_address=permanent_address,
        )
        self.submit_text_form()
        return self.get_result_text()
