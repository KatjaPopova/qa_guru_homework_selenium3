import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.table_element import TableElement
from pages.tables_page import TablesPage


@pytest.fixture()
def tables_page(driver):
    page = TablesPage(driver)
    page.open()

    page.table1.wait_visible()
    page.table2.wait_visible()

    return page


# =========================
# ТАБЛИЦА №1
# =========================

# ПОЗИТИВНЫЕ ТЕСТЫ:

# 1. Строка 3 таблицы 1 соответствует ожидаемым данным:
def test_get_third_row_data_table1(tables_page):
    third_row = tables_page.table1.get_row_data(2)

    expected_row = [
        "Doe",
        "Jason",
        "jdoe@hotmail.com",
        "$100.00",
        "http://www.jdoe.com",
        "edit delete"
    ]

    assert third_row == expected_row


# 2. Корректное получение email из таблицы 1:
def test_get_cell_value_email_column_table1(tables_page):
    assert tables_page.table1.get_cell_value(1, 2) == "fbach@yahoo.com"


# 3. В таблице 1 существует пользователь с задолженностью $50.00:
def test_user_with_due_exist_table1(tables_page):
    assert tables_page.table1.user_with_due_exists("$50.00")


# 4. Каждая строка таблицы 1 содержит кнопки Edit и Delete:
def test_all_rows_have_edit_and_delete_buttons_table1(tables_page):
    assert tables_page.table1.all_rows_have_buttons_edit_and_delete()


# 5. Все email в таблице 1 содержат символ "@":
def test_all_emails_contain_mail_symbol_table1(tables_page):
    emails = tables_page.table1.get_all_emails()
    assert all("@" in email for email in emails)


# 6. Пользователь Bach присутствует в таблице 1 (Fluent Wait):
def test_fluent_wait_user_bach_exists_table1(tables_page):
    wait = WebDriverWait(
        tables_page.driver,
        timeout=5,
        poll_frequency=0.2,
        ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
    )

    wait.until(EC.text_to_be_present_in_element(tables_page.table1.locator, "Bach"))

    assert tables_page.table1.user_exists("Bach"), "Пользователь не найден"


# НЕГАТИВНЫЕ ТЕСТЫ:
# 1. Несуществующий пользователь:
def test_user_unknown_not_exists_table1(tables_page):
    assert not tables_page.table1.user_exists("Peterson")


# 2. Несуществующее значение долга:
def test_user_with_wrong_due_not_exists_table1(tables_page):
    assert not tables_page.table1.user_with_due_exists("$10000")


# 3. Пустая строка Last Name:
def test_user_exists_empty_field_table1(tables_page):
    assert not tables_page.table1.user_exists("")


# 4. Таблица не найдена:
def test_table_wrong_locator_table1(tables_page):
    wrong_table = TableElement(tables_page.driver, (By.ID, "table999"))
    with pytest.raises(NoSuchElementException):
        _ = wrong_table.element


# 5. Пустые значения Email:
def test_no_empty_emails_table1(tables_page):
    emails = tables_page.table1.get_all_emails()
    for email in emails:
        assert email != "", "Найден пустой email"


# =========================
# ТАБЛИЦА №2
# =========================

# ПОЗИТИВНЫЕ ТЕСТЫ:
# 1. Получение email из 1 строки, 3 колонки таблицы 2
def test_get_cell_value_email_column_table2(tables_page):
    assert tables_page.table2.get_cell_value(0, 2) == "jsmith@gmail.com"


# 2. Пользователь Conway присутствует в таблице 2
def test_user_conway_exists_table2(tables_page):
    assert tables_page.table2.user_exists("Conway")


# 3. В таблице 2 есть пользователь с задолженностью $100.00
def test_user_with_due_exist_table2(tables_page):
    assert tables_page.table2.user_with_due_exists("$100.00")


# НЕГАТИВНЫЕ ТЕСТЫ:
# 1. Пользователь с несуществующей задолженностью отсутствует в таблице 2:
def test_user_with_wrong_due_not_exists_table2(tables_page):
    assert not tables_page.table2.user_with_due_exists("$700")


# 2. Несуществующий пользователь отсутствует в таблице 2:
def test_user_unknown_not_exists_table2(tables_page):
    assert not tables_page.table2.user_exists("Johnson")


# =========================
# ТАБЛИЦЫ №1 и №2
# =========================

# ПОЗИТИВНЫЕ ТЕСТЫ:
# 1. Обе таблицы отображаются на странице:
def test_both_tables_are_displayed(tables_page):
    assert tables_page.table1.is_displayed()
    assert tables_page.table2.is_displayed()


# 2. Обе таблицы содержат 4 строки данных:
def test_both_tables_have_4_rows(tables_page):
    assert tables_page.table1.get_rows_count() == 4
    assert tables_page.table2.get_rows_count() == 4


# 3. Обе таблицы содержат 6 колонок:
def test_both_tables_have_6_columns(tables_page):
    assert tables_page.table1.get_columns_count() == 6
    assert tables_page.table2.get_columns_count() == 6


# 4. Заголовки обеих таблиц совпадают:
def test_tables_have_same_headers(tables_page):
    assert tables_page.table1.get_headers() == tables_page.table2.get_headers()


# НЕГАТИВНЫЕ ТЕСТЫ:
# 1. Обращение к несуществующей строке вызывает ошибку IndexError:
def test_wrong_row_number(tables_page):
    with pytest.raises(IndexError):
        tables_page.table1.get_cell_value(10, 1)

    with pytest.raises(IndexError):
        tables_page.table2.get_cell_value(10, 1)


# 2. Обращение к несуществующей колонке вызывает ошибку IndexError:
def test_wrong_column_number(tables_page):
    with pytest.raises(IndexError):
        tables_page.table1.get_cell_value(1, 10)

    with pytest.raises(IndexError):
        tables_page.table2.get_cell_value(1, 10)
