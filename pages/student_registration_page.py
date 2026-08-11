import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StudentRegistrationPage:

    # =========================
    # ЛОКАТОРЫ
    # =========================

    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    USER_NUMBER = (By.ID, "userNumber")
    DATE_INPUT = (By.ID, "dateOfBirthInput")
    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    UPLOAD_PICTURE = (By.ID, "uploadPicture")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    STATE_DROPDOWN = (By.ID, "state")
    CITY_DROPDOWN = (By.ID, "city")
    SUBMIT = (By.ID, "submit")

    CLOSE_BANNER = (By.XPATH, "//*[@id='fixedban']/div/div/button")

    MODAL_TITLE = (By.ID, "example-modal-sizes-title-lg")
    RESULT_TABLE = (By.CLASS_NAME, "table-responsive")


    # =========================
    # ИНИЦИАЛИЗАЦИЯ
    # =========================
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)


    # =========================
    # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # =========================
    def open(self):
        self.driver.get(self.URL)

    def close_banner(self):
        close_btn = self.wait.until(
            EC.element_to_be_clickable(self.CLOSE_BANNER)
        )
        close_btn.click()
        self.wait.until(EC.invisibility_of_element(close_btn))

    def open_and_prepare(self):
        self.open()
        try:
            self.close_banner()
        except TimeoutException:
            pass

        return self


    def submit(self):
        submit_button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT))
        self.driver.execute_script("arguments[0].click();", submit_button)

    # =========================
    # ЗАПОЛНЕНИЕ ПОЛЕЙ
    # =========================

    def enter_first_name(self, first_name):
        self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME)).send_keys(first_name)

    def enter_last_name(self, last_name):
        self.wait.until(EC.element_to_be_clickable(self.LAST_NAME)).send_keys(last_name)

    def enter_email(self, email):
        self.wait.until(EC.element_to_be_clickable(self.EMAIL)).send_keys(email)

    def select_gender(self, gender_number):
        gender_locator = (By.CSS_SELECTOR, f"label[for='gender-radio-{gender_number}']")
        self.wait.until(
            EC.element_to_be_clickable(gender_locator)
        ).click()

    def enter_phone(self, phone):
        self.wait.until(EC.element_to_be_clickable(self.USER_NUMBER)).send_keys(phone)

    def select_date(self, month, year, day):
        # Открываем календарь
        self.wait.until(EC.element_to_be_clickable(self.DATE_INPUT)).click()

        # Выбираем месяц
        month_dropdown = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__month-select")))
        month_dropdown.find_element(By.XPATH, f".//option[@value='{month}']").click()

        # Выбираем год
        year_dropdown = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__year-select")))
        year_dropdown.find_element(By.XPATH, f".//option[@value='{year}']").click()

        # Выбираем день
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f".react-datepicker__day--{day}:not(.react-datepicker__day--outside-month)"))).click()

    def enter_subject(self, subject):
        subject_input = self.wait.until(EC.element_to_be_clickable(self.SUBJECTS_INPUT))
        subject_input.send_keys(subject)
        subject_input.send_keys(Keys.ENTER)

    def select_hobby(self, hobby_number):
        hobby_locator = (By.CSS_SELECTOR, f"label[for='hobbies-checkbox-{hobby_number}']")
        self.wait.until(EC.element_to_be_clickable(hobby_locator)).click()

    def upload_file(self, file_name):
        file_path = os.path.abspath(file_name)
        self.wait.until(EC.presence_of_element_located(self.UPLOAD_PICTURE)).send_keys(file_path)

    def enter_address(self, address):
        self.wait.until(EC.element_to_be_clickable(self.CURRENT_ADDRESS)).send_keys(address)

    def select_state(self, state_name):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        self.wait.until(EC.element_to_be_clickable(self.STATE_DROPDOWN)).click()

        state_option = (By.XPATH, f"//div[text()='{state_name}']")

        self.wait.until(EC.element_to_be_clickable(state_option)).click()

    def select_city(self, city_name):
        self.wait.until(EC.element_to_be_clickable(self.CITY_DROPDOWN)).click()

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
        modal = self.wait.until(
            EC.visibility_of_element_located(self.MODAL_TITLE)
        )
        assert modal.text == "Thanks for submitting the form"


    def is_success_modal_opened(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.MODAL_TITLE))
            return True

        except TimeoutException:
            return False


    def check_user_in_table(self, text):
        table = self.driver.find_element(*self.RESULT_TABLE)
        assert text in table.text

