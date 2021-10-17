import json

from selenium.common.exceptions import (ElementNotInteractableException,
                                        ElementNotVisibleException)
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

try:
    path_driver = "./driver/mac/chromedriver"

    options = ChromeOptions()
    options.add_argument('--headless=true')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920x1080')
    # Prevent Selenium Detection
    options.add_argument(
        '--disable-blink-features=AutomationControlled')
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    options.add_experimental_option(
        'useAutomationExtension', False)
    options.page_load_strategy = 'normal'
    driver = Chrome(path_driver, options=options)

    link = 'https://www.gadisline.com/'

    driver.get(link)
    driver.delete_all_cookies()

    postal_code = '15001'
    xpath_postal_code = "//select[@id='cl_postal_code']"
    xpath_button_code = "//button[@tabindex='6']"
    xpath_category_links = "//div[@class='container']//a[@role='menuitem'][contains(@href, '://')]"
    xpath_button_cookies = "//a[contains(@class, 'is-primary')]"

    """ FluentWait """
    wait = WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[
        ElementNotVisibleException, ElementNotInteractableException])

    select_postal_code = driver.find_element_by_xpath(xpath_postal_code)
    Select(select_postal_code).select_by_visible_text(postal_code)
    driver.find_element_by_xpath(xpath_button_code).click()

    # for request in driver.requests:
    #     if request.response:
    #         print(
    #             request.url,
    #             request.response.status_code,
    #             request.response.headers['Content-Type']
    #         )

    # cookies = driver.get_cookies()

    wait.until(
        EC.element_to_be_clickable((By.XPATH, xpath_button_cookies))).click()

    category_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, xpath_category_links)))

    category_links = []
    cookies = driver.get_cookies()

    with open('cookietest.json', 'w', newline='') as outputdata:
        json.dump(cookies, outputdata)

    print("----------------------------")
    print(cookies)
    print("----------------------------")
    for category in category_elements:
        href = category.get_attribute('href')
        if(href):
            category_links.append(href)
finally:
    driver.quit()
