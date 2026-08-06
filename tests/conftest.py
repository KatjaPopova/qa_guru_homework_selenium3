import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.table_element import TableElement


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


# Фикстура для страницы логина
@pytest.fixture()
def login_page(driver):
    driver.get("https://qa-guru.github.io/one-page-form/login.html")
    return driver


# Фикстура для Text Box страницы
@pytest.fixture()
def text_box_page(driver):
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    return driver


# Фикстура для страницы Data Tables
@pytest.fixture()
def tables_page(driver):
    driver.get("https://the-internet.herokuapp.com/tables")
    return driver


# Фикстура для Таблицы 1
@pytest.fixture
def table1(tables_page):
    return TableElement(tables_page, (By.ID, "table1"))


# Фикстура для Таблицы 2
@pytest.fixture
def table2(tables_page):
    return TableElement(tables_page, (By.ID, "table2"))
