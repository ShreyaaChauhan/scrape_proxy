import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.response import open_in_browser


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/js/"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": False},
    }

    def start_requests(self):
        yield scrapy.Request(
            url="http://quotes.toscrape.com/js/",
            meta={"playwright": True},
        )

    def parse(self, response):
        for q in response.css(".quote"):
            yield {
                "author": q.css(".author ::text").get(),
                "quote": q.css(".text ::text").get(),
            }


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
