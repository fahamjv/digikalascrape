from lxml import html
import csv,os,json
import requests
from lxml import etree
from time import sleep
from bs4 import BeautifulSoup
import re

def AmzonParser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)


    while True:
        try:
            doc = html.fromstring(str(page.content, 'utf-8'))
            XPATH_NAME = '//h1[@class="c-product__title"]//text()[not(parent::span)]'
            XPATH_EN_NAME = '//h1[@class="c-product__title"]//span//text()'
            XPATH_SALE_PRICE = '//span[contains(@class,"js-price-value") or contains(@class,"c-price__value js-variant-price")]/text()'
            XPATH_ORIGINAL_PRICE = '//div[@class="c-price__value js-variant-price"]//del//text()'
            XPATH_CATEGORY = '//div[@class="c-product__directory"]//a[@class="btn-link-spoiler"]//text()'
            XPATH_DISCOUNT = '//div[@class="c-price__discount js-price-discount 1"]//text()'
            XPATH_SELLER = '//div[@class="c-product__delivery-seller js-seller-icon"]//ul/li//span[@class="js-seller-text"]//text()'

            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_EN_NAME = doc.xpath(XPATH_EN_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_DISCOUNT = doc.xpath(XPATH_DISCOUNT)
            RAw_SELLER = doc.xpath(XPATH_SELLER)


            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            EN_NAME = ' '.join(''.join(RAW_EN_NAME).split()) if RAW_EN_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            DISCOUNT = ''.join(RAw_DISCOUNT).strip() if RAw_DISCOUNT else None
            SELLER = ''.join(RAw_SELLER).strip() if RAw_SELLER else None
            INFO = BeautifulSoup(page.text,"lxml").body.find('div', attrs={'class':'p-tabs'})

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page.status_code!=200:
                # raise ValueError('captha')
                break

            if(DISCOUNT):
                DISCOUNT = (DISCOUNT.split()[0]+DISCOUNT.split()[1])

            data = {
                    'NAME':NAME,
                    'EN_NAME':EN_NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'DISCOUNT':DISCOUNT,
                    'SELLER':SELLER,
                    'INFO':re.sub('\n','',str(INFO)),
                    'URL':url,
                    }

            return data
        except Exception as e:
            print(e)

def ReadAsin():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))

    AsinList = ['dkp-190163'
        ,'dkp-190161'
        ,'dkp-75689'
        ,'dkp-190162'
        ,'dkp-190163'
        ,'dkp-190164'
        ,'dkp-190175'
        ,'dkp-190166']

    extracted_data = []

    for i in AsinList:
        url = "https://www.digikala.com/product/"+i
        print("Processing: "+url)
        dat = AmzonParser(url)
        if dat:
            extracted_data.append(dat)

    f=open('digikala.json','w')
    json.dump(extracted_data,f,indent=4,ensure_ascii=False)


if __name__ == "__main__":
    ReadAsin()
