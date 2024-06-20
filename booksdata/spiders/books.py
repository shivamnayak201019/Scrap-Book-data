import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime


client = MongoClient("mongodb+srv://nayakshivam1:Shivam%40mdb1@cluster0.alpwwda.mongodb.net/")
db = client.scrapy
def insertToDb(page,title,rating,image,price,instock):
    collection = db[page]
    doc={"title":title,"rating":rating,"image":image,"price":price,"instock":instock,   
    "date": datetime.datetime.now(tz=datetime.timezone.utc),}
    inserted=collection.insert_one(doc)
    return inserted.inserted_id


class BooksSpider(scrapy.Spider):
    name = "books"
    # allowed_domains = ["toscrape.com"]
    # start_urls = ["https://toscrape.com"]


    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page=response.url.split("/")[-2]
        filename = f"books-{page}.html"
        bookdetail={}
        #save the content as file
        # Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        cards=response.css(".product_pod")
        for card in cards:
            title=card.css("h3>a::text").get()
            
            rating=card.css(".star-rating").attrib["class"].split(" ")[1]
            
            image=card.css(".image_container img")
            image=image.attrib["src"].replace("../../../../media","https://books.toscrape.com/media")
        
            price=card.css(".product_price .price_color::text").get()
            
            availibility=card.css(".instock")
            if (len(availibility))>0:
                instock=True
            else:
                instock=False
            
            insertToDb(page,title,rating,image,price,instock)
        # print(a)
        # b=a.css("a")
        # print(b)
        
