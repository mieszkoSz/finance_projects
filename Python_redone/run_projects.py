import project_1 as p1
import project_2 as p2
import project_3 as p3

#Run project 1 code
#Please use spaces in country names
p1.run_code(country_name="United States")

#Run project 2 code.
#Provide country code to generate apropriate regression p_values and coefficients.
#US, EU, and JP for United States, European Union, and Japan respectively
p2.run_code(country_code="US")

#Run project 3 code.
#Plot types: "stat" = stationarity vs non-stationarity with DF p-val, "acf" = ACF plots, "pred" = ARIMA forecast plot
#Country codes: US, EU, and JP for United States, European Union, and Japan respectively
p3.run_code(country_code="US",plot_type="stat")