from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.student_registration_page import StudentRegistrationPage


# =========================
# ПОЗИТИВНЫЕ ТЕСТЫ
# =========================

# 1. Проверяем, что форма отправляется с обязательными полями:
def test_successful_submit_with_required_fields(driver):
    page = StudentRegistrationPage(driver).open_and_prepare()

    page.fill_required_fields("Петр", "Петров", gender=1, phone="8900000000")
    page.submit()

    page.check_success_modal()
    page.check_user_in_table("Петр")
    page.check_user_in_table("Петров")


# 2. Проверяем отправку формы, где выбраны все доступные Subjects:
def test_positive_select_all_subjects(driver):
    page = StudentRegistrationPage(driver).open_and_prepare()

    page.fill_required_fields("Ivan", "Petrov", gender=1, phone="9998887766")

    page.enter_subject("Maths")
    page.enter_subject("Physics")
    page.enter_subject("Chemistry")
    page.enter_subject("Biology")
    page.enter_subject("English")
    page.enter_subject("Computer Science")
    page.enter_subject("Economics")
    page.enter_subject("History")
    page.enter_subject("Hindi")
    page.enter_subject("Civics")
    page.enter_subject("Arts")

    page.submit()

    page.check_success_modal()
    page.check_user_in_table("Maths")
    page.check_user_in_table("Physics")
    page.check_user_in_table("Chemistry")
    page.check_user_in_table("Biology")
    page.check_user_in_table("English")
    page.check_user_in_table("Computer Science")
    page.check_user_in_table("Economics")
    page.check_user_in_table("History")
    page.check_user_in_table("Hindi")
    page.check_user_in_table("Civics")
    page.check_user_in_table("Arts")


# 3. Проверяем отправку формы, где выбраны все доступные Hobbies:
def test_positive_select_all_hobbies(driver):
    page = StudentRegistrationPage(driver).open_and_prepare()

    page.fill_required_fields("Anna", "Ivanova", gender=2, phone="1112223344")

    page.select_hobby(1)
    page.select_hobby(2)
    page.select_hobby(3)

    page.submit()

    page.check_success_modal()
    page.check_user_in_table("Sports")
    page.check_user_in_table("Reading")
    page.check_user_in_table("Music")


# 4. После отправки формы ждём, пока в таблице результата появится текст "Sports" (Fluent Wait)
def test_fluent_wait_result_table_has_text(driver):
    page = StudentRegistrationPage(driver).open_and_prepare()

    page.fill_required_fields("Anna", "Ivanova", gender=2, phone="1112223344")
    page.select_hobby(1)  # Sports
    page.submit()

    wait = WebDriverWait(
        driver,
        timeout=6,
        poll_frequency=0.2,
        ignored_exceptions=(NoSuchElementException, StaleElementReferenceException)
    )

    wait.until(EC.text_to_be_present_in_element(page.RESULT_TABLE, "Sports"))

    page.check_user_in_table("Sports")

    # =========================
    # НЕГАТИВНЫЕ ТЕСТЫ
    # =========================


# 1. Проверяем, что пустая форма не отправляется:
def test_negative_empty_form_not_submitted(driver):
    page = StudentRegistrationPage(driver)
    page.open_and_prepare()

    page.submit()

    assert page.is_success_modal_opened() is False


# 2. Проверяем, что форма не отправляется без выбора пола:
def test_negative_without_gender_not_submitted(driver):
    page = StudentRegistrationPage(driver)
    page.open_and_prepare()

    page.enter_first_name("Ivan")
    page.enter_last_name("Petrov")
    page.enter_phone("9998887766")

    page.submit()

    assert page.is_success_modal_opened() is False


# 3. Проверяем, что форма не отправляется с невалидным номером телефона:
def test_negative_invalid_phone_not_submitted(driver):
    page = StudentRegistrationPage(driver)
    page.open_and_prepare()

    page.fill_required_fields("Ivan", "Petrov", gender=1, phone="12345")
    page.submit()

    assert page.is_success_modal_opened() is False
