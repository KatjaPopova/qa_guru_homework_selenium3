import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.login_page import LoginPage


@pytest.fixture()
def login_page(driver):
    page = LoginPage(driver)
    page.open()
    return page


# Позитивные тесты:
# 1. Неудачная попытка залогиниться (не удалось найти успешный способ это сделать):
def test_unsuccessful_login(login_page):
    login_page.perform_login("Ekaterina", "123456")
    assert login_page.get_error_message() == "Wrong login or password"


# 2. Проверка ввода текста в поля формы:
def test_input_fields(login_page):
    login_page.perform_login("Ekaterina", "123456")

    login = login_page.driver.find_element(*login_page.LOGIN_INPUT)
    password = login_page.driver.find_element(*login_page.PASSWORD_INPUT)

    assert login.get_attribute("value") == "Ekaterina"
    assert password.get_attribute("value") == "123456"


# 3. Проверка кнопки Login:
def test_button_login_enabled(login_page):
    button = login_page.driver.find_element(*login_page.LOGIN_BUTTON)
    assert button.is_enabled()


# Негативные тесты:
# 1. Корректный Login, некорректный Password
def test_invalid_password_valid_login(login_page):
    login_page.perform_login("Ekaterina", "invalid")
    assert login_page.get_error_message() == "Wrong login or password"


# 2. Отправка формы с пустыми полями Login и Password:
def test_all_empty_fields(login_page):
    login_page.driver.find_element(*login_page.LOGIN_BUTTON).click()
    assert login_page.get_error_message() == "Login and password are required (minimum 3 and 6 characters)"


# 3. Отправка формы с пустым полем Login:
def test_empty_field_login(login_page):
    login_page.perform_login("", "123456")
    assert login_page.get_error_message() == "Login is required (minimum 3 characters)"


# 4. Отправка формы с пустым полем Password:
def test_empty_field_password(login_page):
    login_page.perform_login("Ekaterina", "")
    assert login_page.get_error_message() == "Password is required (minimum 6 characters)"


# 5. Слишком короткий Login:
def test_too_short_login(login_page):
    login_page.perform_login("Hi", "123456")
    assert login_page.get_error_message() == "Login must be at least 3 characters"


# 6. Слишком короткий Password:
def test_too_short_password(login_page):
    login_page.perform_login("Ekaterina", "123")
    assert login_page.get_error_message() == "Password must be at least 6 characters"


# 7. SQL-инъекция:
def test_sql_injection_in_login_field(login_page):
    payload = "' OR 1=1 --"
    login_page.perform_login(payload, "123456")
    assert login_page.get_error_message() == "Wrong login or password"


# 8. XSS-инъекция:
def test_xss_injection_in_login_field(login_page):
    payload = "<script>alert('XSS')</script>"
    login_page.perform_login(payload, "123456")

    with pytest.raises(TimeoutException):
        WebDriverWait(login_page.driver, 3).until(EC.alert_is_present())
