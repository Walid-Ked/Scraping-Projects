# %%
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import pickle

# %% [markdown]
# ## Getting London Restaurants Details

# %%
class RestaurantsDetails():
    
    def __init__(self, region = "london-restaurant-listings"):
        self.region = region
        self.details_list = []
        
    def get_data(self):
        for i in range(0,901,100):
            url = f"https://www.opentable.co.uk/s/node/api?size=100&from={i}&PageType=2"
            print(i)
            payload={}
            headers = {
              'Connection': 'keep-alive',
              'Content-Length': '0',
              'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
              'DNT': '1',
              'accept-language': 'en-GB',
              'sec-ch-ua-mobile': '?0',
              'ot-originaluri': f'/{self.region}',
              'ot-originalhost': 'www.opentable.co.uk',
              'ot-requestid': '467d7c26-4f5c-4ec6-9f38-55b22c149b55',
              'Accept': 'application/json, text/javascript, */*; q=0.01',
              'ot-anonymousid': '13FCAB79-4414-4262-9E3C-C7923781A007',
              'csrf-token': 'lgVh4YVK-8jGvYre40AcoVcWpiZPR8NBMgNc',
              'X-Requested-With': 'XMLHttpRequest',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
              'ot-domain': 'couk',
              'Origin': 'https://www.opentable.co.uk',
              'Sec-Fetch-Site': 'same-origin',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Dest': 'empty',
              'Referer': 'https://www.opentable.co.uk/london-restaurant-listings?covers=2&currentview=list&datetime=2021-08-03+19%3A00&latitude=51.511465&longitude=-0.136868&metroid=72&size=100&sort=Rating',
              'Cookie': '_csrf=606857d2-3d5c-4852-87c2-8e0faca8438b; otuvid=13FCAB79-4414-4262-9E3C-C7923781A007; spredCKE=redcount=0; lsCKE=cbref=1; _gid=GA1.3.51178568.1627989249; OT-SessionId=1b207ef7-2645-4b14-8a6b-5968d90fe149; ak_bmsc=4E324A9BD4E57AE7DF63388327BB0215~000000000000000000000000000000~YAAQLvMUAlQLRAZ7AQAAPpi4CwzgZkXbWm9t21520a3GGTEC7t4Ew5mwf4NPERZ4dWNIjYg/7Ko98MA+/6cf9LFAygnj8FLGeQypz2RkXM/J8JYFwWsIPuewK+bMaBmxCxoCsIzl/UZNyLLLwzoKZzT/0u7r0iyl76WH2TdZg2ueWZW8JmB6YRnlADPid86MUGWekeb/e2AigKCuvJzSkbXx8bsGlDnCTJp00WqGjyUypaYQiFKmh30NHbPMoemCKfLXOPuo/sMSbfigsTfUBY6S2alJx0L6/J+kuCQxxVZGymYPOOBgo3lCImAxw5BaPMz/uTxs+onjkLeW+Qn6oj5O71ZM3QugceiYz21bcf1cRzsN1f1g2W0hUvdVuaCEjpdGgIMxZAg+KNNT6B8N6LPpPqNcjSUHTzwXEvOV5ARvXsu+yDxRacI4+kQljSq6kIWOwl8owVhL3fHX12ZegmNNbGlmRs4fpfUHVM5GF2/coMEDsD3g; lvCKE=lvmreg=%2C0&histmreg=72%2C0%7C%2C0; ftc=x=2021-08-03T12%3A16%3A46&c=1&pt1=1&pt2=1&er=134610; bm_sv=ADDBFE11E0E2D2F4BC9390148A2078A7~sFeK3wm438D+RoVAbdhSqczFkXDgsa43f1ZA28IZ/l77eYyb6+K7MjtPZ+/vMPgEf/WRCuuBQ+4xEonVoNqmGr9fNFZiLiflpu9A9o3Yf/ySkdXMAt2MtyRvfUzdGs5apJj7F8I6lrTYOx12cr2FBdmxYQUqNXtWtU//wf6Hmf0=; OptanonConsent=isIABGlobal=false&datestamp=Tue+Aug+03+2021+12%3A16%3A56+GMT%2B0100+(GMT%2B01%3A00)&version=6.20.0&hosts=&consentId=e6621830-4b28-49aa-bffd-daeedc660c0f&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A0%2CC0010%3A1&AwaitingReconsent=false; _ga=GA1.3.1321804136.1627475906; OT-Session-Update-Date=1627989596; _ga_Y7868SCB6E=GS1.1.1627989251.3.1.1627989660.0; OT-Session-Update-Date=1627990264; OT-SessionId=1b207ef7-2645-4b14-8a6b-5968d90fe149; bm_sv=ADDBFE11E0E2D2F4BC9390148A2078A7~sFeK3wm438D+RoVAbdhSqczFkXDgsa43f1ZA28IZ/l77eYyb6+K7MjtPZ+/vMPgEf/WRCuuBQ+4xEonVoNqmGr9fNFZiLiflpu9A9o3Yf/zCDdU4u/1PuE/gXMK9nruraumfhD7G58qVSfg3DvYXSdS6dHcTEbRCylmR/3sFOsc='
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            
            for e in response.json()['Results']['Restaurants']:
                address = e["Address"]
                cuisine = e["Cuisine"]
                description = e["Description"]
                id_ = e["Id"]
                location = e["Location"]
                name = e["Name"]
                print(name)
                phone = e["PhoneNumber"]['FormattedNumber']
                rating = e["Reviews"]["Rating"]
                
                new_restaurant = {
                    "address" : address,
                    "cuisine" : cuisine,
                    "description" : description,
                    "id" : id_,
                    "location" : location,
                    "name" : name,
                    "phone" : phone,
                    "rating" : rating
                }
                
                self.details_list.append(new_restaurant)
        
        return self.details_list

# %%
DetailsObject = RestaurantsDetails()
all_details = DetailsObject.get_data()
len(all_details)

# %% [markdown]
# ## Get Restaurants Reviews

# %%
class RestaurantsReviews():
    def __init__(self, ids_list):
        self.all_reviews = []
        self.ids_list = ids_list
        
    def get_data(self):
        for rid in self.ids_list:
            url = f"https://oc-registry.opentable.co.uk/v2/oc-reviews-restaurant-profile-feed/1.1.2483?rid={rid}&culture=en-GB&page=1&pageSize=100&anonymousId=13FCAB79-4414-4262-9E3C-C7923781A007&__ot_conservedHeaders=x2YPvT6POzqVVB9%2B77Ms1PfEj5zyoJ3SrT3%2BPcr%2Fj4Yz2GBDGlBoD7Sj%2F0oV6XaqFfuX7l15I0qKWC1wuXnHNCt2z13Y3xselKqNMj%2FHLK3izADxsSABG1TVQeA9n2FIjrrvfjMbVix8y2OFRqFCU5SrW1yln6f0uzcVpUWMshFqOdLAogiC5gtr%2BCaVnkYmHzHH03mS4Sc%3D&__oc_Retry=0"
            print(f"restaurant id: {rid}")
            payload={}
            headers = {
              'Connection': 'keep-alive',
              'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
              'Accept': 'application/vnd.oc.unrendered+json',
              'DNT': '1',
              'sec-ch-ua-mobile': '?0',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
              'Content-Type': 'text/plain',
              'Origin': 'https://www.opentable.co.uk',
              'Sec-Fetch-Site': 'same-site',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Dest': 'empty',
              'Referer': 'https://www.opentable.co.uk/',
              'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,ar;q=0.6',
              'If-None-Match': '"6e03b-oKXB0nSexpKqeFoXpX9amCzuyA8--gzip"',
              'Cookie': 'OT-Session-Update-Date=1627993858; OT-SessionId=171c4717-a02d-4627-88e3-f1430b124c10; bm_sv=ADDBFE11E0E2D2F4BC9390148A2078A7~sFeK3wm438D+RoVAbdhSqczFkXDgsa43f1ZA28IZ/l77eYyb6+K7MjtPZ+/vMPgEf/WRCuuBQ+4xEonVoNqmGr9fNFZiLiflpu9A9o3Yf/yVP74x3VAabOPBcjoxrQzJkfKZo7xPDNUYc0ZpSX7xxy9TByAF2QsN+lO5+Gbo5ec=; otuvid=54FC2B7D-56B8-4CF7-A9D2-562FE6CC7461'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            response.json()

            num_pages = int(response.json()['data']['paginationData']['totalPages'])+1
            print(f"num_pages = {num_pages}")
            
            for page in range(1,num_pages):
                url = f"https://oc-registry.opentable.co.uk/v2/oc-reviews-restaurant-profile-feed/1.1.2483?rid={rid}&culture=en-GB&page={page}&pageSize=100&anonymousId=13FCAB79-4414-4262-9E3C-C7923781A007&__ot_conservedHeaders=x2YPvT6POzqVVB9%2B77Ms1PfEj5zyoJ3SrT3%2BPcr%2Fj4Yz2GBDGlBoD7Sj%2F0oV6XaqFfuX7l15I0qKWC1wuXnHNCt2z13Y3xselKqNMj%2FHLK3izADxsSABG1TVQeA9n2FIjrrvfjMbVix8y2OFRqFCU5SrW1yln6f0uzcVpUWMshFqOdLAogiC5gtr%2BCaVnkYmHzHH03mS4Sc%3D&__oc_Retry=0"
                response = requests.request("GET", url, headers=headers, data=payload)
                response.json()
                print(f"current page: {page}")
                
                for e in response.json()['data']['reviews'][0:1]:
                    text = e['reviewText']
                    overall_rating = e['rating']['overall']
                    food_rating = e['rating']['food']    
                    ambience_rating = e['rating']['ambience']    
                    service_rating = e['rating']['service']    
                    value_rating = e['rating']['value']    
                    date = e['dateDined']

                    review = {
                        'restaurant_id': rid,
                        "text" : text,
                        "overall_rating" : overall_rating,
                        "food_rating" : food_rating,
                        "ambience_rating" : ambience_rating,
                        "service_rating" : service_rating,
                        "value_rating" : value_rating,
                        "date" : date
                    }

                    self.all_reviews.append(review)
        return self.all_reviews

# %%
rids = [r['id'] for r in all_details]

ReviewsObject = RestaurantsReviews(rids)
ReviewsObject.get_data()

len(ReviewsObject.all_reviews)

# %% [markdown]
# ## Saving Data

# %%
with open('london_restaurants.pickle', 'wb') as f:
    pickle.dump([DetailsObject.details_list, ReviewsObject.all_reviews], f)

# %% [markdown]
# ## Loading Data 

# %%
with open('london_restaurants.pickle', 'rb') as f:
    details, reviews = pickle.load(f)

# %%
df = pd.DataFrame(reviews)
df.to_csv('london_restaurants_reviews.csv')


