rm(list=ls())

# set the woking directory
setwd("C:\\Users\\")
source("functions_3.r")

#Configuration variables
country_code = "EU" #Codes are: US, EU, JP for United States, European Union and Japan accordingly
variable_name = "Market"
plot_type = "acf"
no_plots_per_layer = 2

data = load_country_data(country_code)

pdf(paste(plot_type,"_",country_code,".pdf",sep=""))
cols <- colnames(data)[-1]
use_log_difference = FALSE

par(mfrow = c(3,no_plots_per_layer))

for(variable_name in cols){
  if(variable_name == "Market"){use_log_difference = TRUE}
  master_function(plot_type,data,variable_name,use_log_difference)
  use_log_difference = FALSE
}

dev.off()
par(mfrow = c(1,1))