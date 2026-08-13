import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from seleniumpagefactory.Pagefactory import PageFactory


class StudentRegistrationPage(PageFactory):
    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    # =========================
    # ИНИЦИАЛИЗАЦИЯ
    # =========================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.locators = {
            "first_name": ("ID", "firstName"),
            "last_name": ("ID", "lastName"),
            "email": ("ID", "userEmail"),
            "user_number": ("ID", "userNumber"),
            "date_input": ("ID", "dateOfBirthInput"),
            "subjects_input": ("ID", "subjectsInput"),
            "upload_picture": ("ID", "uploadPicture"),
            "current_address": ("ID", "currentAddress"),
            "state_dropdown": ("ID", "state"),
            "city_dropdown": ("ID", "city"),
            "submit_btn": ("ID", "submit"),

            "close_banner_btn": ("XPATH", "//*[@id='fixedban']/div/div/button"),

            "modal_title": ("ID", "example-modal-sizes-title-lg"),
            "result_table": ("CLASS_NAME", "table-responsive"),
        }


    # =========================
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # =========================
    def open(self):
        self.driver.get(self.URL)


    def close_banner(self):
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='fixedban']/div/div/button"))
            )
            self.close_banner_btn.click_button()
            self.wait.until(EC.invisibility_of_element_located((By.ID, "fixedban")))
        except TimeoutException:
            pass


    def open_and_prepare(self):
        self.open()
        self.close_banner()


    def submit(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "submit")))
        self.driver.execute_script("arguments[0].click();", self.submit_btn)


    # =========================
    # ЗАПОЛНЕНИЕ ПОЛЕЙ
    # =========================
    def enter_first_name(self, first_name: str):
        self.first_name.set_text(first_name)


    def enter_last_name(self, last_name: str):
        self.last_name.set_text(last_name)


    def enter_email(self, email: str):
        self.email.set_text(email)


    def select_gender(self, gender_number: int):
        gender_locator = (By.CSS_SELECTOR, f"label[for='gender-radio-{gender_number}']")
        self.wait.until(EC.element_to_be_clickable(gender_locator)).click()


    def enter_phone(self, phone: str):
        self.user_number.set_text(phone)


    def enter_subject(self, subject: str):
        self.subjects_input.set_text(subject)
        self.subjects_input.send_keys(Keys.ENTER)


    def select_hobby(self, hobby_number: int):
        hobby_locator = (By.CSS_SELECTOR, f"label[for='hobbies-checkbox-{hobby_number}']")
        self.wait.until(EC.element_to_be_clickable(hobby_locator)).click()


    def upload_file(self, file_name: str):
        file_path = os.path.abspath(file_name)
        self.upload_picture.send_keys(file_path)


    def enter_address(self, address: str):
        self.current_address.set_text(address)


    def select_state(self, state_name: str):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.state_dropdown.click_button()

        state_option = (By.XPATH, f"//div[text()='{state_name}']")
        self.wait.until(EC.element_to_be_clickable(state_option)).click()


    def select_city(self, city_name: str):
        self.city_dropdown.click_button()

        city_option = (By.XPATH, f"//div[text()='{city_name}']")
        self.wait.until(EC.element_to_be_clickable(city_option)).click()


    # =========================
    # ЗАПОЛНЕНИЕ ТОЛЬКО ОБЯЗАТЕЛЬНЫХ ПОЛЕЙ
    # =========================
    def fill_required_fields(self, first_name, last_name, gender, phone):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.select_gender(gender)
        self.enter_phone(phone)


    # -------------------------
    # ВСПОМОГАТЕЛЬНЫЕ ПРОВЕРКИ
    # -------------------------
    def check_success_modal(self):
        self.wait.until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
        assert self.modal_title.text == "Thanks for submitting the form"


    def is_success_modal_opened(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
            return True
        except TimeoutException:
            return False


    def check_user_in_table(self, text: str):
        table = self.result_table
        assert text in table.text
