from fake_useragent import UserAgent
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
import time
import json

def process_address(data):
    
    try:
        
        sample = json.load(open("address_cache.json", encoding='utf-8'))
        
    except FileNotFoundError:
        
        sample = []
    
    data = data.iloc[len(sample):]
    
    for i,r in data.iterrows():
        
        ua = UserAgent()
        locator = Nominatim(user_agent=ua.random)
        location_full = locator.geocode(r["address"], timeout = 10)

        obs = {}
        obs["id"] = r["id"]
        obs["address"] = r["address"]
        
        try:
            location_point = location_full.point
            #obs["location_full"] = location_full
            obs["address_latitude"] = location_point[0]
            obs["address_longitude"] = location_point[1]
            obs["address_altitude"] = location_point[2]
            
        except: #AttributeError is not sufficient, some errors may not be caught
            #obs["location_full"] = np.nan
            obs["address_latitude"] = np.nan
            obs["address_longitude"] = np.nan
            obs["address_altitude"] = np.nan

        sample.append(obs)
        time.sleep(1)

        if 1000 % len(sample):
            with open('address_cache.json', 'w', encoding='utf-8') as f:
                json.dump(sample, f, ensure_ascii= False)

    return sample