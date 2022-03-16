import pandas as pd
import numpy as np

def log_diff(x):
    return np.diff(np.log(x))

def difference(x):
    return np.diff(x)

def load_country_data(country_code):

    months = pd.read_csv(".//data/Inflation_rate.csv",parse_dates= True)["Month"]
    inflation = pd.read_csv(".//data/Inflation_rate.csv",parse_dates= True)[country_code]
    money_supply = pd.read_csv(".//data/M2_growth.csv",parse_dates= True)[country_code]
    unemployment_rate = pd.read_csv(".//data/Unemployment_rate.csv",parse_dates= True)[country_code]
    ipi = pd.read_csv(".//data/IPI.csv",parse_dates= True)[country_code]
    pmi = pd.read_csv(".//data/PMI.csv",parse_dates= True)[country_code]
    market_return = pd.read_csv(".//data/Index_returns.csv",parse_dates= True)[country_code]

    frames = [months,market_return,inflation,money_supply,unemployment_rate,ipi,pmi]
    combined = pd.concat(frames,axis=1)
    combined.columns = ["Month","Market","Inflation","M2","Unemployment","IPI","PMI"]

    return combined
