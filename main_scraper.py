#Packages
from bs4 import BeautifulSoup
from requests import get
import re
from datetime import datetime
import json
from random import randint
from time import sleep
import numpy as np

#Functions
import data_load
import property_details

def MainScraper():
    
    input_data = data_load.InputData()
    
    headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    
    #Basic parameters
    flat_params = ["price", "price--sqm", "listing__address", "listing__data--area-size",
                       "listing__data--room-count", "listing__data--balcony-count"]
    
    house_params = ["price", "price--sqm", "listing__address", "listing__data--area-size",
                    "listing__data--plot-size","listing__data--room-count"]
    
    plot_params = ["price", "price--sqm", "listing__address", "listing__data--plot-size"]
    
    all_params = [flat_params, house_params, plot_params]
    
    obj_types = ['lakas', 'haz', 'telek']
    
    for obj_type, param_types in zip(obj_types,all_params): 
        
        url_fix = "https://ingatlan.com/lista/elado+{}?page={}".format(obj_type,{})
        
        page_count = int(re.findall(
                r'\d+', 
                BeautifulSoup(
                    get(
                        "https://ingatlan.com/lista/elado+{}".format(obj_type), 
                        headers=headers).text,'html.parser')
                .find_all(
                    'div', 
                    class_="pagination__page-number")[0]
                .text
                .replace(' ', 
                         ''))[1])
        try:
            ids = [val['id'] for val in input_data[obj_type]]
                    
        except KeyError: #"Initial scrape, no IDs"
            ids = []

        for page in range(page_count):

            url = url_fix.format(page+1)
            response = get(url, headers=headers)
            html_soup = BeautifulSoup(response.text, 
                                      'html.parser')

            for obs in range(len(html_soup.find_all('a', class_="listing__link js-listing-active-area"))):

                source_url = html_soup.find_all(
                    'a', 
                    class_="listing__link js-listing-active-area", 
                    href= True)[obs]['href']

                id_ = int(source_url.split("/")[-1])
                
                if (id_ not in ids) & (len(str(id_)) == 8):

                    input_data[obj_type].append({})
                    
                    input_data[obj_type][-1]["id"] = id_

                    input_data[obj_type][-1]["source_url"] = (
                        "https://ingatlan.com" + source_url)

                    input_data[obj_type][-1]["timestamp"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    

                    for param in param_types:

                        try:
                            input_data[obj_type][-1][param] = html_soup.find_all(
                                'div', 
                                class_=param)[obs].text

                        except IndexError: #parameter not av for obs

                             input_data[obj_type][-1][param] = "nincs megadva"

                    input_data[obj_type][-1].update(
                            property_details.PorpertyDetails(
                            input_data[obj_type][-1]["source_url"], headers))

                    input_data[obj_type][-1]["aprox_listing_uptime"] = np.nan

                    #t.sleep(random.uniform(1,3))

                elif (id_ in ids):
                    '''
                    Uptime is an estimation based on the first scrape date and the new scrape date
                    So if the link is removed the last aprox_listing_uptime will be the last update
                    If it is first scraped the aprox_listing_uptime is nan
                    '''
                    for i, flat in enumerate(input_data[obj_type]):
                        if flat["id"] == id_:
                            now = datetime.now()
                            first_timestamp = datetime.strptime(
                                input_data[obj_type][i]["timestamp"],
                                '%m/%d/%Y, %H:%M:%S')
                            input_data[obj_type][i]["aprox_listing_uptime"] = (now - first_timestamp).days
            print(page)

            sleep(randint(2,4))
                    
        print(str(obj_type) + ' is done')

        with open('data.json', 'w', encoding='utf-8') as fp:
            json.dump(input_data, fp, ensure_ascii= False)
        
    return input_data

# output_data = MainScraper()

# with open('data.json', 'w', encoding='utf-8') as fp:
#     json.dump(output_data, fp, ensure_ascii= False)