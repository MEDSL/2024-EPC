###############################################################################
# Plot Georgia's voter registrations
###############################################################################
# Set Libpath
.libPaths(new = A_PLACE_TO_STORE_HELPER_FILES)

# load and install necessary packages
if(!require("showtext")) install.packages("showtext", 
                        lib = A_PLACE_TO_STORE_HELPER_FILES)
library(showtext)

# Set font
font_add(THE_FONT_YOU_WANT_TO_ADD)

# Set working directory
setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

WEEKLY <- TRUE
WEEKDAY <- "Friday"

# Load the data
ga <- read.csv("ga_reg.csv")

# Fix dates
ga$date <- as.Date(ga$date, "%Y-%m-%d")

ga$weekday <- weekdays(ga$date)
if (WEEKLY){
  ga <- ga[ga$weekday == WEEKDAY | 
	   ga$date == as.Date('2024-10-10', "%Y-%m-%d"),]
}

#Compute daily changes
ga$regdiff <- rep(NA, nrow(ga))
ga$actdiff <- rep(NA, nrow(ga))
for(i in seq(2,nrow(ga))){
  ga$regdiff[i] <- ga$registered[i] - ga$registered[i-1]
  ga$actdiff[i] <- ga$active[i] - ga$active[i-1]
}

## Start the graphing

# Store graph
png(paste0(A_PLACE_TO_STORE_FIGURES,
    format(Sys.time(), "%Y%m%d"), ".png"), pointsize=7,
    width=1190, height=1000, res=300) 

# Font
par(family = "styrene")
showtext_auto()
par(mar = c(6.0, 4.1, 4.1, 2.1))

ga <- ga[2:nrow(ga),]
xlim_dates <- c(min(ga$date), max(ga$date))
numDays <- as.integer(diff(range(xlim_dates)))
YMAX <- max(max(ga$actdiff,ga$regdiff))*1.2

plot(NULL,
     main = paste0("Weekly Change in Georgia Voter Registration ",
                   format(Sys.time(), "%m/%d/%Y")),
     xlim = xlim_dates,
     ylim = c(min(min(0,ga$actdiff,ga$regdiff))*0.9, YMAX),
     xlab = "Data As Of",
     ylab = "Net Change Since Previous Week",
     cex.main = 4,
     cex.lab = 3.5,
     pch = 16,
     xaxt = "n",
     yaxt = "n")
#Add gridlines
abline(v = seq(xlim_dates[1], xlim_dates[2], by = "1 week"),
       col = adjustcolor("lightgray", alpha=0.8),
       lty = "solid")
ySeq <- seq(-10000, YMAX, by = 10000)
abline(h = ySeq, col = adjustcolor("lightgray", alpha=0.8), lty = "solid")
#Add change in registered voters
lines(ga$date, 
      ga$regdiff,
      col = "#c0ba79" ,
      lwd = 3 ,
      pch=19)
points(ga$date, 
       ga$regdiff,
       col = "#c0ba79",
       cex = 1.5,
       pch=19)
#Add change in active voters
lines(ga$date, 
      ga$actdiff,
      col = "#37C256",
      lwd = 3 ,
      pch=19)
points(ga$date, 
       ga$actdiff,
       col = "#37C256",
       cex = 1.5,
       pch=19)

date_labs <- seq(xlim_dates[1], xlim_dates[2], by = "1 week")
axis.Date(1,
          at = date_labs,
          format = "%b %d",
    cex.axis = 2)
axis(2, at = ySeq,
        labels = formatC(ySeq, format ="d", big.mark = ","), cex.axis = 2)


mtext('Data Source: Georgia Secretary of State, sos.ga.gov/election-data-hub',
      side = 1, cex  = 1.5, at = as.Date("09302024", "%m%d%Y")+1, line = 4)
mtext('Graph Source: MIT Election Data and Science Lab, @MITelectionlab',
      side = 1, line  = 4.5, , cex = 1.5,
      at = as.Date("09302024", "%m%d%Y")+0.88)
mtext("*Data were collected on Fridays", side = 1, line  = 3.25, cex = 2,
      at = as.Date("10142024", "%m%d%Y")+0.88)
mtext("and show a week-by-week change,", side = 1, line  = 4, cex = 2,
      at = as.Date("10142024", "%m%d%Y")+0.88)
mtext("except on Thursday, October 10.", side = 1, line  = 4.75, cex = 2,
      at = as.Date("10142024", "%m%d%Y")+0.88)

# Manual legend
rect(xleft=min(xlim_dates)+0.1,
     #Set the right boundary to the inverse of the 1-day plot expansion unit
     xright=min(xlim_dates)+(1/3*numDays),
     ybottom=3000,
     ytop=12000,
     col='white'
    )
legend(x="bottomleft", legend=c("Registered Voters"),
       col=c("#c0ba79"), lty=1, cex = 2, seg.len = 0.8,
       text.width=4, bty='n', lwd = 2)
legend(x="bottomleft", inset=c(0,0.05), legend=c("Active Voters"),
       col=c("#37C256"), lty=1, cex = 2, seg.len = 0.8,
       text.width=4, bty='n', lwd = 2)


dev.off()

fileSaveLoc <- A_PLACE_TO_STORE_DATA_FOR_THIS_STATE
write.csv(ga,file = paste0(fileSaveLoc,format(Sys.time(), "%Y%m%d"),
                           "_GA_reg.csv"), row.names = FALSE)

# prevents Rplots.pdf from being generated
pdf(NULL)
