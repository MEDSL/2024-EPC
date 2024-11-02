##############################
## Voter Registration FL graphing
## Sina Shaikh
## Note that this won't run on the server correctly, would need some tweaks
##############################

# load necessary packages
library(lubridate)
library(showtext)
library(readxl)
library(scales)

# Set font
font_add(THE_FONT_YOU_WANT_TO_ADD)
showtext_auto()


# Set working directory
setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

# Create empty df 
date <- gsub('\\.(csv|xlsx)$', '', list.files(path ="."))
other <- rep(0, length(list.files(path =".")))
dem <- rep(0, length(list.files(path =".")))
rep <- rep(0, length(list.files(path =".")))

AZ <- data.frame(date, other, dem, rep)

for (i in 1:4)  {
  # Read in data
  temp <- data.frame(read.csv(list.files(path =".")[i]))
  
  names(temp) <- temp[which(temp[,1] == "District")[1],]
  
  AZ$rep[i] <- as.numeric(gsub(',', '', temp$Republican[temp$District == "State Total:"][1], ))
  AZ$dem[i] <- as.numeric(gsub(',', '', temp$Democratic[temp$District == "State Total:"][1], ))
  AZ$other[i] <- as.numeric(gsub(',', '', temp$Other[temp$District == "State Total:"][1], ))
  
}

for (i in 5:7)  {
  # Read in data
  temp <- data.frame(read_excel(list.files(path =".")[i]))
  
  names(temp) <- temp[which(temp[,1] == "District")[1],]
  

  AZ$rep[i] <- as.numeric(gsub(',', '', temp$Republican[temp$District == "State Total:" & !is.na(temp$Republican)][1], ))
  AZ$dem[i] <- as.numeric(gsub(',', '', temp$Democratic[temp$District == "State Total:" & !is.na(temp$Democratic)][1], ))
  AZ$other[i] <- as.numeric(gsub(',', '', temp$Other[temp$District == "State Total:" & !is.na(temp$Other)][1], ))
  
}




temp <- data.frame(read.csv(list.files(path =".")[8]))

names(temp) <- temp[which(temp[,1] == "District")[1],]


AZ$rep[8] <- as.numeric(gsub(',', '', temp$Republican[temp$District == "State Total:" & !is.na(temp$Republican)][1], ))
AZ$dem[8] <- as.numeric(gsub(',', '', temp$Democratic[temp$District == "State Total:" & !is.na(temp$Democratic)][1], ))
AZ$other[8] <- as.numeric(gsub(',', '', temp$Other[temp$District == "State Total:" & !is.na(temp$Other)][1], ))


AZ$year <- ifelse(grepl("2020", AZ$date), "2020", "2024")
AZ$date <- sub("2020", "2024", AZ$date)
AZ$date <- as.Date(AZ$date, "%Y%m%d")


# Store graph
png(paste0(A_PLACE_TO_STORE_FIGURES, format(Sys.time(), "%Y%m%d"), ".png"), pointsize=7, width=1190, height=1000, res=300)

# Change font
par(family = "styrene")


xlim_dates <- c(min(AZ$date), max(AZ$date))


plot(NULL,
     main = "Arizona Voter Registration 2020 vs. 2024",
     xlim = xlim_dates,
     ylim = c(min(AZ$dem)*.9,max(AZ$rep)*1.1),
     xlab = "Date",
     ylab = "Registration",
     pch = 16,
     xaxt = "n",
     yaxt = "n")


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
          format = "%b",
          cex.axis = .8)

axis(2, at = seq(1000000, 1600000, by = 100000), labels = c("1M", "1.1M", "1.2M", "1.3M", "1.4M", "1.5M", "1.6M"), cex.axis = .8)



# Add lines
lines(AZ$date[AZ$year == "2020"], 
      AZ$other[AZ$year == "2020"],
      col = alpha("#c0ba79", .75),
      lwd = 2,
      lty = 3,
      type = "o",
      cex  = 1.3,
      pch = 16)


# Add lines
lines(AZ$date[AZ$year == "2024"], 
      AZ$other[AZ$year == "2024"],
      col = alpha("#c0ba79", .75) ,
      lwd = 2,
      type = "o",
      cex  = 1.3,
      pch = 15)


# Add lines
lines(AZ$date[AZ$year == "2020"], 
      AZ$rep[AZ$year == "2020"],
      col = alpha("#f6573e", .75),
      lwd = 2,
      lty = 3,
      type = "o",
      cex  = 1.3,
      pch = 16)

# Add lines
lines(AZ$date[AZ$year == "2024"], 
      AZ$rep[AZ$year == "2024"],
      col = alpha("#f6573e", .75),
      lwd = 2,
      type = "o",
      cex  = 1.3,
      pch = 15)


# Add lines
lines(AZ$date[AZ$year == "2020"], 
      AZ$dem[AZ$year == "2020"],
      col = alpha("#3791ff", .75),
      lty = 3,
      lwd = 2,
      type = "o",
      cex  = 1.3,
      pch = 16)


# Add lines
lines(AZ$date[AZ$year == "2024"], 
      AZ$dem[AZ$year == "2024"],
      col = alpha("#3791ff", .75),
      lwd = 2,
      type = "o",
      pch = 15,
      cex  = 1.3)



legend(as.Date("01/01/2024", "%m/%d/%Y"), 1600000, legend=c("Republican",
                                                             "Democrat",
                                                             "Other"),
       col=c("#f6573e", "#3791ff","#c0ba79"), lty=1, cex=0.7,
       text.font=2, lwd = 3)

legend(as.Date("01/01/2024", "%m/%d/%Y"), 1510000, legend = c("2020", "2024"),
       lty = c(3,1), cex = 0.7, pch  = 16:15)


mtext('Data Source: Arizona Secretary of State, azsos.gov/elections', side = 1, cex  = .55, at = as.Date("01282024", "%m%d%Y"), line = 3)
mtext('Graph Source: MIT Election Data and Science Lab, @MITelectionlab', side = 1, line  = 3.5, , cex = .55, at = as.Date("01282024", "%m%d%Y"))

dev.off()

# Save graphing data
write.csv(AZ, file = paste0(A_PLACE_TO_STORE_FIGURES,
                            format(Sys.time(), "%Y%m%d"),
                            "_AZ_reg.csv"),
          row.names = FALSE)


# Ensure that Rplots.pdf is not created
pdf(NULL)



