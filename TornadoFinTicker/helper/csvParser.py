# -*- coding: utf-8 -*-


### THIS FILE IS UNUSED ####

# used to debug functions and dataframes
import pandas as pd
import pickle,json
import numpy as np

def CSVtoDF(filePath):
    df = pd.read_csv(filePath)
    df = df.drop("Open", 1)
    df = df.drop("High", 1)
    df = df.drop("Low", 1)
    df = df.drop("Adj Close", 1)
    df = df.drop("Volume", 1)
    row = df.iloc[1:5]
    jsonified = json.dumps({
                   'Date':row["Date"].tolist(),
                   'Close':row["Close"].tolist()
            })
    jsonified = "update`;"+jsonified
    print(jsonified)
    x = 0
    return x

m = CSVtoDF("AAPL.csv")


def test():
    x = np.arange(0,np.pi*10,0.1).tolist()
    print(x)
    m = json.dumps({
            'x':x[0:50],
            'y':x[0:1]
    })
    
    return m
# print(test())


