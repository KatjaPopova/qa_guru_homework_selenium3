from selenium.common import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# =========================
# ЛОКАТОРЫ
# =========================

LOGIN_INPUT = (By.CSS_SELECTOR, "[data-testid='login-input']")
PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='password-input']")
LOGIN_BUTTON = (By.XPATH, "//button[text()='Login']")
ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='error-message']")


# =========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =========================

def perform_login(login_page, login="", password=""):
    wait = WebDriverWait(login_page, 10)

    # Explicit Wait + expected_conditions
    login_input = wait.until(EC.visibility_of_element_located(LOGIN_INPUT))
    password_input = wait.until(EC.visibility_of_element_located(PASSWORD_INPUT))
    login_button = wait.until(EC.element_to_be_clickable(LOGIN_BUTTON))

    login_input.clear()
    password_input.clear()

    if login:
        login_input.send_keys(login)
    if password:
        password_input.send_keys(password)

    login_button.click()


def get_error_message(login_page):
    # Использование Fluent Wait:
    wait = WebDriverWait(
        login_page,
        timeout=10,
        poll_frequency=0.3,
        ignored_exceptions=[NoSuchElementException]
    )
    # Explicit Wait + expected_conditions
    return wait.until(
        EC.visibility_of_element_located(ERROR_MESSAGE)
    ).text


# Позитивные тесты:
# 1. Неудачная попытка залогиниться (не удалось найти успешный способ это сделать):
def test_unsuccessful_login(login_page):
    perform_login(login_page, "Ekaterina", "123456")

    assert get_error_message(login_page) == "Wrong login or password"


# 2. Проверка ввода текста в поля формы:
def test_input_fields(login_page):
    perform_login(login_page, "Ekaterina", "123456")

    login = login_page.find_element(*LOGIN_INPUT)
    password = login_page.find_element(*PASSWORD_INPUT)

    assert login.get_attribute("value") == "Ekaterina"
    assert password.get_attribute("value") == "123456"


# 3. Проверка кнопки Login:
def test_button_login_enabled(login_page):
    button = WebDriverWait(login_page, 10).until(EC.element_to_be_clickable(LOGIN_BUTTON))

    assert button.is_enabled()


# Негативные тесты:
# 1. Корректный Login, некорректный Password
def test_invalid_password_valid_login(login_page):
    perform_login(login_page, "Ekaterina", "invalid")

    assert get_error_message(login_page) == "Wrong login or password"


# 2. Отправка формы с пустыми полями Login и Password:
def test_all_empty_fields(login_page):
    login_page.find_element(*LOGIN_BUTTON).click()

    assert get_error_message(login_page) == "Login and password are required (minimum 3 and 6 characters)"


# 3. Отправка формы с пустым полем Login:
def test_empty_field_login(login_page):
    perform_login(login_page, "", "123456")

    assert get_error_message(login_page) == "Login is required (minimum 3 characters)"


# 4. Отправка формы с пустым полем Password:
def test_empty_field_password(login_page):
    perform_login(login_page, "Ekaterina", "")

    assert get_error_message(login_page) == "Password is required (minimum 6 characters)"


# 5. Слишком короткий Login:
def test_too_short_login(login_page):
    perform_login(login_page, "Hi", "123456")

    assert get_error_message(login_page) == "Login must be at least 3 characters"


# 6. Слишком короткий Password:
def test_too_short_password(login_page):
    perform_login(login_page, "Ekaterina", "123")

    assert get_error_message(login_page) == "Password must be at least 6 characters"


# 7. SQL-инъекция:
def test_sql_injection_in_login_field(login_page):
    payload = "' OR 1=1 --"
    perform_login(login_page, payload, "123456")

    assert get_error_message(login_page) == "Wrong login or password"


# 8. XSS-инъекция:
def test_xss_injection_in_login_field(login_page):
    payload = "<script>alert('XSS')</script>"
    perform_login(login_page, payload, "123456")

    try:
        login_page.switch_to.alert
        assert False, "XSS сработал!"
    except NoAlertPresentException:
        pass
