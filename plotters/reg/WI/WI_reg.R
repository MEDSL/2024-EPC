##############################
## Voter Registration WI graphing
## Sina Shaikh
##############################

# Set Libpath
.libPaths(new = A_PLACE_TO_STORE_HELPER_FILES)

# Load necessary packages
if(!require("stringr")) install.packages("stringr", lib = A_PLACE_TO_STORE_HELPER_FILES)
library(stringr)
library(dplyr)
library(showtext)
library(readxl)
library(lubridate)

# Set font
font_add(THE_FONT_YOU_WANT_TO_ADD)
showtext_auto()


# Set working directory
setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

# Weird exception
if(length(list.files(pattern = "August_Voter.xlsx") != 0)){
  file.rename("August_Voter.xlsx", "August_2024.xlsx")
}

# Create empty data frame
date <- c(sub('\\.csv$', '', list.files(path =".", pattern = "2024.csv")),
          sub('\\.xlsx$', '', list.files(path =".", pattern = "2024.xlsx")),
          sub('\\.xlsx$', '', list.files(path =".", pattern = "2020.xlsx")))
total <- rep(0, length(date))

WI <- data.frame(date, total)

# Have to split up cleaning because they changed their file structure a couple times
for (i in 1:length(list.files(path =".", pattern = "2024.csv"))){
  month <- read.csv(list.files(path =".", pattern = "2024.csv")[i])
  
  WI$total[date == sub('\\.csv$', '', list.files(path =".", pattern = "2024.csv")[i])] <-
    sum(month$VoterCount)
}

# Second file structure
for (i in 1:length(list.files(path =".", pattern = "2024.xlsx"))){
  month <- data.frame(read_excel(list.files(path =".", pattern = "2024.xlsx")[i], 1))
  
  WI$total[date == sub('\\.xlsx$', '', list.files(path =".", pattern = "2024.xlsx")[i])] <-
    sum(month$VoterCount)
}

# Third file structure
for (i in 1:length(list.files(path =".", pattern = "2020.xlsx"))){
  month <- data.frame(read_excel(list.files(path =".", pattern = "2020.xlsx")[i], 1))
  
  WI$total[date == sub('\\.xlsx$', '', list.files(path =".", pattern = "2020.xlsx")[i])] <-
    sum(month[,5])
}

print(WI)

# Remove Duplicates
WI <- WI[!duplicated(WI$date), ]

# split up month and year
WI[c('month', 'year')] <- str_split_fixed(WI$date, '_', 2)

# Make everything 2024
WI$date_for_graphing <- as.Date(paste(WI$month, "2024", "01"), "%B %Y %d")

# Order
WI <- WI[order(WI$date_for_graphing),]

# Store graph
png(paste0(A_PLACE_TO_STORE_FIGURES, format(Sys.time(), "%Y%m%d"), ".png"), pointsize=7, width=1190, height=1000, res=300)

# Set Font
par(family = "styrene")


YMAX <- 10000
xlim_dates <- c(min(WI$date_for_graphing), max(WI$date_for_graphing[duplicated(WI$date_for_graphing)]))

par(mar = c(6.0, 4.1, 4.1, 2.1))

plot(NULL,
     main = "Change in Registered Wisconsin Voters Since 2020",
     xlim = xlim_dates,
     ylim = c(min(WI$total[WI$year == "2024"] - WI$total[WI$year == "2020"][1:sum(WI$year == "2024")])*1.2, 
      max(WI$total[WI$year == "2024"] - WI$total[WI$year == "2020"][1:sum(WI$year == "2024")])*1.2),
     xlab = "Month",
     ylab = "Reg 2024 - Reg 2020",
     pch = 16,
     cex.main = 4,
     cex.lab = 3.5,
     yaxt = "n",
     xaxt = "n")


axis.Date(1, at = seq(xlim_dates[1], xlim_dates[2], by = "1 month"), format = "%b", cex.axis = 2)
axis(2, at = seq(-200000, 200000, by = 50000), labels = formatC(seq(-200000, 200000, by = 50000), format ="d", big.mark = ","), cex.axis = 2)

# Add grid manually
abline(h = seq(-200000, 200000, by = 50000), tck = 1, lty = 2, col = "gray")
abline(v = seq(xlim_dates[1], xlim_dates[2], by = "1 month"), tck = 1, lty = 2, col = "gray")


# Add lines + points
lines(WI$date_for_graphing[WI$year == "2020"][1:sum(WI$year == "2024")], 
      WI$total[WI$year == "2024"] - WI$total[WI$year == "2020"][1:sum(WI$year == "2024")],
      col = "#c0ba79",
      lwd = 3,
      type = "o",
      pch=19)


mtext('Data Source: Wisconsin Elections Commission, elections.wi.gov', side = 1, cex  = 1.5, at = as.Date("01212024", "%m%d%Y"), line = 4)
mtext('Graph Source: MIT Election Data and Science Lab, @MITelectionlab', side = 1, line  = 4.5, , cex = 1.5, at = as.Date("01212024", "%m%d%Y"))

dev.off()

# Write to csv
write.csv(WI, file = paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,
                                   format(Sys.time(), "%Y%m%d"),
                                   "_WI_reg.csv"),
          row.names = FALSE)

# Ensure that Rplots.pdf is not created
pdf(NULL)
