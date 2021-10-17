import json

import scrapy
from scrapy.utils.project import get_project_settings
from selenium.common.exceptions import (ElementNotInteractableException,
                                        ElementNotVisibleException)
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from supermarkets.items import SupermarketsItem

# from webdriver_manager.chrome import ChromeDriverManager


class GadisSpider(scrapy.Spider):
    name = 'gadis'
    # allowed_domains = ['www.gadisline.com']
    # start_urls = ['http://example.com/']

    def start_requests(self):
        try:
            settings = get_project_settings()
            driver_path = settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')
            options = ChromeOptions()
            options.page_load_strategy = 'normal'
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
            options.add_argument(
                "user-agent=%s" % "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")

            driver = Chrome(executable_path=driver_path, options=options)
            driver.delete_all_cookies()
            # Prevent Selenium Detection
            driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            link = 'https://www.gadisline.com/'

            driver.get(link)

            postal_code = '15001'

            xpath_postal_code = "//select[@id='cl_postal_code']"
            xpath_button_code = "//button[@tabindex='6']"
            xpath_category_links = "//div[@class='container']//a[@role='menuitem'][contains(@href, '://')]"
            xpath_button_cookies = "//a[contains(@class, 'is-primary')]"

            wait = WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[
                ElementNotVisibleException, ElementNotInteractableException])

            select_postal_code = driver.find_element_by_xpath(
                xpath_postal_code)
            Select(select_postal_code).select_by_visible_text(postal_code)

            driver.find_element_by_xpath(xpath_button_code).click()

            """ FluentWait """

            wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath_button_cookies))).click()

            category_elements = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, xpath_category_links)))
            cookies = driver.get_cookies()

            with open('cookietest.json', 'w', newline='') as outputdata:
                json.dump(cookies, outputdata)

            for category in category_elements[0:1]:
                href = category.get_attribute('href')
                if(href):
                    yield scrapy.Request(href)

        finally:
            driver.quit()

    def parse(self, response):
        print("===============PARSE=================")
        print(response.headers.getlist('Set-Cookie'))
        print("================================")
        item = SupermarketsItem()
        xpath_list_products = "//div[@class='product_container']"
        list_products = response.xpath(xpath_list_products)
        for product in list_products:
            item.descripcion = product.xpath(
                './/p[@class="product_description"]/a/text()').extract_first()
            yield item
