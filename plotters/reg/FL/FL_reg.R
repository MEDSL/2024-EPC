##############################
## Voter Registration FL graphing
## Sina Shaikh
##############################

# Helper file used for all plotting
source(paste0(A_PLACE_TO_STORE_HELPER_FILES,"plotting_helpers.R"))

# Packages ---------------------------------------------------------------------

packages <- c("readxl", 
  "lubridate", 
  "showtext")
custom_library_load(packages)

# Analysis ---------------------------------------------------------------------

# Set working directory
setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

FL <- data.frame(
  date = paste(month.name[1:(month(Sys.time()) - 1)], "2024"),
  rep = 0,
  dem = 0,
  minor = 0,
  no_party = 0
)

for (i in 2:month(Sys.time())){
  prev <- data.frame(read_excel(list.files(path =".",
       pattern ="Party Affilation by County 2020"), i))
  
  month <- data.frame(read_excel(list.files(path = ".",
       pattern = paste0("2024-post.*", 
              tolower(month.abb[month(Sys.time()) - 1]))), i))


  FL$rep[i-1] <- as.numeric(month[month[,1] == "TOTALS",2]) -
       as.numeric(prev[prev[,1] == "TOTALS",2])
  FL$dem[i-1] <- as.numeric(month[month[,1] == "TOTALS",3]) - 
       as.numeric(prev[prev[,1] == "TOTALS",3])
  FL$minor[i-1] <- as.numeric(month[month[,1] == "TOTALS",4]) - 
       as.numeric(prev[prev[,1] == "TOTALS",4])
  FL$no_party[i-1] <- as.numeric(month[month[,1] == "TOTALS",5]) - 
       as.numeric(prev[prev[,1] == "TOTALS",5])
  
}


FL$date <- as.Date(paste0("01 ", FL$date), "%d %B %Y")

FL <- na.omit(FL)

FL$other <- FL$minor + FL$no_party

# Plotting ---------------------------------------------------------------------

# Because this graph is pretty distinct from others, both in its x-axis time
# scale and in its legend contents, I've just done those seperately in this
# file rather than creating new functions

max_val <- max(FL$rep, FL$dem, FL$minor, FL$no_party)
min_val <- min(FL$rep, FL$dem, FL$minor, FL$no_party)
xlim_dates <- c(min(FL$date), max(FL$date))

png(paste0(A_PLACE_TO_STORE_FIGURES,
       format(Sys.time(), "%Y%m%d"), ".png"), 
       pointsize=7, 
       width=1190, 
       height=1000, 
       res=300)

font_add(THE_FONT_YOU_WANT_TO_ADD)
showtext_auto()
par(family = "styrene", mar = c(6, 4.1, 4.1, 2.1))

plot(NULL,
     main = "Change in Registered Florida Voters Since 2020",
     xlim = xlim_dates,
     ylim = c(min_val * 1.8, max_val*2),
     xlab = "Month",
     ylab = "2024 Reg - 2020 Reg",
     pch = 19,
     cex.main = 4,
     cex.lab = 3.5,
     xaxt = "n",
     yaxt = "n",
     cex.axis  = 1)

axis.Date(1, 
       at = seq(xlim_dates[1], xlim_dates[2], by = "1 month"), 
       format = "%b", 
       cex.axis = 2)
axis(2, 
       at = seq(-1500000, 500000, by = 500000), 
       labels = c("-1.5M", "-1M", "-0.5M", "0", "+0.5M"), 
       cex.axis = 2)

# Add grid
abline(h = seq(-2000000, 2000000, by = 500000), tck = 1, lwd = .5, col = "gray")
abline(v = seq(xlim_dates[1], xlim_dates[2], by = "1 month"),
       tck = 1, 
       lwd = .5, 
       col = "gray")

abline(h = 0, lwd = 2)

lines(FL$date, 
      FL$minor,
      col = "#c0ba79",
      lwd = 2,
      type = "o")

lines(FL$date, 
      FL$no_party,
      col = "#948de5",
      lwd = 2,
      type = "o")

lines(FL$date, 
      FL$rep,
      col = "#f6573e",
      lwd = 2,
      type = "o")

lines(FL$date, 
      FL$dem,
      col = "#3791ff",
      lwd = 2,
      type = "o")

rect(xleft = xlim_dates[1],
       xright = xlim_dates[1] +
              as.numeric((xlim_dates[2] - xlim_dates[1])) / 2.8,
       ytop = -1010000, 
       ybottom = -1500000, 
       col = 'white')
legend("bottomleft", inset=c(0,0.11), legend=c("Republican"),
       col=c("#f6573e"), lty=1, cex = 2, seg.len = 0.8,
       text.width=4, bty='n', lwd = 3)
legend("bottomleft", inset=c(0,0.07), legend=c("Democrat"),
       col=c("#3791ff"), lty=1, cex = 2, seg.len = 0.8,
       text.width=4, bty='n', lwd = 3)
legend("bottomleft", inset=c(0,0.03), legend=c("Minor Party"),
       col=c("#c0ba79"), lty=1, cex = 2, seg.len = 0.8,
       text.width=4, bty='n', lwd = 3)
legend("bottomleft", inset=c(0,-.01), legend=c("No Party Affiliation"),
       col=c("#948de5"), lty=1, cex = 2, seg.len = 0.8,
       text.width=4, bty='n', lwd = 3)

add_std_margin_text(
       'Data Source: Florida Department of State, dos.fl.gov/elections',
       xlim_dates)

save_outputs(FL, "FL", "reg")





