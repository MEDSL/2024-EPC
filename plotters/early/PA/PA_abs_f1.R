##############################
## Absentee Ballots PA graphing
## Sina Shaikh
##############################

# Global -----------------------------------------------------------------------

# Toggle for plotting apps vs sent
SENT = TRUE

# Helper file used for all plotting
source(paste0(A_PLACE_TO_STORE_HELPER_FILES,"plotting_helpers.R"))

# Packages ---------------------------------------------------------------------

packages <- c("stringr", 
  "lubridate", 
  "showtext", 
  "readxl", 
  "dplyr", 
  "scales",
  "data.table")
custom_library_load(packages)

# Analysis ---------------------------------------------------------------------

clean_mail_ballots <- function(mail_ballots, start_date, end_date, type) {
    

    mail_ballots <- mail_ballots[mail_ballots$AppReturnDate != "",]
    mail_ballots <- mail_ballots[!is.na(mail_ballots$Party),]

    if(SENT){
      if(type == "slashed"){
        mail_ballots$AppReturnDate <- as.Date(mail_ballots$BallotSentDate, "%m/%d/%Y")
      } else {
        mail_ballots$AppReturnDate <- as.Date(mail_ballots$BallotSentDate, "%Y-%m-%d")
      }
    } else {
      mail_ballots$AppReturnDate <- as.Date(mail_ballots$AppReturnDate, "%m/%d/%Y")
    }

    if(type == "slashed"){
        mail_ballots$BallotReturnedDate <- as.Date(
            mail_ballots$BallotReturnedDate, "%m/%d/%Y")
    } else {
        mail_ballots$BallotReturnedDate <- as.Date(
            mail_ballots$BallotReturnedDate, "%Y-%m-%d")
        mail_ballots <- mail_ballots[mail_ballots$Ballot.Application.Disposition == "Approved",]
    }


    # Here we are interested in Applications returned rather than Ballots sent
    # because the BallotSentDate variable doesn't actually correspond to when the
    # ballots are sent, rather it corresponds to when they are printed, at least in
    # some counties (according to the PA secretary of stat and the Butler County
    # Director of elections)
    apps <- summarize(group_by(mail_ballots, AppReturnDate),
                            rep = sum(Party == "R"),
                            dem = sum(Party == "D"),
                            other = sum(!(Party %in% c("R", "D"))))

    ballot_returned <- summarize(group_by(mail_ballots, BallotReturnedDate),
                            rep = sum(Party == "R"),
                            dem = sum(Party == "D"),
                            other = sum(!(Party %in% c("R", "D"))))

    ballot_returned <- ballot_returned[!is.na(ballot_returned$BallotReturnedDate),]
    apps <- apps[!is.na(apps$AppReturnDate),]


    # If there are no applications received or no ballots returned in a given day
    # we want to fill in 0s so the graph is not discontinuous
    dates <- seq(start_date, end_date, by = "1 day")

    for (i in 1:length(dates)){
      if(!(dates[i] %in% ballot_returned$BallotReturnedDate)){
          ballot_returned <-rbind(ballot_returned, list(dates[i], 0,0,0))
      }
      if(!(dates[i] %in% apps$AppReturnDate)){
          apps <-rbind(apps, list(dates[i], 0,0,0))
      }
    }

    # Adding the 0s may make it so that the order of the dates may not be preserved
    ballot_returned <- ballot_returned[order(ballot_returned$BallotReturnedDate),]
    apps <- apps[order(apps$AppReturnDate),]

    # We want these values to be cummulative
    for (i in 2:nrow(apps)){
      apps[i,2:4] <- apps[i, 2:4] + apps[i-1, 2:4]
    }
    for (i in 2:nrow(ballot_returned)){
      if(!is.na(ballot_returned$BallotReturnedDate[1])){
          ballot_returned[i,2:4] <- ballot_returned[i,2:4] + ballot_returned[i-1, 2:4]
      }
    }

    return(list(apps = apps, ballot_returned = ballot_returned))

}

setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

# This finds all the files which have a date in them and don't have DDA in the
# title. This seems to be the easiest way to identify relevant files
files <- list.files(".")[!grepl("DDA", list.files(".")) &
  grepl("2024\\d{4}", list.files("."))]

# There is an open quotation somewhere in the file with no close quotation which
# causes it to break without specifically accounting for it. This also finds the
# most recent file based on the date in the title. WILL NEED TO BE MODIFIED FOR
# FUTURE YEARS
mail_ballots_2024 <- read.csv(
  files[which.max(sub(".*?(2024\\d{4}).*", "\\1", files))],
  sep = "|", 
  quote = "")

# Should be redundant but there were a few not labeled as 2024 GENERAL ELECTION
mail_ballots_2024 <- mail_ballots_2024[mail_ballots_2024$ElectionName ==
  "2024 GENERAL ELECTION",]

result_2024 <- clean_mail_ballots(mail_ballots_2024, 
    as.Date("20240701", "%Y%m%d"), 
    date(Sys.time()) - 1,
    "dashed")

apps_2024 <- result_2024$apps
ballot_returned_2024 <- result_2024$ballot_returned


# Truncate at sept 1st so recent changes are more distinguishable. We also used
# to truncate at the current date - 2 so that we didn't have to wait for the 
# current day's data to come out. Now we do wait for the current days data so
# we only have a one day lag as the current day's data is released at midday so
# only contains a few ballots from the current day.
apps_2024 <- apps_2024[apps_2024$AppReturnDate >= as.Date("20241005", "%Y%m%d") &
               apps_2024$AppReturnDate <= date(Sys.time()) - 1,]
ballot_returned_2024 <- ballot_returned_2024[ballot_returned_2024$BallotReturnedDate >=
  as.Date("20241005", "%Y%m%d") & ballot_returned_2024$BallotReturnedDate <=
  date(Sys.time()) - 1,]

# Ok now let's do the same thing for 2020
setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

mail_ballots_2020 <- fread("SWMB.110520.txt")

mail_ballots_2020 <- mail_ballots_2020[mail_ballots_2020$ElectionName ==
  "2020 GENERAL ELECTION",]

result_2020 <- clean_mail_ballots(mail_ballots_2020, 
    as.Date("20200701", "%Y%m%d"),
    as.Date("20201103", "%Y%m%d"),
    type = "slashed")

apps_2020 <- result_2020$apps
ballot_returned_2020 <- result_2020$ballot_returned

# Make it so that the dates represent days before the election
apps_2020 <- apps_2020[year(apps_2020$AppReturnDate) == 2020,]
ballot_returned_2020 <- ballot_returned_2020[year(ballot_returned_2020$BallotReturnedDate) == 2020,]

year(apps_2020$AppReturnDate) <- 2024
year(ballot_returned_2020$BallotReturnedDate) <- 2024

apps_2020$AppReturnDate <- apps_2020$AppReturnDate + 2
ballot_returned_2020$BallotReturnedDate <- ballot_returned_2020$BallotReturnedDate + 2

write.csv(ballot_returned_2020,
  file = paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,
    format(Sys.time(), "%Y%m%d"),
    "_returned_2020_PA_early.csv"),
  row.names = FALSE)

write.csv(apps_2020,
  file = paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,
    format(Sys.time(), "%Y%m%d"),
    "_apps_2020_PA_early.csv"),
  row.names = FALSE)

# Truncation is now with 2024 dates
apps_2020 <- apps_2020[apps_2020$AppReturnDate >= as.Date("20241005", "%Y%m%d") &
               apps_2020$AppReturnDate <= as.Date("20241105", "%Y%m%d"),]
ballot_returned_2020 <- ballot_returned_2020[ballot_returned_2020$BallotReturnedDate >=
  as.Date("20241005", "%Y%m%d") & ballot_returned_2020$BallotReturnedDate <=
  as.Date("20241105", "%Y%m%d"), ]


# Plotting ---------------------------------------------------------------------

xlim_dates <- c(min(apps_2020$AppReturnDate), max(apps_2020$AppReturnDate))
max_val <- max(apps_2024$rep + apps_2024$dem + apps_2024$other,
    apps_2020$rep + apps_2020$dem + apps_2020$other, na.rm = TRUE)

basic_plot(title = "Pennsylvania Mail Ballot Status",
  xlim_dates,
  xlabel = "Days Before the Election",
  ylabel = "Ballots Sent and Returned",
  y_tics = seq(0, 10000000, by = 500000),
  type = "early",
  state = "PA",
  max_val,
  days_before = TRUE,
  alt = "1v",
  y_mil = TRUE)

# Add lines
lines(apps_2024$AppReturnDate, 
      apps_2024$dem + apps_2024$other + apps_2024$rep,
      col = alpha("#c0ba79", .8),
      lwd = 2)
lines(ballot_returned_2024$BallotReturnedDate, 
      ballot_returned_2024$dem + ballot_returned_2024$rep + ballot_returned_2024$other,
      col = alpha("#37C256", .8),
      lwd = 2)

# Add 2020 lines
lines(apps_2020$AppReturnDate, 
      apps_2020$dem + apps_2020$other + apps_2020$rep,
      col = alpha("#c0ba79", .8),
      lwd = 2,
      lty = 3)
lines(ballot_returned_2020$BallotReturnedDate, 
      ballot_returned_2020$dem + ballot_returned_2020$rep + ballot_returned_2020$other,
      col = alpha("#37C256", .8),
      lwd = 2,
      lty = 3)

rect(xleft = xlim_dates[1],
      xright = xlim_dates[1] +
      as.numeric((xlim_dates[2] - xlim_dates[1])) / 3.5,
      ytop = max_val * 1.22, 
      ybottom = max_val * 1.1, 
      col = 'white')
legend("topleft", 
      inset = c(0, -0.06), 
      legend = c("Sent"),
      col = c("#c0ba79"), 
      lty = 1, 
      cex = 2, 
      seg.len = 0.8,
      text.width = 2, 
      bty = 'n', 
      lwd = 2)
legend("topleft", 
      inset = c(0, -0.02), 
      legend = c("Returned"),
      col = c("#37C256"), 
      lty = 1, 
      cex = 2, 
      seg.len = 0.8,
      text.width = 2, 
      bty = 'n', 
      lwd = 2)

rect(xleft = xlim_dates[1] + as.numeric((xlim_dates[2] - xlim_dates[1])) / 3.3,
    xright = xlim_dates[1] + as.numeric((xlim_dates[2] - xlim_dates[1])) / 1.9,
    ytop = max_val * 1.22, 
    ybottom = max_val * 1.1,
    col = 'white'
)
legend("topleft",
  inset=c(.31,-.06), 
  legend=c("2024"),
  lty = 1, 
  seg.len = 0.8,
  text.width = 2, 
  bty = 'n', 
  lwd = 2,
  cex = 2,
  pt.cex = 1,
  pch = 15
  )
legend("topleft",
  inset=c(.31,-.02), 
  legend=c("2020"),
  lty = 3, 
  seg.len = 0.8,
  text.width = 2, 
  bty = 'n', 
  lwd = 2,
  cex = 2,
  pt.cex = 1,
  pch = 16
  )

text(date(Sys.time()) - 1, 
  ballot_returned_2020$dem[ballot_returned_2020$BallotReturnedDate == date(Sys.time()) - 1] +
  ballot_returned_2020$rep[ballot_returned_2020$BallotReturnedDate == date(Sys.time()) - 1] + 
  ballot_returned_2020$other[ballot_returned_2020$BallotReturnedDate == date(Sys.time()) - 1], 
  paste0(signif((ballot_returned_2020$dem[ballot_returned_2020$BallotReturnedDate == date(Sys.time()) - 1] +
  ballot_returned_2020$rep[ballot_returned_2020$BallotReturnedDate == date(Sys.time()) - 1] + 
  ballot_returned_2020$other[ballot_returned_2020$BallotReturnedDate == date(Sys.time()) - 1]) / 
    (apps_2020$dem[apps_2020$AppReturnDate == date(Sys.time()) - 1] +
  apps_2020$rep[apps_2020$AppReturnDate == date(Sys.time()) - 1] + 
  apps_2020$other[apps_2020$AppReturnDate == date(Sys.time()) - 1]) * 100, 2), "% (2020)"), 
  cex = 1.5,
  pos = 4)

points(date(Sys.time()) - 1, 
  ballot_returned_2020$dem[ballot_returned_2020$BallotReturnedDate == date(Sys.time()) - 1] +
  ballot_returned_2020$rep[ballot_returned_2020$BallotReturnedDate == date(Sys.time()) - 1] + 
  ballot_returned_2020$other[ballot_returned_2020$BallotReturnedDate == date(Sys.time()) - 1],
  pch = 19,
  col = "#37C256")

points(date(Sys.time()) - 1, 
  ballot_returned_2024$dem[ballot_returned_2024$BallotReturnedDate == date(Sys.time()) - 1] +
  ballot_returned_2024$rep[ballot_returned_2024$BallotReturnedDate == date(Sys.time()) - 1] + 
  ballot_returned_2024$other[ballot_returned_2024$BallotReturnedDate == date(Sys.time()) - 1],
  pch = 15,
  col = "#37C256")


text(date(Sys.time()) - 1, 
  ballot_returned_2024$dem[ballot_returned_2024$BallotReturnedDate == date(Sys.time()) - 1] +
  ballot_returned_2024$rep[ballot_returned_2024$BallotReturnedDate == date(Sys.time()) - 1] + 
  ballot_returned_2024$other[ballot_returned_2024$BallotReturnedDate == date(Sys.time()) - 1], 
  paste0(signif((ballot_returned_2024$dem[ballot_returned_2024$BallotReturnedDate == date(Sys.time()) - 1] +
  ballot_returned_2024$rep[ballot_returned_2024$BallotReturnedDate == date(Sys.time()) - 1] + 
  ballot_returned_2024$other[ballot_returned_2024$BallotReturnedDate == date(Sys.time()) - 1]) / 
    (apps_2024$dem[apps_2024$AppReturnDate == date(Sys.time()) - 1] +
  apps_2024$rep[apps_2024$AppReturnDate == date(Sys.time()) - 1] + 
  apps_2024$other[apps_2024$AppReturnDate == date(Sys.time()) - 1]) * 100, 2), "% (2024)"), 
  cex = 1.5,
  pos = 4)

mtext("For each year, labels show percent of ballots",
        side = 1, 
        cex  = 1.5, 
        at = xlim_dates[2] - as.numeric((xlim_dates[2] - xlim_dates[1])) / 4, 
        line = 4, 
        adj = 0)
mtext('sent in that year which have been returned', 
        side = 1, 
        line = 4.5, 
        cex = 1.5, 
        at =  xlim_dates[2] - as.numeric((xlim_dates[2] - xlim_dates[1])) / 4, 
        adj = 0)

mtext("(Nov 5 2024/",
        side = 1, 
        cex  = 1.5, 
        at = xlim_dates[2], 
        line = 1.6)
mtext("Nov 3 2020)",
side = 1, 
cex  = 1.5, 
at = xlim_dates[2], 
line = 2.0)


add_std_margin_text(
  'Data Source: Pennsylvania Department of State, pa.gov', 
  xlim_dates)

dev.off()


# Ensure that Rplots.pdf is not created
pdf(NULL)

