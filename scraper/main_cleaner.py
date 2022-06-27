import json
import pandas as pd
import numpy as np
import re

def MainCleaner(data, data_name, colnames):
    
    #Rename cols
    data.columns = colnames
    
    #Replace missing with nan
    data.replace(
        ['nincs megadva','nem értékelt'], 
        np.nan,
        regex = True,
        inplace = True)
    
    #gen binary
    data.replace({"igen": 1, "van": 1, "részt vett": 1,
                  "nem": 0, "nincs": 0, "nem vett részt": 0},
                 inplace = True)
    
    #gen numeric columns
    numeric_cols = data.loc[:,
                            [True if re.findall(
                                r"price+|size+|count+|sqm+|over+|built_in_area|level_area_indicator|gross_level_area",
                                column) 
                             else False for column in data.columns]].columns
    for i in numeric_cols:
        try:
            repl = {"\+ 1 fél": ".5", "m2":""}
            data[i] = data[i].replace(repl, regex = True)
            data[i] = pd.to_numeric(data[i].str.replace(r'[^0-9|.]+', '', regex = True))
            
        except AttributeError:
            continue
    
    return data
