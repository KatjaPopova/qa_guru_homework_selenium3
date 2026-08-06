# =========================
# ТАБЛИЦА №1
# =========================

# ПОЗИТИВНЫЕ ТЕСТЫ:

# 1. Таблица 1 содержит 4 строки данных:
def test_table1_rows_count(table1):
    rows_count = table1.get_rows_count()

    assert rows_count == 4, f"Ожидалось 4 строки, но найдено {rows_count}"


# 2. Таблица 1 содержит 6 колонок:
def test_table1_columns_count(table1):
    columns_count = table1.get_columns_count()

    assert columns_count == 6, f"Ожидалось 6 столбцов, но найдено {columns_count}"


# 3. Строка 3 таблицы 1 соответствует ожидаемым данным:
def test_get_third_row_data_table1(table1):
    third_row = table1.get_row_data(2)

    expected_row = [
        "Doe",
        "Jason",
        "jdoe@hotmail.com",
        "$100.00",
        "http://www.jdoe.com",
        "edit delete"
    ]

    assert third_row == expected_row, \
        f"Ожидалась строка {expected_row}, но получено {third_row}"


# 4. Заголовки таблицы 1 соответствуют ожидаемым:
def test_get_correct_headers_table1(table1):
    correct_headers = table1.get_headers()

    expected_headers = [
        "Last Name",
        "First Name",
        "Email",
        "Due",
        "Web Site",
        "Action"
    ]

    assert correct_headers == expected_headers, \
        f"Ожидалась строка {expected_headers}, но получено {correct_headers}"


# 5. Корректное получение email из таблицы 1:
def test_get_cell_value_email_column_table1(table1):
    cell_value = table1.get_cell_value(1, 2)

    assert cell_value == "fbach@yahoo.com", \
        f"Ожидалась 'fbach@yahoo.com', но получено {cell_value}"


# 6. В таблице 1 существует пользователь с задолженностью $50.00:
def test_user_with_due_exist_table1(table1):
    assert table1.user_with_due_exists("$50.00")


# 7. Таблица 1 отображается на странице:
def test_table_is_displayed_table1(table1):
    assert table1.is_displayed()


# 7. Каждая строка таблицы 1 содержит кнопки Edit и Delete:
def test_all_rows_have_edit_and_delete_buttons_table1(table1):
    assert table1.all_rows_have_buttons_edit_and_delete()


# 8. Все email в таблице 1 содержат символ "@":
def test_all_emails_contain_mail_symbol_table1(table1):
    emails = table1.get_all_emails()

    assert all("@" in email for email in emails)


# 9. Пользователь Bach присутствует в таблице 1:
def test_user_bach_exists_table1(table1):
    assert table1.user_exists("Bach"), "Пользователь не найден"


# НЕГАТИВНЫЕ ТЕСТЫ:
# 1. Несуществующая строка:
def test_get_row_data_invalid_index_table1(table1):
    try:
        table1.get_row_data(10)  # строки с таким индексом нет
        assert False, "Ожидалась ошибка IndexError"
    except IndexError:
        pass  # тест пройден


# 2. Несуществующая ячейка:
def test_get_cell_value_invalid_column_table1(table1):
    try:
        table1.get_cell_value(0, 10)  # колонки с таким индексом нет
        assert False, "Ожидалась ошибка IndexError"
    except IndexError:
        pass  # тест пройден


# 3. Несуществующий пользователь:
def test_user_unknown_not_exists_table1(table1):
    assert not table1.user_exists("Peterson"), \
        "Пользователь не должен существовать"


# 4. Несуществующее значение долга:
def test_user_with_wrong_due_not_exists_table1(table1):
    assert not table1.user_with_due_exists("$10000"), \
        "Пользователь с такой суммой не должен существовать"


# 5. Пустая строка Last Name:
def test_user_exists_empty_field_table1(table1):
    assert not table1.user_exists(""), \
        "Пустая фамилия не должна существовать"


# 6. Таблица не найдена:
def test_table_wrong_locator_table1(table1):
    try:
        table1.element()
        assert False, "Ожидалась ошибка NoSuchElementException"
    except Exception:
        pass


# 7. Пустые значения Email:
def test_no_empty_emails_table1(table1):
    emails = table1.get_all_emails()

    for email in emails:
        assert email != "", "Найден пустой email"


# =========================
# ТАБЛИЦА №2
# =========================

# ПОЗИТИВНЫЕ ТЕСТЫ:
# 1. Получение email из 1 строки, 3 колонки таблицы 2
def test_get_cell_value_email_column_table2(table2):
    cell_value = table2.get_cell_value(0, 2)

    assert cell_value == "jsmith@gmail.com", \
        f"Ожидалась 'jsmith@gmail.com', но получено {cell_value}"


# 2. Пользователь Conway присутствует в таблице 2
def test_user_conway_exists_table2(table2):
    assert table2.user_exists("Conway"), "Пользователь не найден"


# 3. В таблице 2 есть пользователь с задолженностью $100.00
def test_user_with_due_exist_table2(table2):
    assert table2.user_with_due_exists("$100.00")


# НЕГАТИВНЫЕ ТЕСТЫ:
# 1. Пользователь с несуществующей задолженностью отсутствует в таблице 2:
def test_user_with_wrong_due_not_exists_table2(table2):
    assert not table2.user_with_due_exists("$700"), \
        "Пользователь с такой суммой не должен существовать"


# 2. Несуществующий пользователь отсутствует в таблице 2:
def test_user_unknown_not_exists_table2(table2):
    assert not table2.user_exists("Johnson"), \
        "Пользователь не должен существовать"


# =========================
# ТАБЛИЦЫ №1 и №2
# =========================

# ПОЗИТИВНЫЕ ТЕСТЫ:
# 1. Обе таблицы отображаются на странице:
def test_both_tables_are_displayed(table1, table2):
    assert table1.is_displayed()
    assert table2.is_displayed()


# 2. Обе таблицы содержат 4 строки данных:
def test_both_tables_have_4_rows(table1, table2):
    tables = [table1, table2]

    for table in tables:
        assert table.get_rows_count() == 4


# 3. Обе таблицы содержат 6 колонок:
def test_both_tables_have_6_columns(table1, table2):
    tables = [table1, table2]

    for table in tables:
        assert table.get_columns_count() == 6


# 4. Заголовки обеих таблиц совпадают:
def test_tables_have_same_headers(table1, table2):
    assert table1.get_headers() == table2.get_headers()


# НЕГАТИВНЫЕ ТЕСТЫ:
# 1. Обращение к несуществующей строке вызывает ошибку IndexError:
def test_wrong_row_number(table1, table2):
    tables = [table1, table2]

    for table in tables:
        try:
            table.get_cell_value(10, 1)
            assert False, "Ожидалась ошибка IndexError"
        except IndexError:
            pass


# 2. Обращение к несуществующей колонке вызывает ошибку IndexError:
def test_wrong_column_number(table1, table2):
    tables = [table1, table2]

    for table in tables:
        try:
            table.get_cell_value(1, 10)
            assert False, "Ожидалась ошибка IndexError"
        except IndexError:
            pass
