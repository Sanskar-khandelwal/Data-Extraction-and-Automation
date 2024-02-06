import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
from selenium.webdriver.common.keys import Keys


class DealsSpider(scrapy.Spider):
    name = "deals"

    def start_requests(self):
        yield SeleniumRequest(url="https://slickdeals.net/computer-deals/", wait_time=3,
                              callback=self.parse, screenshot=True)

    def parse(self, response):
        # img = response.request.meta['screenshot']
        # with open("screenshot.png", 'wb') as f:
        #     f.write(img)
        driver = response.meta['driver']
        input_form = driver.find_element("xpath", "//input[2]")
        input_form.send_keys("My User Agent")
        input_form.send_keys(Keys.ENTER)
        driver.save_screenshot("latest.png")
