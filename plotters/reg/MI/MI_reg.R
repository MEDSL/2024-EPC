##############################
## Voter Registration MI graphing
## Sina Shaikh
##############################

# Set Libpath
.libPaths(new = A_PLACE_TO_STORE_HELPER_FILES)

# load and install necessary packages
if(!require("dplyr")) install.packages("dplyr", lib = A_PLACE_TO_STORE_HELPER_FILES)
if(!require("showtext")) install.packages("showtext", lib = A_PLACE_TO_STORE_HELPER_FILES)
library(dplyr)
library(showtext)

# Set font
font_add(THE_FONT_YOU_WANT_TO_ADD)


# Set working directory
setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)


# Create empty dataframe
date <- sub('\\.txt$', '', list.files(path ="."))
total <- rep(0, length(list.files(path =".")))
MI <- data.frame(date, total)

# Iterate through files
for (i in 1:length(list.files(path ="."))){
  
  # Read the entire file into R as a single column (I did it like this because its space seperated which is weird)
  lines <- readLines(list.files(path =".")[i])
  
  # Split each line into two parts: county name and population
  split_lines <- strsplit(lines, "\\s{2,}")
  
  # Convert the list to a data frame
  date <- do.call(rbind, lapply(split_lines, function(x) data.frame(county = x[1], registration = as.numeric(x[2]), stringsAsFactors = FALSE)))
  
  # Update total for date
  MI$total[i] <- sum(date$registration)
}

# Fix dates
MI$date <- as.Date(MI$date, "%Y%m%d")

# Make it weekly and make it change
MI_weekly_change <- MI[MI$date %in% seq(as.Date("07/19/2024", "%m/%d/%Y"),
                           as.Date(format(Sys.time(), "%Y%m%d"), "%Y%m%d"), by = "1 week"),]

for (i in nrow(MI_weekly_change):2){
  MI_weekly_change$total[i] <- MI_weekly_change$total[i] - MI_weekly_change$total[i-1]
}
MI_weekly_change <- MI_weekly_change[-1,]


## Start the graphing

# Store graph
png(paste0(A_PLACE_TO_STORE_FIGURES, format(Sys.time(), "%Y%m%d"), ".png"), pointsize=7, width=1190, height=1000, res=300) 

# Font
par(family = "styrene")
showtext_auto()
par(mar = c(6.0, 4.1, 4.1, 2.1))

xlim_dates <- c(min(MI_weekly_change$date), max(MI_weekly_change$date))

plot(NULL,
     main = paste0("Michigan Weekly Voter Registration ", format(Sys.time(), "%m/%d/%Y")),
     xlim = xlim_dates,
     ylim = c(min(MI_weekly_change$total)*1.5,max(MI_weekly_change$total)*1.5),
     xlab = "Week Ending Friday",
     ylab = "Net Change in Registration",
     cex.main = 4,
     cex.lab = 3.5,
     pch = 16,
     xaxt = "n",
     yaxt = "n")



# Determine tic lines
date_labs <- c()

if(length(seq(xlim_dates[1], xlim_dates[2], by = "1 week")) <= 8){
  date_labs <- seq(xlim_dates[1], xlim_dates[2], by = "1 week")
} else if(length(seq(xlim_dates[1], xlim_dates[2], by = "1 week"))  > 8 & length(seq(xlim_dates[1], xlim_dates[2], by = "1 week"))  <=16){
  date_labs <- seq(xlim_dates[1], xlim_dates[2], by = "2 weeks")
} else if(length(seq(xlim_dates[1], xlim_dates[2], by = "1 week"))  > 16){
  date_labs <- seq(xlim_dates[1], xlim_dates[2], by = "1 month")
}


# Add tic marks and labels
axis.Date(1,
          at = date_labs,
          format = "%b %d",
	  cex.axis = 2)

axis(2, at = seq(-10000, 50000, by = 10000), labels = formatC(seq(-10000, 50000, by = 10000), format ="d", big.mark = ","), cex.axis = 2)

# Add grid
abline(v = seq(xlim_dates[1], xlim_dates[2], by = "1 week"), col = "lightgray", lty = "dotted")
abline(h = seq(-5000, 50000, by = 5000), col = "lightgray", lty = "dotted")


# Add primary date
abline(v = as.Date("08/06/2024", "%m/%d/%Y"), col = "#948de5", lwd=2)
text(as.Date("08/06/2024", "%m/%d/%Y") + .5, 32000, "State Primary", col = "#948de5", cex = 2, pos = 4)


# Add lines + points
lines(MI_weekly_change$date, 
      MI_weekly_change$total,
      col = "#c0ba79" ,
      lwd = 3 ,
      pch=19)
points(MI_weekly_change$date, 
       MI_weekly_change$total,
       col = "#c0ba79" ,
       lwd = 3 ,
       pch=19)

mtext('Data Source: Michigan Department of State, michigan.gov/sos/elections', side = 1, cex  = 1.5, at = as.Date("07152024", "%m%d%Y"), line = 4, adj = 0)
mtext('Graph Source: MIT Election Data and Science Lab, @MITelectionlab', side = 1, line  = 4.5, , cex = 1.5, at = as.Date("07152024", "%m%d%Y"), adj = 0)


dev.off()


# Write data
write.csv(MI_weekly_change, file = paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,format(Sys.time(), "%Y%m%d"),"_MI_reg.csv"), row.names = FALSE)


# prevents Rplots.pdf from being generated
pdf(NULL)
