from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Инициализация браузера
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # 1. Открытие тестовой страницы
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")

    name = "Иван Иванов"
    email = "ivan@example.com"
    current_address = "ул. Ленина, дом 1"
    permanent_address = "ул. Пушкина, дом 10"

    # 2. Заполнение полей формы
    driver.find_element(By.ID, "userName").send_keys(name)
    driver.find_element(By.ID, "userEmail").send_keys(email)
    driver.find_element(By.ID, "currentAddress").send_keys(current_address)
    driver.find_element(By.ID, "permanentAddress").send_keys(permanent_address)

    # Скролл до кнопки и клик
    submit_button = driver.find_element(By.ID, "submit")
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    submit_button.click()

    # 3. Настройка Fluent Wait
    # timeout: максимальное время ожидания (10 секунд)
    # poll_frequency: интервал опроса страницы (0.5 секунды)
    # ignored_exceptions: список игнорируемых исключений во время опроса
    fluent_wait = WebDriverWait(
        driver,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException]
    )

    # 4. Ожидание появления блока с результатами (id="output")
    output_block = fluent_wait.until(EC.visibility_of_element_located((By.ID, "output")))

    # 5. Проверка результата
    assert name in output_block.text
    assert email in output_block.text
    assert current_address in output_block.text
    assert permanent_address in output_block.text

finally:
    # Закрытие браузера
    driver.quit()
