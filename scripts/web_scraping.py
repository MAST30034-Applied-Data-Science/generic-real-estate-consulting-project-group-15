# built-in imports
import re
import time
import random
from collections import defaultdict
from json import dump
import json
from lxml import etree
import csv
from pprint import pprint
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4051.0 Safari/537.36 Edg/82.0.425.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",

]

# constants
BASE_URL = "https://www.domain.com.au"
N_PAGES = range(1, 51)

headers = {

    'authority': 'www.domain.com.au',

    'sec-ch-ua-platform': '"macOS"',

    'user-agent': random.choice(USER_AGENTS)

}

# begin code
url_links = []
property_metadata = defaultdict(dict)

for number in range(1, 6):
    # generate list of urls to visit
    for page in N_PAGES:
        print('page')
        url = BASE_URL + "/rent/?bedrooms=" + str(number) + f"&state=vic&page={page}"
        print(url)
        bs_object = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")

        # find the unordered list (ul) elements which are the results, then
        # find all href (a) tags that are from the base_url website.
        index_links = bs_object.find("ul", {"data-testid": "results"}).findAll(
            "a", href=re.compile(f"{BASE_URL}/*")  # the `*` denotes wildcard any
        )

        for link in index_links:
            # if its a property address, add it to the list
            if "address" in link["class"]:
                url_links.append(link["href"])

    print('url_links', url_links)

    price_pattern = re.compile(r'\$?((\d+,\d+)|(\d+))')

    for item_url in url_links:
        print('item-url', item_url)

        req = requests.get(item_url, headers=headers)
        response = etree.HTML(req.text)

        #
        address = response.xpath('//h1[@class="css-164r41r"]//text()')[0]
        nums = re.findall(r'\b\d+\b', address)
        postcode = nums[-1] if len(nums) > 0 else 'none'
        print('postcode:', postcode)

        #
        coordinate_href = response.xpath('//a[@class="css-1aszeu9"]/@href')[0]
        nums = re.findall(r'-?\d+.\d+', coordinate_href)
        latitude, longitude = 'none', 'none'
        if len(nums) >= 2:
            latitude = nums[-2]
            longitude = nums[-1]
        print(f'coordinate: longitude={longitude}, latitude={latitude}')

        #
        price_str = ''.join(response.xpath('//div[@class="css-1texeil"]//text()'))
        matched_price = re.search(price_pattern, price_str)
        price = 'N/A'
        if matched_price:
            price = int(re.sub(r'[$,]', '', matched_price.group()))
        print('price', price)

        item_numbers = response.xpath('//div[@class="css-ghc6s4"]/div/span//text()')
        item_list = list(filter(lambda x: len(x.strip()) > 0, item_numbers))
        beds_num = 'N/A' if len(item_list) == 0 or not item_list[0].isdigit() else item_list[0]
        baths_num = 'N/A' if len(item_list) < 3 or not item_list[2].isdigit() else item_list[2]
        parking_num = 'N/A' if len(item_list) < 5 or not item_list[4].isdigit() else item_list[4]
        print(f'item_number beds: {beds_num}, baths: {baths_num}, parking: {parking_num}')

        #
        Description = ''.join(response.xpath('//div[@name="listing-details__description"]/div/div/div/div/p//text()'))
        print('Description', Description)
        #
        domainsys = ''.join(response.xpath('//p[@class="css-jml5ay"]/text()'))
        print('domainsys', domainsys)

        item_json = response.xpath('//script[@id="__NEXT_DATA__"]//text()')
        try:
            item_jsons = json.loads(item_json[0])
            props = item_jsons['props']['pageProps']['componentProps']['schoolCatchment']['schools']
            item_list = []
            for school_item in props:
                school_name = school_item['name']
                year = school_item['year']
                if year == '':
                    year = 'null'

                gender = school_item['gender']
                if gender == '':
                    gender = 'null'

                type = school_item['type']

                item_list.append(school_name + ' | ' + year + ' | ' + gender + ' | ' + type)
            item_lists = ''.join(item_list)
        except:
            item_lists = ''
        print('item_lists', item_lists)

        year_tags = ''.join(response.xpath('//tr[@class="css-1a43shy"]//text()'))
        print('year_tags', year_tags)

        long_term = ''.join(response.xpath('//div[@class="css-ibsnk8"]/text()'))
        print('long_term', long_term)

        residents_ = response.xpath('//div[@class="css-1m57t70"]//div[@class="css-1duxvxh"]/div/@style')

        residents_s = ''.join([i_s.replace('width:', '') + ' | ' for i_s in residents_])
        print('residents_s', residents_s)

        adders = response.xpath('//div[@class="css-mlseai"]//text()')
        adderss = ''.join(([i_adders.strip() for i_adders in adders]))
        print('adders', adderss)

        propertirs_item = response.xpath('//div[@class="css-170a2ks"]//text()')
        propertirs_items = ''.join([i_propertirs_item + ' | ' for i_propertirs_item in propertirs_item])
        print('propertirs_items', propertirs_items)

        ownep_item = response.xpath('//div[@data-testid="location-profile-card__occupancy"]/div/div[1]/div/@style')
        ownep_items = ''.join([i_ownep_item.replace('width:', '') + ' | ' for i_ownep_item in ownep_item])
        print('ownep_items', ownep_items)

        prlces_txt = ''.join(response.xpath('//div[@class="css-1japfew"]/p//text()')).replace('\r', '').replace('\t',
                                                                                                                '').replace(
            '\n', '')

        print('prlces_txt', prlces_txt)

        market_item = response.xpath('//div[@class="css-1y1u6ku"]/div[1]/div/div/div/text()')
        market_items = ''.join([i_market_item + ' ｜ ' for i_market_item in market_item])
        print('market_items', market_items)

        demographics = response.xpath('//div[@class="css-1y1u6ku"]/div[2]/div/div/div/text()')
        demographicss = ''.join([i_demographics + ' ｜ ' for i_demographics in demographics])
        print('demographics', demographicss)

        demographics_owner = response.xpath('//div[@data-testid="suburb-insights__occupancy"]/div/div/div/div/@style')
        demographics_owners = ''.join(
            [i_demographics_owner.replace('width:', '') + ' ｜ ' for i_demographics_owner in demographics_owner])
        print('demographics_owner', demographics_owners)


        with open('webscrap_data.csv', 'a+', encoding='utf-8-sig', newline='') as f:
            f = csv.writer(f)
            f.writerow([item_url] + [postcode] + [longitude] + [latitude] + [price] + [beds_num] + [baths_num] + [
                    parking_num] + [Description] + [domainsys] + [item_lists] + [year_tags] + [long_term] +
                    [residents_s] + [adderss] + [propertirs_items] + [ownep_items] + [prlces_txt] + [market_items] + [demographicss] +
                           [demographics_owners])

    # for each url, scrape some basic metadata
    # for property_url in url_links[1:]:
    #     bs_object = BeautifulSoup(
    #         requests.get(property_url, headers=headers).text, "html.parser"
    #     )
    #
    #     # looks for the header class to get property name
    #     property_metadata[property_url]["name"] = bs_object.find(
    #         "h1", {"class": "css-164r41r"}
    #     ).text
    #
    #     # looks for the div containing a summary title for cost
    #     property_metadata[property_url]["cost_text"] = bs_object.find(
    #         "div", {"data-testid": "listing-details__summary-title"}
    #     ).text
    #
    #     # extract coordinates from the hyperlink provided
    #     # i'll let you figure out what this does :P
    #     property_metadata[property_url]["coordinates"] = [
    #         float(coord)
    #         for coord in re.findall(
    #             r"destination=([-\s,\d\.]+)",  # use regex101.com here if you need to
    #             bs_object.find(
    #                 "a", {"target": "_blank", "rel": "noopener noreferer"}
    #             ).attrs["href"],
    #         )[0].split(",")
    #     ]
    #     print('url, ', url)
    #     property_metadata[property_url]["rooms"] = [
    #         re.findall(r"\d\s[A-Za-z]+", feature.text)[0]
    #         for feature in bs_object.find(
    #             "div", {"data-testid": "property-features"}
    #         ).findAll("span", {"data-testid": "property-features-text-container"})
    #     ]
    #
    #     property_metadata[property_url]["desc"] = re.sub(
    #         r"<br\/>", "\n", str(bs_object.find("p"))
    #     ).strip("</p >")
    #
    #
    #
    # # output to example json in data/raw/
    # with open("../data/raw/example.json", "w") as f:
#       dump(property_metadata, f)


# for each url, scrape some basic metadata
    # for property_url in url_links[1:]:
    #     bs_object = BeautifulSoup(
    #         requests.get(property_url, headers=headers).text, "html.parser"
    #     )
    #
    #     # looks for the header class to get property name
    #     property_metadata[property_url]["name"] = bs_object.find(
    #         "h1", {"class": "css-164r41r"}
    #     ).text
    #
    #     # looks for the div containing a summary title for cost
    #     property_metadata[property_url]["cost_text"] = bs_object.find(
    #         "div", {"data-testid": "listing-details__summary-title"}
    #     ).text
    #
    #     # extract coordinates from the hyperlink provided
    #     # i'll let you figure out what this does :P
    #     property_metadata[property_url]["coordinates"] = [
    #         float(coord)
    #         for coord in re.findall(
    #             r"destination=([-\s,\d\.]+)",  # use regex101.com here if you need to
    #             bs_object.find(
    #                 "a", {"target": "_blank", "rel": "noopener noreferer"}
    #             ).attrs["href"],
    #         )[0].split(",")
    #     ]
    #     print('url, ', url)
    #     property_metadata[property_url]["rooms"] = [
    #         re.findall(r"\d\s[A-Za-z]+", feature.text)[0]
    #         for feature in bs_object.find(
    #             "div", {"data-testid": "property-features"}
    #         ).findAll("span", {"data-testid": "property-features-text-container"})
    #     ]
    #
    #     property_metadata[property_url]["desc"] = re.sub(
    #         r"<br\/>", "\n", str(bs_object.find("p"))
    #     ).strip("</p >")
    #
    #
    #
    # # output to example json in data/raw/
    # with open("../data/raw/example.json", "w") as f:
#       dump(property_metadata, f)


