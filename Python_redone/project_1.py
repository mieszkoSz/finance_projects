from datetime import date
import pandas as pd
import numpy as np
from scipy import stats
from pandas.core.indexes import period
import functions
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

def run_code(country_name):

    #Load raw data
    CPI = pd.read_csv(".//philips_curve_data/CPI.csv",parse_dates= True)
    unemployment = pd.read_csv(".//philips_curve_data/Unemployment_rate_seasonaly_adjusted.csv",parse_dates= True)

    #Separate dates and use them as df indecies
    dates = CPI.iloc[0:,0]
    pure_CPI = CPI[country_name]
    pure_CPI.index = dates
    pure_unemployment = unemployment[country_name]
    pure_unemployment.index = dates

    print(dates)
    print(pure_CPI)
    print(pure_unemployment)

    #Make stationary
    pure_CPI = np.log(pure_CPI)
    pure_unemployment = np.log(pure_unemployment)
    pure_CPI = pure_CPI.diff(periods=12)
    pure_unemployment = pure_unemployment.diff(periods=12)

    #Cleanup inf and nan
    pure_CPI.replace([np.inf, -np.inf], np.nan, inplace=True)
    pure_unemployment.replace([np.inf, -np.inf], np.nan, inplace=True)
    pure_CPI = pure_CPI.dropna()
    pure_unemployment = pure_unemployment.dropna()

    #Perform Jarque–Bera tests and output to console
    jb_cpi = stats.jarque_bera(pure_CPI)
    print(jb_cpi)
    jb_unemployment = stats.jarque_bera(pure_unemployment)
    print(jb_unemployment)

    #Plot histograms
    sns.histplot(pure_CPI,stat='density',bins=20, kde=True).set_title("CPI")
    plt.show()
    sns.histplot(pure_unemployment,stat='density',bins=20, kde=True).set_title("Unemployment")
    plt.show()

    #Create linear regression model to evaluate the philips curve theory
    model = sm.OLS(pure_CPI, pure_unemployment).fit() 
    print(model.summary())

    #Plot a scatterplot + line of best fit ilustrating the philips curve
    model.params
    plt.scatter(pure_unemployment,pure_CPI)
    plt.title("Scatterplot")
    plt.plot([min(pure_unemployment), max(pure_unemployment)], [min(pure_unemployment*model.params[0]), max(pure_unemployment*model.params[0])], color='red')
    plt.xlabel("Unemployment")
    plt.ylabel("CPI")
    plt.show()


