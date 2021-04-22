import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import random
from UAStrings import uastrings as uas
from datetime import date, time, timedelta
import logging

class AmazonProductScraper():
    
    def __init__(self):
        ''' Initialize scraper '''
        self.uas = uas
    
    def rotate_UA(self):
        ''' rotation of UA to by-pass crawl error '''
        return random.choice(self.uas)


    def parse_url(self, url):

        headers = {'User-Agent': self.rotate_UA()}
        content = None

        try:
            response = requests.get(url, headers=headers)
            ct = response.headers['Content-Type'].lower().strip()

            if 'text/html' in ct:
                content = response.content
                # soup = BeautifulSoup(content, "lxml")
                soup = BeautifulSoup(content, "html.parser")
            else:
                print("Else here")
                content = response.content
                soup = None
        except Exception as e:
            print("Parsing error:", str(e))
        
        return content, soup, ct


    def get_data(self):

        content, soup, ct = self.parse_url('https://www.amazon.com.au/gp/bestsellers/lighting/ref=zg_bs_nav_0')
        product_list, prod_name_l, prod_price_l, prod_rating_l, prod_rcount_l = [], [], [], [], []

        try:
            # dissect soup
            for item in soup.find_all("div", {"class": "a-section a-spacing-none aok-relative"}):

                item_rating = self.get_product_rating(item)
                item_name = self.get_product_name(item)
                item_review_cnt = self.get_review_cnt(item)
                # item_asin = self.get_product_asin(item)
                item_price = self.get_product_price(item)

                product = {
                    'Item Name' : item_name,
                    'Price' : item_price,
                    'Rating' : item_rating,
                    'Review Count' : item_review_cnt,
                    # 'ASIN' : item_asin
                }

                product_list.append(product)

            print("Product list:", product_list)

            for p in product_list:
                p_name = p['Item Name']
                p_price = p['Price']
                p_rating = p['Rating']
                p_rcount = p['Review Count']

                prod_name_l.append(p_name)
                prod_price_l.append(p_price)
                prod_rating_l.append(p_rating)
                prod_rcount_l.append(p_rcount)

            #generating CSV
            product_dict = {'Item Name': prod_name_l,
                            'Price': prod_price_l,
                            'Rating': prod_rating_l,
                            'Review Count': prod_rcount_l
                            }

            df = pd.DataFrame(product_dict) 
        
            # saving the dataframe 
            df.to_csv('sample_product_{}-{}.csv'.format(str(date.today()),str(random.randrange(0,9999))))
            print("Done saving csv")

        except Exception as e:
            print("Soup error:", str(e))
            return False

    def get_product_name(self, soup_src):
        try:
            # class name is dynamic and rotating, using attributes to get data
            item_name = soup_src.find("div", {"aria-hidden" : "true"}).text.strip()
                    
        except Exception as e:
            item_name = "N/A"

        return item_name


    def get_product_rating(self, soup_src):
        try:
            item_rating = soup_src.find("span", {"class" : "a-icon-alt"}).text.strip()
        except Exception as e:
            item_rating = "N/A"

        return item_rating


    def get_review_cnt(self, soup_src):
        try:
            item_review_cnt = soup_src.find("a", {"class" : "a-size-small a-link-normal"}).text.strip()
        except Exception as e:
            item_review_cnt = "N/A"

        return item_review_cnt


    def get_product_asin(self, soup_src):
        try:
            item_asin = soup_src.find('a', href = re.compile(r'product'))
        except Exception as e:
            item_asin = "N/A"

        return item_asin


    def get_product_price(self, soup_src):
        try:
            item_price = soup_src.find("span", {"class" : "p13n-sc-price"}).text.strip()
        except Exception as e:
            item_price = "N/A"

        return item_price
