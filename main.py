import scrapy
import json
from itemadapter import ItemAdapter
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess


class QuoteItem(Item):
    quote = Field()
    author = Field()
    tags = Field()


class QuoteAuthor(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class MainPipeline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "fullname" in adapter.keys():
            self.authors.append(adapter.asdict())
        if "tags" in adapter.keys():
            self.quotes.append(adapter.asdict())

    def close_spider(self, spider):
        with open("authors.json", "w", encoding="utf-8") as fd:
            json.dump(self.authors, fd)
        with open("quotes.json", "w", encoding="utf-8") as fd:
            json.dump(self.quotes, fd)


class MainSpider(scrapy.Spider):
    name = "main_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]
    custom_settings = {"ITEM_PIPELINES": {MainPipeline: 300}}

    def parse(self, response, *args):
        for element in response.xpath("/html//div[@class='quote']"):
            quote = element.xpath("span[@class='text']/text()").get().strip()
            author = element.xpath("span/small[@class='author']/text()").get().strip()
            tags = [el.strip() for el in element.xpath("div[@class='tags']/a[@class='tag']/text()").extract()]
            yield QuoteItem(tags=tags, author=author, quote=quote)
            yield response.follow(url=self.start_urls[0] + element.xpath("span/a/@href").get().strip(),
                                  callback=self.parse_author)
            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                yield scrapy.Request(url=self.start_urls[0] + next_link.strip())

    def parse_author(self, response, *args):
        content = response.xpath("//div[@class='author-details']")
        fullname = content.xpath("h3[@class='author-title']/text()").get().strip()
        data_born = content.xpath("p/span[@class='author-born-date']/text()").get().strip()
        location = content.xpath("p/span[@class='author-born-location']/text()").get().strip()
        description = content.xpath("div[@class='author-description']/text()").get().strip()
        yield QuoteAuthor(fullname=fullname, born_date=data_born, born_location=location, description=description)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(MainSpider)
    process.start()
    process.join()
    print("---END---")
