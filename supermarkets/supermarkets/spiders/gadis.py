# import json

import scrapy
# from webdriver_manager.chrome import ChromeDriverManager
from scrapy import signals
# from scrapy.utils.project import get_project_settings
from selenium.common.exceptions import (ElementNotInteractableException,
                                        ElementNotVisibleException)
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from supermarkets.items.Supermarkets import SupermarketsItem


class GadisSpider(scrapy.Spider):
    name = 'gadis'
    handle_httpstatus_list = [500, 502, 503,
                              504, 408, 403, 401, 400, 404, 408, 302]

    # allowed_domains = ['www.gadisline.com']
    # start_urls = ['http://example.com/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed_urls = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GadisSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(
            spider.handle_spider_closed, signals.spider_closed)
        return spider

    def start_requests(self):
        try:
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

            driver = Chrome(
                executable_path='/Users/hamiltonmercadocuellar/Documents/Desarollo/my-projects/python/scrappy/driver/mac/chromedriver', options=options)
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
            # cookies = driver.get_cookies()

            # with open('cookietest.json', 'w', newline='') as outputdata:
            #     json.dump(cookies, outputdata)

            for category in category_elements[0:1]:
                href = category.get_attribute('href')
                if(href):
                    yield scrapy.Request(href, callback=self.parse)

        finally:
            driver.quit()

    def parse(self, response):
        if response.status != 200 or len(response.headers) == 0:
            self.crawler.stats.inc_value('failed_url_count')
            self.failed_urls.append(response.url)
            print("===============PARSE != 200=================")
            print(response.url)
            print("================================")
        else:
            print("===============PARSE=================")
            print(response.headers)
            print("================================")
            item = SupermarketsItem()
            xpath_list_products = "//div[@class='product_container']"
            list_products = response.xpath(xpath_list_products)
            for product in list_products:
                item.descripcion = product.xpath(
                    './/p[@class="product_description"]/a/text()').extract_first()
                yield item

    def handle_spider_closed(self, reason):
        self.crawler.stats.set_value(
            'failed_urls', self.failed_urls)

    def process_exception(self, response, exception, spider):
        ex_class = "%s.%s" % (exception.__class__.__module__,
                              exception.__class__.__name__)
        self.crawler.stats.inc_value(
            'downloader/exception_count', spider=spider)
        self.crawler.stats.inc_value(
            'downloader/exception_type_count/%s' % ex_class, spider=spider)
