from selenium.common import NoSuchElementException, StaleElementReferenceException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# =========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =========================

def fill_text_form(text_box_page, name="", email="", currentAddress="", permanentAddress=""):
    # Explicit Wait + expected_conditions
    wait = WebDriverWait(text_box_page, 10)

    user_name = wait.until(EC.visibility_of_element_located((By.ID, "userName")))
    user_name.clear()
    user_name.send_keys(name)

    user_email = wait.until(EC.visibility_of_element_located((By.ID, "userEmail")))
    user_email.clear()
    user_email.send_keys(email)

    current_address = wait.until(EC.visibility_of_element_located((By.ID, "currentAddress")))
    current_address.clear()
    current_address.send_keys(currentAddress)

    permanent_address = wait.until(EC.visibility_of_element_located((By.ID, "permanentAddress")))
    permanent_address.clear()
    permanent_address.send_keys(permanentAddress)


def submit_text_form(text_box_page):
    wait = WebDriverWait(text_box_page, 10)

    submit_button = wait.until(
        EC.element_to_be_clickable((By.ID, "submit"))
    )
    submit_button.click()

    # Использование Fluent Wait:
    wait = WebDriverWait(
        text_box_page,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException]
    )

    # Explicit Wait + expected_conditions
    return wait.until(
        EC.visibility_of_element_located((By.ID, "output"))
    )


def submit_without_wait(text_box_page):
    text_box_page.find_element(By.ID, "submit").click()


def submit_text_form_with_name_payload(text_box_page, payload):
    fill_text_form(
        text_box_page,
        name=payload,
        email="petrov@example.com",
        currentAddress="Москва",
        permanentAddress="Санкт-Петербург"
    )
    submit_text_form(text_box_page)


def get_result_box(text_box_page):
    return text_box_page.find_element(By.ID, "output")


def assert_result_contains(result_box, name="", email="", currentAddress="", permanentAddress=""):
    assert result_box.is_displayed()

    assert name in result_box.text
    assert email in result_box.text
    assert currentAddress in result_box.text
    assert permanentAddress in result_box.text


def check_form(text_box_page, name="", email="", currentAddress="", permanentAddress=""):
    fill_text_form(text_box_page, name, email, currentAddress, permanentAddress)
    result_box = submit_text_form(text_box_page)
    assert_result_contains(result_box, name, email, currentAddress, permanentAddress)


def assert_email_validation_error(text_box_page, email):
    fill_text_form(
        text_box_page,
        name="Петр Петров",
        email=email,
        currentAddress="Москва",
        permanentAddress="Санкт-Петербург"
    )

    submit_without_wait(text_box_page)

    error_text = text_box_page.find_element(By.ID, "userEmail").get_attribute("validationMessage")

    assert error_text != ""


# =========================
# ✅ ПОЗИТИВНЫЕ ТЕСТЫ
# =========================

def test_all_fields_filled_with_cyrillic_letters(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Москва",
        permanentAddress="Санкт-Петербург"
    )


# 2. Все поля формы заполнены латиницей:
def test_all_fields_filled_with_latin_letters(text_box_page):
    check_form(
        text_box_page,
        name="Olga Ivanova",
        email="olgaivanova@example.com",
        currentAddress="Moscow",
        permanentAddress="Saint-Petersburg"
    )


# 3. В поле Full Name указано полное ФИО (с отчеством):
def test_name_surname_patronymic_in_name_field(text_box_page):
    check_form(
        text_box_page,
        name="Петров Петр Петрович",
        email="petrov@example.com",
        currentAddress="Москва",
        permanentAddress="Санкт-Петербург"
    )


# 4. В поле Full Name указано короткое значение:
def test_short_name(text_box_page):
    check_form(
        text_box_page,
        name="Ян",
        email="yan@example.com",
        currentAddress="Москва",
        permanentAddress="Сочи"
    )


# 5. В поле Full Name указано длинное значение:
def test_long_name(text_box_page):
    check_form(
        text_box_page,
        name="Константинопольская Апполинария Максимилиановна",
        email="yan@example.com",
        currentAddress="Москва",
        permanentAddress="Сочи"
    )


# 6. В поле Full Name присутствует дефис:
def test_hyphen_in_name_field(text_box_page):
    check_form(
        text_box_page,
        name="Иван Мамин-Сибиряк",
        email="ivansibir@example.com",
        currentAddress="Москва",
        permanentAddress="Сочи"
    )


# 7. В поле Email буквы разных регистров:
def test_email_in_mixed_case(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="PetrovPetr@example.com",
        currentAddress="Казань",
        permanentAddress="Москва"
    )


# 8. В поле Email присутствуют цифры:
def test_numbers_in_email(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov1985@example.com",
        currentAddress="Тюмень",
        permanentAddress="Омск"
    )


# 9. Значения полей current_address и permanent_address совпадают:
def test_current_address_equals_permanent_address(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrovpetya@example.com",
        currentAddress="Москва",
        permanentAddress="Москва"
    )


# 10. В поле current_address указан адрес с городом, улицей, номерами дома и квартиры:
def test_current_address_with_city_street_house_flat(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Москва, ул. Тверская, дом 5, кв. 23",
        permanentAddress="Краснодар"
    )


# 11. В поле current_address указан адрес с городом, улицей, номерами дома, строения и квартиры:
def test_current_address_with_city_street_house_building_flat(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Москва, ул. Тверская, дом 5, корп. 1, кв. 23",
        permanentAddress="Краснодар"
    )


# 12. В поле current_address указан адрес с городом и улицей:
def test_current_address_only_city_and_street(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Москва, ул. Тверская",
        permanentAddress="Краснодар"
    )


# 13. В поле current_address указан длинный адрес:
def test_long_current_address(text_box_page):
    long_current_address: str = ("192177, г. Санкт-Петербург, Внутригородское "
                                 "муниципальное образование Санкт-Петербурга "
                                 "муниципальный округ Рыбацкое, Шлиссельбургский проспект, "
                                 "дом 24, корпус 2, строение 1, подвальный этаж, "
                                 "помещение 3-Н, комната 14, офис 5")
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress=long_current_address,
        permanentAddress="Краснодар"
    )


# 14. В поле current_address указан короткий адрес:
def test_short_current_address(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Уфа",
        permanentAddress="Краснодар"
    )


# 15. В поле current_address присутствуют спецсимволы:
def test_current_address_contains_symbols(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="г. Санкт-Петербург, Невский пр., д. 15/2, кв. №34",
        permanentAddress="Пермь"
    )


# 16. В поле permanent_address указан адрес с городом, улицей, номерами дома и квартиры:
def test_permanent_address_with_city_street_house_flat(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Казань",
        permanentAddress="Москва, ул. Тверская, дом 5, кв. 23"
    )


# 17. В поле permanent_address указан адрес с городом, улицей, номерами дома, строения и квартиры:
def test_permanent_address_with_city_street_house_building_flat(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Казань",
        permanentAddress="Москва, ул. Тверская, дом 5, корп. 1, кв. 23"
    )


# 18. В поле permanent_address указан адрес с городом и улицей:
def test_permanent_address_only_city_and_street(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Казань",
        permanentAddress="Москва, ул. Тверская"
    )


# 19. В поле permanent_address указан длинный адрес:
def test_long_permanent_address(text_box_page):
    long_permanent_address: str = ("192177, г. Санкт-Петербург, Внутригородское "
                                   "муниципальное образование Санкт-Петербурга "
                                   "муниципальный округ Рыбацкое, Шлиссельбургский проспект, "
                                   "дом 24, корпус 2, строение 1, подвальный этаж, "
                                   "помещение 3-Н, комната 14, офис 5")
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Казань",
        permanentAddress=long_permanent_address
    )


# 20. В поле permanent_address указан короткий адрес:
def test_short_permanent_address(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Мурманск",
        permanentAddress="Уфа"
    )


# 21. В поле permanent_address присутствуют спецсимволы:
def test_permanent_address_contains_symbols(text_box_page):
    check_form(
        text_box_page,
        name="Петр Петров",
        email="petrov@example.com",
        currentAddress="Пермь",
        permanentAddress="г. Санкт-Петербург, Невский пр., д. 15/2, кв. №34"
    )


# 22. Форма отправляется, если все поля формы пустые (позитивная проверка, так как все поля формы необязательные):
# Падает из-за опечатки на странице ("permananet" вместо "permanent")
def test_text_form_sent_if_all_fields_empty(text_box_page):
    check_form(text_box_page)


# Негативные тесты:
# 1. Email без символа @:
def test_email_with_no_mail_symbol(text_box_page):
    assert_email_validation_error(text_box_page, "petrovexample.com")


# 2. В поле Email используется кириллица:
def test_cyrillic_letters_in_email(text_box_page):
    assert_email_validation_error(text_box_page, "петров@example.com")


# 3. В поле Email два символа @@:
def test_email_with_two_mail_symbols(text_box_page):
    assert_email_validation_error(text_box_page, "petrov@@example.com")


# 4. В поле Email спецсимволы:
def test_special_symbols_in_email_field(text_box_page):
    assert_email_validation_error(text_box_page, "petrov[]@example.com")


# 5. В поле Email пробел:
def test_space_in_email_field(text_box_page):
    assert_email_validation_error(text_box_page, "petrov @example.com")


# 6. HTML-иньекция (тест падает, так как html выполняется):
def test_html_injection(text_box_page):
    payload = "<div id='hack'>Hello</div>"

    submit_text_form_with_name_payload(text_box_page, payload)

    html_elements = text_box_page.find_elements(By.ID, "hack")

    assert len(html_elements) == 0


# 7. XSS-иньекция:
def test_xss_injection(text_box_page):
    payload = "<script>alert(1)</script>"

    submit_text_form_with_name_payload(text_box_page, payload)

    try:
        alert = text_box_page.switch_to.alert
        assert False, f"XSS работает! Alert: {alert.text}"
    except NoAlertPresentException:
        pass
