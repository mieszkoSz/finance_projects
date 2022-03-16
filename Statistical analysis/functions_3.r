load_country_data <- function(country_code){
  
  months = load_data("Inflation_rate.csv")["Month"]
  inflation = load_data("Inflation_rate.csv")[country_code]
  money_supply = load_data("M2_growth.csv")[country_code]
  unemployment_rate = load_data("Unemployment_rate.csv")[country_code]
  ipi = load_data("IPI.csv")[country_code]
  pmi = load_data("PMI.csv")[country_code]
  market_return = load_data("Index_returns.csv")[country_code]
  
  colnames(inflation) <- c("Inflation")
  colnames(money_supply) <- c("M2")
  colnames(unemployment_rate) <- c("Unemployment")
  colnames(ipi) <- c("IPI")
  colnames(pmi) <- c("PMI")
  colnames(market_return) <- c("Market")
  
  data <- cbind(months,market_return,inflation,money_supply,unemployment_rate,ipi,pmi)
  return(data)
}

load_data <- function(filename){
  print("test")
  path = paste("\\data\\",filename,sep="")
  path = paste(getwd(),path,sep="")
  temp_data <- read.csv(path, header=TRUE)
  return(temp_data)
}

log.return <- function(z){diff(log(z))}

#plot_types are: acf,stat and pred for ACF plots, Stationary vs non-stationary plots and forecast plot respectively.
master_function <- function(plot_type,data,variable_name,use_log_difference){
  
  dates = as.Date(data[,1])
  pure_data = data[,2:NCOL(data)]
  pure_data <- apply(pure_data, 2, as.numeric)
  rownames(pure_data) <- as.character(dates)
  
  if(use_log_difference){
    r <- log.return(pure_data[,variable_name])
  } else {
    r <- diff(pure_data[,variable_name])
  }
  
  d <- as.Date(rownames(r))
  
  #Check for stationarity
  library("tseries")
  dfp <- adf.test(pure_data[,variable_name])
  dfr <- adf.test(r)
  print(dfp)
  print(dfr)
  
  #Plot before vs after diff / log diff
  if(dfp$p.value < 0.1){
    title <- paste(variable_name,"raw data","is stationary with DF p-value of:",round(dfp$p.value,digits=3),sep=" ")
  } else {
    title <- paste(variable_name,"raw data","is non-stationary with DF p-value of:",round(dfp$p.value,digits=3),sep=" ")
  }
  if(plot_type == "stat"){
    plot(pure_data[,variable_name] ~ dates, type="l",ylab = variable_name,main=title, xlab = "Date")
  }
  
  
  if(use_log_difference){
    temp <- "log return/growth"
    title <- paste(variable_name,"period to period",temp,"is stationary with DF p-value of:",round(dfr$p.value,digits=3),sep=" ")
  } else {
    temp <- "return/growth"
    title <- paste(variable_name,"period to period",temp,"is stationary with DF p-value of:",round(dfr$p.value,digits=3),sep=" ")
  }
  y_lab = paste(variable_name,temp,sep=" ")
  if(plot_type == "stat"){
    plot(r ~ dates[-1], type="l",ylab=y_lab,main=title, xlab = "Date")
  }
  
  #Calculate auto fitted arma
  library("forecast")
  library("lubridate")
  out1 <- auto.arima(r, ic="aicc")
  out2 <- auto.arima(r, ic="aic")
  out3 <- auto.arima(r, ic="bic")
  
  summary(out1)
  summary(out2)
  summary(out3)
  
  #Compare acf's to check if the model explains the series
  
  r_acf = acf(r,plot=FALSE)
  if(plot_type == "acf"){
    plot(r_acf,main=paste(variable_name,"return/change ACF",sep=" "))
  }
  res <- out2$residuals
  
  residuals_acf = acf(res,plot=FALSE)
  if(plot_type == "acf"){
    plot(residuals_acf,main=paste(variable_name,"model residuals ACF",sep=" "))
  }
  
  #Make a forecast
  periods=12
  forecast_dates = dates[-1]
  for(i in 1:periods){
    temp_date <- forecast_dates[length(forecast_dates)] %m+% months(1)
    forecast_dates <- append(forecast_dates,temp_date)
  }
  print(forecast_dates)
  
  
  temp <- "return/growth"
  model_used <- summary(out2)
  if(use_log_difference){temp <- "log return/growth"}
  title <- paste(periods,"months",model_used,"forecast for",variable_name,temp)
  my_forecast <-forecast(out2,h=periods)
  if(plot_type == "pred"){
    plot( forecast(out2,h=periods),ylab=paste(variable_name,temp,sep=" "),main=title,xlab="Period")
  }
  
}