import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.text_box_page import TextBoxPage


@pytest.fixture()
def text_box_page(driver):
    page = TextBoxPage(driver)
    page.open()
    return page


def assert_result_contains(page, name="", email="", current_address="", permanent_address=""):
    text = page.get_result_text()

    assert name in text
    assert email in text
    assert current_address in text
    assert permanent_address in text


# =========================
# ПОЗИТИВНЫЕ ТЕСТЫ
# =========================

def test_all_fields_filled_with_cyrillic_letters(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Москва",
        "permanent_address": "Санкт-Петербург",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 2. Все поля формы заполнены латиницей:
def test_all_fields_filled_with_latin_letters(text_box_page):
    data = {
        "name": "Olga Ivanova",
        "email": "olgaivanova@example.com",
        "current_address": "Moscow",
        "permanent_address": "Saint-Petersburg",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 3. В поле Full Name указано полное ФИО (с отчеством):
def test_name_surname_patronymic_in_name_field(text_box_page):
    data = {
        "name": "Петров Петр Петрович",
        "email": "petrov@example.com",
        "current_address": "Москва",
        "permanent_address": "Санкт-Петербург",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 4. В поле Full Name указано короткое значение:
def test_short_name(text_box_page):
    data = {
        "name": "Ян",
        "email": "yan@example.com",
        "current_address": "Москва",
        "permanent_address": "Сочи",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 5. В поле Full Name указано длинное значение:
def test_long_name(text_box_page):
    data = {
        "name": "Константинопольская Апполинария Максимилиановна",
        "email": "constanta@example.com",
        "current_address": "Москва",
        "permanent_address": "Сочи",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 6. В поле Full Name присутствует дефис:
def test_hyphen_in_name_field(text_box_page):
    data = {
        "name": "Иван Мамин-Сибиряк",
        "email": "ivansibir@example.com",
        "current_address": "Москва",
        "permanent_address": "Сочи",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 7. В поле Email буквы разных регистров:
def test_email_in_mixed_case(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "PetrovPetr@example.com",
        "current_address": "Казань",
        "permanent_address": "Москва",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 8. В поле Email присутствуют цифры:
def test_numbers_in_email(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov1985@example.com",
        "current_address": "Тюмень",
        "permanent_address": "Омск",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 9. Значения полей current_address и permanent_address совпадают:
def test_current_address_equals_permanent_address(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrovpetya@example.com",
        "current_address": "Москва",
        "permanent_address": "Москва",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 10. В поле current_address указан адрес с городом, улицей, номерами дома и квартиры:
def test_current_address_with_city_street_house_flat(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Москва, ул. Тверская, дом 5, кв. 23",
        "permanent_address": "Краснодар",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 11. В поле current_address указан адрес с городом, улицей, номерами дома, строения и квартиры:
def test_current_address_with_city_street_house_building_flat(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Москва, ул. Тверская, дом 5, корп. 1, кв. 23",
        "permanent_address": "Краснодар",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 12. В поле current_address указан адрес с городом и улицей:
def test_current_address_only_city_and_street(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Москва, ул. Тверская",
        "permanent_address": "Краснодар",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 13. В поле current_address указан длинный адрес:
def test_long_current_address(text_box_page):
    long_current_address: str = ("192177, г. Санкт-Петербург, Внутригородское "
                                 "муниципальное образование Санкт-Петербурга "
                                 "муниципальный округ Рыбацкое, Шлиссельбургский проспект, "
                                 "дом 24, корпус 2, строение 1, подвальный этаж, "
                                 "помещение 3-Н, комната 14, офис 5")
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": long_current_address,
        "permanent_address": "Краснодар",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 14. В поле current_address указан короткий адрес:
def test_short_current_address(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Уфа",
        "permanent_address": "Краснодар",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 15. В поле current_address присутствуют спецсимволы:
def test_current_address_contains_symbols(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "г. Санкт-Петербург, Невский пр., д. 15/2, кв. №34",
        "permanent_address": "Пермь",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 16. В поле permanent_address указан адрес с городом, улицей, номерами дома и квартиры:
def test_permanent_address_with_city_street_house_flat(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Казань",
        "permanent_address": "Москва, ул. Тверская, дом 5, кв. 23",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 17. В поле permanent_address указан адрес с городом, улицей, номерами дома, строения и квартиры:
def test_permanent_address_with_city_street_house_building_flat(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Казань",
        "permanent_address": "Москва, ул. Тверская, дом 5, корп. 1, кв. 23",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 18. В поле permanent_address указан адрес с городом и улицей:
def test_permanent_address_only_city_and_street(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Казань",
        "permanent_address": "Москва, ул. Тверская",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 19. В поле permanent_address указан длинный адрес:
def test_long_permanent_address(text_box_page):
    long_permanent_address: str = ("192177, г. Санкт-Петербург, Внутригородское "
                                   "муниципальное образование Санкт-Петербурга "
                                   "муниципальный округ Рыбацкое, Шлиссельбургский проспект, "
                                   "дом 24, корпус 2, строение 1, подвальный этаж, "
                                   "помещение 3-Н, комната 14, офис 5")

    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Казань",
        "permanent_address": long_permanent_address,
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 20. В поле permanent_address указан короткий адрес:
def test_short_permanent_address(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Мурманск",
        "permanent_address": "Уфа",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 21. В поле permanent_address присутствуют спецсимволы:
def test_permanent_address_contains_symbols(text_box_page):
    data = {
        "name": "Петр Петров",
        "email": "petrov@example.com",
        "current_address": "Пермь",
        "permanent_address": "г. Санкт-Петербург, Невский пр., д. 15/2, кв. №34",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# 22. Форма отправляется, если все поля формы пустые (позитивная проверка, так как все поля формы необязательные):
# Падает из-за опечатки на странице ("permananet" вместо "permanent")
def test_text_form_sent_if_all_fields_empty(text_box_page):
    data = {
        "name": "",
        "email": "",
        "current_address": "",
        "permanent_address": "",
    }

    text_box_page.submit_filled_form(**data)
    assert_result_contains(text_box_page, **data)


# =========================
# НЕГАТИВНЫЕ ТЕСТЫ
# =========================


# 1. Невалидные значения Email:
@pytest.mark.parametrize("invalid_email", [
    "petrovexample.com",
    "петров@example.com",
    "petrov@@example.com",
    "petrov[]@example.com",
    "petrov @example.com",
])
def test_invalid_email(text_box_page, invalid_email):
    text_box_page.fill_text_form(
        name="Петр Петров",
        email=invalid_email,
        current_address="Москва",
        permanent_address="Санкт-Петербург",
    )
    text_box_page.submit_without_wait()

    assert text_box_page.get_email_validation_message() != ""


# 2. HTML-иньекция (тест падает, так как html выполняется):
def test_html_injection(text_box_page):
    payload = "<div id='hack'>Hello</div>"

    text_box_page.submit_text_form_with_name_payload(payload)

    html_elements = text_box_page.driver.find_elements(By.ID, "hack")

    assert len(html_elements) == 0


# 3. XSS-иньекция:
def test_xss_injection(text_box_page):
    payload = "<script>alert(1)</script>"

    text_box_page.submit_text_form_with_name_payload(payload)

    with pytest.raises(TimeoutException):
        WebDriverWait(text_box_page.driver, 1).until(EC.alert_is_present())
