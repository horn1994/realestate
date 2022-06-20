import pandas as pd
import numpy as np

def prefilt(colname, data = lakas):
    
    if data[colname].isnull().mean() > 0.65:
        data.drop(columns = colname, inplace = True)
    
    return data

def outliers(colname):
    
    data = prefilt(colname, data = lakas)
    
    #Censoring non-binary float/int type columns (top 0.001%)
    if data[colname].dtype in ["float64", "int64"]:
        if ((colname not in ["id", "room_count"]) 
           & (data[colname].std() > 1)):
        
            data[colname] = np.where(data[colname] > data[colname].describe(percentiles = [.999])[-2],
                                    data[colname].describe(percentiles = [.999])[-2],
                                    data[colname])
        
        #Censoring room count (due to half-rooms there is some error in the scraping, so have to censor top 2%)
        elif colname == "room_count":
            data[colname] = np.where(data[colname] > data[colname].describe(percentiles = [.98])[-2],
                                    data[colname].describe(percentiles = [.98])[-2],
                                    data[colname])        
    return data

def impute_missing(colname):
    
    data = outliers(colname)
    
    #Non-binary, numeric values (prices, sizes)
    if data[colname].dtype in ["float64", "int64"]:
        if ((colname != "id") 
           & (data[colname].std() > 1)):
            
            

            data[colname] = np.where(data[colname].isna(), 
                                 data[~data[colname].isna()][colname].median(),
                                 data[colname])
    
    #Binary, numeric values (dummy vars)
    #Here I assume that (for not largly missing predictors) if the info is not given it is not av, hence 0
        elif ((colname != "id")
           & (data[colname].std() <= 1)):

            data[colname] = np.where(data[colname].isna(),
                                     0,
                                     data[colname])

    #Impute every object predictor with a "Missing category"
    elif data[colname].dtype == 'O':
        
        data[colname].fillna(value="Missing", inplace = True)
        
    return data

def normalizer(colname):
    
    data = impute_missing(colname)
    
    if data[colname].dtype in ["float64", "int64"]:
        if ((colname != "id") 
           & (data[colname].std() > 1)):
            
            data[str(colname) + "_norm"] = ((data[colname] - data[colname].min())/
                                            (data[colname].max() - data[colname].min()))
            if "price" not in str(colname):
                data.drop(columns = [str(colname)], inplace = True)
    return data

def one_hot_encode(colname):
    
    data = normalizer(colname)
    
    if data[colname].dtype == 'O':
        
        data = (data
                .drop(columns = colname)
                .merge(
                    pd.get_dummies(data[colname], prefix=colname), 
                    right_index = True, 
                    left_index = True))
    return data