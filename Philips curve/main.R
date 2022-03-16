#Empty the enviroment & set working directory
rm(list=ls(all=TRUE))
setwd("C:\\Users\\Mieszko\\Desktop\\Kings College\\Statistical programming\\assignment_1\\")

#Configuration variables
country_name <- "United.States"
library("moments")

#Load pre-processed eurostat data from local .csv files
harmonized_cpi <- read.csv("CPI.csv", header=TRUE)
unemployment_rate <- read.csv("Unemployment_rate_seasonaly_adjusted.csv", header=TRUE)

#Extract dates
get_dates <- function(data){return(data[,1])}

#Convert data into matrix format with dates as rownames
to_matrix_format <- function(data){ 
  data_matrix <- data[,2:NCOL(data)]
  data_matrix <- as.matrix(data_matrix)
  
  #Enforce numeric values, set rownames to dates
  data_matrix <- apply(data_matrix, 2, as.numeric)
  rownames(data_matrix) <- get_dates(data)
  
  return(data_matrix)
}

#Convert to matirices and extract dates
unemployment_r_matrix = to_matrix_format(unemployment_rate)
cpi_matrix = to_matrix_format(harmonized_cpi)
dates = get_dates(unemployment_rate)

#Convert to rates of change (YoY) and make stationary
cpi_change_YoY <- diff(log(cpi_matrix),lag=12)*100

#Get specific country series
cpi_change_YoY = cpi_change_YoY[,country_name]
monthly_unemployment = unemployment_r_matrix[-(1:12),country_name]

#Check for normality and save to .txt
jarque.test(cpi_change_YoY)
jarque.test(monthly_unemployment)

sink("normality_tests.txt")
print(jarque.test(cpi_change_YoY))
print(jarque.test(monthly_unemployment))
sink()

#Plot histograms and save to pdf
title = paste("CPI change distribution for ",country_name,sep=" ")
pdf(paste(title,".pdf",sep=""))
hist(cpi_change_YoY, main=title, col="blue")
dev.off()
title = paste("Unemployment rate distribution for ",country_name,sep=" ")
pdf(paste(title,".pdf",sep=""))
hist(monthly_unemployment, main=title, col="blue")
dev.off()

#Create a Linear Regression model for Philips Curve
liniear_regression <- lm(cpi_change_YoY~monthly_unemployment)
alfa_beta <- liniear_regression$coefficients
errors <- liniear_regression$residuals
summary(liniear_regression)

#Save liniear model summary to .txt
sink("liniear_model_summary.txt")
print(summary(liniear_regression))
sink()

#Make a scatter plot of Philips Curve and save to pdf
title = paste("Philips Curve for",country_name,sep=" ")
pdf(paste(title,".pdf",sep=""))
plot(x=monthly_unemployment, y=cpi_change_YoY, main= title, col="#984ea3", pch=20,
     xlab="Monthly unemployment rate (%)", ylab="CPI change YoY (%)")
abline(liniear_regression, col="#377eb8", lwd=3)
dev.off()

#Plot and save to pdf a boxplot of model errors
pdf("Philips curve regression errors boxplot.pdf")
boxplot(errors)
dev.off()