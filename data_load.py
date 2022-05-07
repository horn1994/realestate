import json

def InputData():
    try:
        # Additional scraping instances
        input_data = json.load(open("data.json", encoding='utf-8'))
    except FileNotFoundError:
        # First scraping
        input_data= {"lakas": [],
                   "haz": [],
                   "telek": []}
    return input_data