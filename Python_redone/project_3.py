import functions
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pmdarima as pm
import pandas as pd
import numpy as np
from   statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def create_plots(plot_type,data,variable_name,use_log_diff,output_file):

    #Separate dates and use them as df indecies
    dates = data.iloc[0:,0]
    pure_data = data.iloc[0:,1:]
    pure_data.index = dates
    print(pure_data)

    #Determine which differentation to use for the variable by name and apply it
    p = pure_data[variable_name]
    if use_log_diff: r = functions.log_diff(p)
    else: r = functions.difference(p)
    print(r)

    #Run adfuller tests
    p_adf = adfuller(p, autolag='AIC')
    r_adf = adfuller(r, autolag='AIC')

    #Plot stationary vs non stationary if selected
    if plot_type == "stat":

        figure = plt.figure()
        plt.plot(p)
        plt.close()
        output_file.savefig(figure)
        figure = plt.figure()
        plt.plot(r)
        plt.close()
        output_file.savefig(figure)

    #Automatically fit an ARIMA model
    out1 = pm.auto_arima(r, start_p=1, start_q=1,
                      test='adf',      
                      max_p=3, max_q=3,
                      m=1,             
                      d=None,           
                      seasonal=False,   
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)
    
    #Make a forecast and concat it in dataframe with past data
    out1.predict_in_sample()

    forecast  = pd.DataFrame(np.concatenate([r,out1.predict_in_sample()], axis =0))
    
    #Plot the forecast if selected
    if plot_type == "pred":

        figure = plt.figure()
        plt.plot(forecast, c='blue')
        plt.close()
        output_file.savefig(figure)
    
    #Plot acf's for transformed data and the forecast concat data
    if plot_type == "acf":

        figure = plt.figure()
        plot_acf(r,lags=20)
        plt.close()
        output_file.savefig(figure)

        figure = plt.figure()
        plot_acf(forecast,lags=20)
        plt.close()
        output_file.savefig(figure)

def run_code(country_code,plot_type):

    #Load all of the data
    data = functions.load_country_data(country_code)
    pure_data = data.iloc[0:,1:]

    #Open an output pdf for selected plots type and country
    output_file = PdfPages(country_code + "_" + plot_type + ".pdf")
    
    #Iteratively create plots for all of the analyzed economic variables
    for variable_name in pure_data.columns:
        log_difference_bool = variable_name == "Market"
        create_plots(plot_type,data,variable_name,log_difference_bool,output_file)
    
    output_file.close()