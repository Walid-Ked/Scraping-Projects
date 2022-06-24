import scrapy
import json

from upshelf.items import UpshelfItem
from scrapy.loader import ItemLoader

class targetspider(scrapy.Spider):
    name = "target"
    
    def start_requests(self):
        
        # The API used by the website to fetch the product information
        api = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin=84616123&store_id=2184&pricing_store_id=2184'
        
        self.headers = {
            "accept": "application/json",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/97.0.4692.71 Safari/537.36",
            "referer": "https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109" 
            }
        yield scrapy.Request(api, headers=self.headers, callback=self.parse)
    
    def parse(self, response):
        
        # Using an itemloader to load the items
        l = ItemLoader(item=UpshelfItem())
        
        # Getting the response from the API request in a json format
        json_response = response.json()

        # There are multiple variants for this product under the "children" node, we can extract all of them, or we can just take 
        # one of them for demonstration purposes. 
        variation = json_response['data']['product']['children'][6]

        # Extracting the necessary fields and adding them to the loader
        l.add_value("description",variation['item']['product_description']['downstream_description'])        
        l.add_value("specifications",variation['item']['product_description']['bullet_descriptions'])        
        l.add_value("highlights",variation['item']['product_description']['soft_bullets']['bullets'])
        l.add_value("images",[json_response['data']['product']['item']['enrichment']['images']['primary_image_url']] + json_response['data']['product']['item']['enrichment']['images']['alternate_image_urls'])
        l.add_value("title",variation['item']['product_description']['title'])
        l.add_value("price",variation['price']['current_retail'])

        # The questions API used by the website to fetch the product's related questions and answers.
        questions_api = 'https://r2d2.target.com/ggc/Q&A/v1/question-answer?type=product&questionedId=84616123&page=0&size=100&sortBy=MOST_ANSWERS&key=9f36aeafbe60771e321a7cc95a78140772ab3e96&errorTag=drax_domain_questions_api_error'
        yield scrapy.Request(questions_api, headers=self.headers, callback=self.parse_questions, meta = {'loader':l})

    
    def parse_questions(self, response):

        # Getting the loader passed in the meta dictionary     
        loader = response.meta['loader']

        # A list to store the questions and their answers
        questions_list = []

        json_response = response.json()
        for r in json_response['results']:
            question = {}
            question['question'] = r['text']
            question['answers'] = [x['text'] for x in r['answers']]
            questions_list.append(question)

        # Adding the list of questions and answers to the loader and yielding
        loader.add_value("questions" ,questions_list)
        yield loader.load_item()
        
