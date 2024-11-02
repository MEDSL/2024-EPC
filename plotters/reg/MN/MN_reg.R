##############################
## Voter Registration MN graphing
## Zachary Djanogly Garai
##############################

print('Begin')
 
# Set Libpath
.libPaths(new = A_PLACE_TO_STORE_HELPER_FILES)

# Load necessary packages
if(!require("stringr")) install.packages("stringr", lib = A_PLACE_TO_STORE_HELPER_FILES)
library(stringr)
library(dplyr)
library(showtext)
library(readxl)
library(lubridate)
library(sysfonts)

# Set font
font_add(THE_FONT_YOU_WANT_TO_ADD)
showtext_auto()


# Set working directory
setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

# Load registration data
MNreg <- read.csv(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE+'MNreg.csv')
MNreg_totals <- tail(MNreg, n=1)
within(MNreg_totals, rm("County"))
MNregT <- setNames(as.data.frame(t(MNreg[-1])), MNreg[,1])
MNregT <- cbind(Month = rownames(MNregT), MNregT)
rownames(MNregT) <- NULL
MNregT$date_for_graphing <- as.Date(paste(MNregT$Month, "2024", "01"), "%B %Y %d")
MN <- MNregT[c('Month', 'date_for_graphing', ('TOTAL'))]
MN$change <- MN$TOTAL - subset(MN$TOTAL, MN$Month == 'December')

# split up month and year
#MN[c('month', 'year')] <- str_split_fixed(WI$date, '_', 2)

# Make everything 2024

# Order
MN[1, 'date_for_graphing'] <- as.Date(paste("December", "2023", "01"), "%B %Y %d")
MN <- MN[order(MN$date_for_graphing),]

# Store graph
png(paste0(A_PLACE_TO_STORE_FIGURES, format(Sys.time(), "%Y%m%d"), ".png"), pointsize=7, width=1190, height=1000, res=300)

font_add(THE_FONT_YOU_WANT_TO_ADD)
showtext_auto()

# Set Font
par(family = "styrene")

YMAX <- 10000
xlim_dates <- c(min(MN$date_for_graphing), max(MN$date_for_graphing))

par(mar = c(6.0, 4.1, 4.1, 2.1))

plot(NULL,
     main = "Change in Registered Minnesota Voters Since December 2023",
     xlim = xlim_dates,
     ylim = c(-max(MN$change*1.2), max(MN$change*1.2)),
     xlab = "Month",
     ylab = "Net Change Minn. Registrants Since 12/23",
     pch = 16,
     cex.main = 3.5,
     cex.lab = 3,
     yaxt = "n",
     xaxt = "n")
axis.Date(1, at = seq(xlim_dates[1], xlim_dates[2], by = "1 month"), format = "%b '%y", cex.axis = 2) ## did this work? not like i hoped!
axis(2, at = seq(-50000, 50000, by = 25000), labels = formatC(seq(-50000, 50000, by = 25000), format ="d", big.mark = ","), cex.axis = 2)

# Add grid manually
abline(h = seq(-50000, 50000, by = 25000), tck = 1, lty = 2, col = "gray")
abline(v = seq(xlim_dates[1], xlim_dates[2], by = "1 month"), tck = 1, lty = 2, col = "gray")


# Add lines + points
lines(MN$date_for_graphing, 
      MN$change,
      col = "#c0ba79",
      lwd = 3,
      type = "o",
      pch=19)


mtext('Data Source: Minnesota Secretary of State, sos.state.mn.us', side = 1, cex  = 1.5, at = as.Date("01212024", "%m%d%Y"), line = 4)
mtext('Graph Source: MIT Election Data and Science Lab, @MITelectionlab', side = 1, line  = 4.5, , cex = 1.5, at = as.Date("01212024", "%m%d%Y"))

dev.off()

print('Plotted')

# Write to csv
write.csv(MN, file = paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,
                            format(Sys.time(), "%Y%m%d"),
                            "_MN_reg.csv"),
          row.names = FALSE)

# Ensure that Rplots.pdf is not created
pdf(NULL)
print('Done')
