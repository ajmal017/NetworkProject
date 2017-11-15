# -*- coding: utf-8 -*-

import csv
import pandas as pd

def CSVtoDF(filePath):
    df = pd.read_csv(filePath)
    df = df.drop("Open", 1)
    df = df.drop("High", 1)
    df = df.drop("Low", 1)
    df = df.drop("Adj Close", 1)
    df = df.drop("Volume", 1)
    row = df.iloc[[2]].to_string(header=False, index=False, index_names=False).split("\n")
    vals = [','.join(ele.split()) for ele in row]
    print(vals)

def parseCSV(filePath):
    print("Parsing CSV")
    with open(filePath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        dates = []
        prices = []
        for row in readCSV:
            date = row[0]
            price = row[4]
            print(date, price)
            dates.append(date)
            prices.append(price)
        return dates,prices
    
    
CSVtoDF("AAPL.csv")