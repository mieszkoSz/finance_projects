import pandas as pd
import numpy as np
import functions
import statsmodels.api as sm

#X is a matrix of explanatory variables
def do_MLR(X,Y,lag):

    #Slice the explanatory variables and variable being explained according to the lag
    num_rows, num_cols = X.shape
    X_slice = X.iloc[0:num_rows-lag,0:]
    Y_slice = Y.iloc[lag:num_rows,0:]
    Y_slice.index = X_slice.index

    #fit a MLR model and print summary to console
    MLR = sm.OLS(Y_slice,X_slice).fit()
    print(MLR.summary())

    #Extract the coefficients and p_values
    coeffs = MLR.params
    p_values = [MLR.pvalues[i] for i in range(len(coeffs))]
    
    #Make proper data frames and return
    coeffs = pd.DataFrame(coeffs)
    names = coeffs.index
    p_values = pd.DataFrame(p_values,index=names)

    return coeffs, p_values

def run_code(country_code):

    #Separate the dates from the data
    data = functions.load_country_data(country_code)
    dates = data.iloc[0:,0]
    pure_data = data.iloc[0:,1:]
    print(pure_data.head())

    Y = pure_data.iloc[0:,0]
    X = pure_data.iloc[0:,1:]

    #Transform the data with differentation or log differentiation
    Y = functions.log_diff(Y)
    X = X.apply(functions.difference)
    Y = pd.DataFrame(Y)
    X = pd.DataFrame(X)
    
    #Estimate MLR
    lag = 0
    coeffs, p_values = do_MLR(X,Y,lag)
    all_p_values = p_values
    all_coeffs = coeffs

    #Estimate MLR at various lags
    for lag in range(1,13):
        coeffs, p_values = do_MLR(X,Y,lag)
        coeffs.columns = [lag]
        p_values.columns = [lag]
        all_coeffs = pd.concat([all_coeffs,coeffs],axis=1)
        all_p_values = pd.concat([all_p_values,p_values],axis=1)

    #Transpose the results into vertical table and print to console
    all_coeffs = all_coeffs.transpose()
    all_p_values = all_p_values.transpose()
    print(all_coeffs)
    print(all_p_values)

    #Save the results locally in .CSV format
    all_coeffs.to_csv(country_code + "_coefficients.csv")
    all_p_values.to_csv(country_code + "_pvals.csv")