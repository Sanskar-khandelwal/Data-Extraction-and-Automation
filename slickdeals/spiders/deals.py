import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
from selenium.webdriver.common.keys import Keys


class DealsSpider(scrapy.Spider):
    name = "deals"
    page_count = 1

    def start_requests(self):
        yield SeleniumRequest(url="https://slickdeals.net/computer-deals/", wait_time=3,
                              callback=self.parse, screenshot=True, headers={
                                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                              })

    # def parse(self, response):
        products = response.xpath(
            "//ul/li[@class = 'bp-p-blueberryDealCard bp-p-blueberryDealCard--priceTitleVariant bp-p-filterGrid_item bp-p-dealCard bp-c-card']/div[1]")
        count = 1

        for product in products:
            yield {
                "product_name": product.xpath(".//a[2]/text()").get(),
                "original_price": product.xpath(".//span[1]/text()").get(),
                "discounted_price": product.xpath(".//span[2]/text()").get(),
                "store": product.xpath("normalize-space(.//span[3]/text())").get(),
                "product_link": product.xpath("normalize-space(.//a[2]/@href)").get()
            }
        count = count + 1
        next_btn = f"https://slickdeals.net/computer-deals/?page={count}"

        if count <= 9:
            yield SeleniumRequest(url=next_btn, callback=self.parse, wait_time=4)

    def parse(self, response):
        products = response.xpath(
            "//ul/li[contains(@class, 'bp-p-blueberryDealCard')]/div[1]")

        for product in products:
            yield {
                "product_name": product.xpath(".//a[2]/text()").get(),
                "original_price": product.xpath(".//span[1]/text()").get(),
                "discounted_price": product.xpath(".//span[2]/text()").get(),
                "store": product.xpath("normalize-space(.//span[3]/text())").get(),
                "product_link": product.xpath(".//a[2]/@href").get()
            }

        self.page_count += 1
        next_btn = f"https://slickdeals.net/computer-deals/?page={self.page_count}"

        if self.page_count <= 9:
            yield SeleniumRequest(url=next_btn, callback=self.parse, wait_time=4)
