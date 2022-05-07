#Packages
from datetime import datetime
import json
import pandas as pd
from sqlalchemy import create_engine
from decouple import config

#Functions
import data_load
import property_details
import main_scraper
import main_cleaner

#Env vars
USERNAME = config('USER')
PASS = config('PASS')
HOST = config("HOST")
PORT = config("PORT")

def create_sql_table(data, data_name, sql_command):

    try:
        print("Appending to {} dataset".format(data_name))
        engine = create_engine('postgresql://{}:{}@{}:{}/retail_data'.format(USERNAME,PASS,HOST,PORT))

        if sqlalchemy.inspect(engine).has_table("{}".format(data_name)) == False:
            engine.execute(sql_command)

        keys = engine.execute('SELECT DISTINCT(id) FROM {};'.format(data_name))
        key_list = []

        for key in keys:
            key_list.append(key[0])

        data_to_update = data[data["id"].isin(key_list)]
        data_to_add = data[~data["id"].isin(key_list)]

        return (data_to_update.to_sql(name=data_name, con=engine, if_exists="replace", index=False),
                data_to_add.to_sql(name=data_name, con=engine, if_exists="append", index=False))

    except: #sql error cannot be recognized, so using all exception
        print("Database cannot connect to SQL server, creating {} database localy".format(data_name))
        return data.to_csv("{}{}.csv".format(data_name, str(datetime.today().date())), index = False)

commands = json.load(open('sql_commands.json', encoding='utf-8'))
colnames = json.load(open('data_colnames.json', encoding='utf-8'))

input_data = main_scraper.MainScraper()

create_sql_table(main_cleaner.MainCleaner(pd.json_normalize(input_data["lakas"]), "flat", colnames["colnames_flat"]), "lakas", commands["command_flat"])
create_sql_table(main_cleaner.MainCleaner(pd.json_normalize(input_data["haz"]), "house", colnames["colnames_house"]), "haz", commands["command_house"])
create_sql_table(main_cleaner.MainCleaner(pd.json_normalize(input_data["telek"]), "plot", colnames["colnames_plot"]), "telek", commands["command_plot"])

if __name__ == "__main__":
    create_sql_table()

