import scrapy
from ..items import BookItem

class BookItems(scrapy.Spider):
    name="Books"
    start_urls=['https://books.toscrape.com/']

    def parse(self,response):
        all_books = response.css('article.product_pod')
        # Books=BookItem()

        for book in all_books:
            Books=BookItem()
            bookname=book.css('h3 a::attr(title)').get().strip()
            bookprice = book.css('.price_color::text').extract_first().strip()
            availability = ''.join(book.css('instock.availability::text').extract()).strip()
            rating_class = book.css('p.star-rating::attr(class)').get()
            rating = rating_class.split()[-1] if rating_class else ''

            Books['bookname'] = bookname
            Books['bookprice'] = bookprice
            Books['availability'] = availability
            Books['rating']=rating

            yield Books

        next_page=response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

