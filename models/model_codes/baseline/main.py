import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
from sqlalchemy import create_engine
from decouple import config

#UDFs
from func_handcode import *
from pre_cleaners import *

def raw_data_import(dir_):
    
    #Importing raw data from sql server
    USERNAME = config('USER')
    PASS = config('PASS')
    HOST = config("HOST")
    PORT = config("PORT")

    engine = create_engine(
        'postgresql://{}:{}@{}:{}/retail_data'.format(
            USERNAME,PASS,HOST,PORT))

    data = pd.read_sql_table("lakas",con=engine)
    
    #Importing processed address data from json (for this the process_address.py was used)
    sample = json.load(open(str(dir_) + "address_cache.json", encoding='utf-8'))
    address_data_clean = pd.DataFrame(sample)
    
    #Removing potential duplicate obs.
    address_data_clean = address_data_clean.drop_duplicates(subset = "id")
    data = data.drop_duplicates(subset = "id")
    
    #Merging the two datasets
    data = (data
            .merge(
                address_data_clean
                .drop(
                    columns = ["address", "address_altitude"]), 
                on = "id", 
                how = "inner"))
    
    return data

def pre_cleaner(data):
    
    #Save stringcols for separate dataset
    data_str = data[["id", "address", "source_url","time_stamp", "img_links", "description"]]
    data.drop(columns = ["address", "source_url","time_stamp", "img_links", "description"], inplace = True)

    #Appling cleaners to pre-process data for ML
    for col in data.columns:
        try:
            data = prefilt(data, col)
            data = outliers(data, col)
            data = impute_missing(data, col)
            data = normalizer(data, col)
            data = one_hot_encode(data, col)
        except KeyError:
            continue
            
    return data, data_str


def main_model(data, epoch = 3000):
    
    Ytrain, Ytest, Xtrain, Xtest, D, M, W, b, V, c = gen_input_params(data)
    train_costs = []
    test_costs = []
    for i in range(epoch):

        Ztrain, Yhat_train = forward(Xtrain,W,b,V,c)
        Ztest, Yhat_test = forward(Xtest,W,b,V,c)

        W, b, V, c = update(Xtrain, Ztrain, Ytrain, Yhat_train, W, b, V, c)

        cost_train = get_cost(Ytrain, Yhat_train)
        cost_test = get_cost(Ytest, Yhat_test)

        train_costs.append(cost_train)
        test_costs.append(cost_test)

        if i % 100 == 0:
            print(cost_train,cost_test)

    # plot the costs
    legend1 = plt.plot(train_costs, label='train cost')
    legend2 = plt.plot(test_costs, label='test cost')
    plt.legend()
    plt.show()

    return Ytrain, Yhat_train, train_costs, test_costs
    
if __name__ == "__main__":
    main_model(lakas, epoch = 3000)