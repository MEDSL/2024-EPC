##############################
## Absentee Ballots in WI graphing
## Sina Shaikh
##############################

# Helper file used for all plotting
source(paste0(A_PLACE_TO_STORE_HELPER_FILES,"plotting_helpers.R"))

# Packages ---------------------------------------------------------------------

packages <- c("stringr", 
  "lubridate", 
  "showtext", 
  "readxl", 
  "dplyr", 
  "scales")
custom_library_load(packages)

# Analysis ---------------------------------------------------------------------

# Set working directory
setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

# Create empty df
WI <- data.frame(
  date = c(
    as.Date(sub(".* as of ([^,\\.]+).*", 
            "\\1 2024", 
            list.files(path = ".", pattern = "Municipal Absentee")), 
      format = "%B %d %Y"),
    as.Date(sub('\\.xlsx$',
            '', 
            list.files(path = ".", pattern = "2020.*\\.xlsx$")), 
      "%Y-%m-%d"),
    as.Date(sub('\\.csv$',
            '', 
            list.files(path = ".", pattern = "2020.*\\.csv$")), 
      "%Y-%m-%d")
  ),
  type = c(
    rep(0, length(list.files(path = ".", pattern = "Municipal Absentee"))),
    rep(1, length(list.files(path = ".", pattern = "2020.*\\.xlsx$"))),
    rep(2, length(list.files(path = ".", pattern = "2020.*\\.csv$")))
  ),
  apps = 0,
  sent = 0,
  returned = 0,
  in_person = 0
)

WI <- WI[order(WI$date),]

# WI has changed their file types 3 times over the course of 2020 and 2024 so
# far, we analyze them seperately
for (i in 1:sum(WI$type == 0)){
  
  files <- list.files(path = ".", pattern = "Municipal Absentee")

  dates <- as.Date(sub(".* as of ([^,\\.]+).*", "\\1 2024", files), 
                 format = "%B %d %Y")

  sorted_files <- files[order(dates)]

  day <- read.csv(sorted_files[i])


  WI[WI$type == 0,]$apps[i] <- 
      day$AbsenteeApplications[day$Jurisdiction == "TOTAL"]
  WI[WI$type == 0,]$sent[i] <- 
      day$BallotsSent[day$Jurisdiction == "TOTAL"]
  WI[WI$type == 0,]$returned[i] <- 
      day$BallotsReturned[day$Jurisdiction == "TOTAL"]
  WI[WI$type == 0,]$in_person[i] <- 
      day$InPersonAbsentee[day$Jurisdiction == "TOTAL"]

}

# Read second type of file
if(length(list.files(path = ".", pattern = "2020.*\\.xlsx$")) != 0){
  for (i in 1:sum(WI$type == 1)){
    day <- data.frame(read_excel(list.files(path = ".",
                          pattern = "2020.*\\.xlsx$")[i], 1))
    
    WI[WI$type == 1,]$apps[i] <-
        day$AbsenteeApplications[day$Jurisdiction == "TOTAL"]
    WI[WI$type == 1,]$sent[i] <- 
        day$BallotsSent[day$Jurisdiction == "TOTAL"]
    WI[WI$type == 1,]$returned[i] <- 
        day$BallotsReturned[day$Jurisdiction == "TOTAL"]
    WI[WI$type == 1,]$in_person[i] <- 
        day$InPersonAbsentee[day$Jurisdiction == "TOTAL"]
  }
}


# Read third type of file
for (i in 1:sum(WI$type == 2)){
  day <- read.csv(list.files(path = ".", pattern = "2020.*\\.csv$")[i])
  
  apps <- day[names(day)[str_detect(names(day), "Application")]]
  
  county <-  day[names(day)[str_detect(names(day), "Jurisdiction|County")]]
  
  sent <-  day[names(day)[str_detect(names(day), "Sent")]]
  
  returned <-  day[names(day)[str_detect(names(day), "Returned")]]

  in_person <-  day[names(day)[str_detect(names(day), "Person")]]

  
  WI[WI$type == 2,]$apps[i] <- apps[county == "TOTAL"]

  WI[WI$type == 2,]$sent[i] <- ifelse(length(sent),
                                      sent[county == "TOTAL"],
                                      NA)
    
  WI[WI$type == 2,]$returned[i] <- ifelse(length(returned),
                                      returned[county == "TOTAL"],
                                      NA)
  
  WI[WI$type == 2,]$in_person[i] <- ifelse(length(in_person),
                                      in_person[county == "TOTAL"],
                                      0)
}

# For some reason, WI in person votes read in as strings, LOOK INTO THIS
WI$in_person <- as.numeric(gsub( ",", "", WI$in_person))
WI$in_person[is.na(WI$in_person)] <- 0

# Make the year of everything 2024 
WI$date_for_graphing <- `year<-`(WI$date, 2024)

# Shift the 2020 points over by two so that its days before the election
WI$date_for_graphing[year(WI$date) == "2020"] <- 
  WI$date_for_graphing[year(WI$date) == "2020"] + 2

# Truncate dates to remove data entry errors
WI <- WI[WI$date_for_graphing >= as.Date("2024-09-16", "%Y-%m-%d") &
         WI$date_for_graphing <= Sys.Date() - 1,]

# Issued and returned includes in person so we subtract that out
WI$sent <- WI$sent - WI$in_person
WI$returned <- WI$returned - WI$in_person

# Plotting ---------------------------------------------------------------------

max_val <- max(WI$apps)
xlim_dates <- c(min(WI$date_for_graphing), max(WI$date_for_graphing))

basic_plot(title = "Wisconsin Absentee Ballot Status",
  xlim_dates,
  xlabel = "Days Before the Election",
  ylabel = "Cummulative Mail and Early Votes",
  y_tics = seq(0, 5000000, by = 500000),
  type = "early",
  state = "WI",
  max_val,
  days_before = TRUE,
  y_mil = TRUE)

# Per Samuel's request I've removed applications for the later plots as it
# seems to be quite simmilar to sent, uncomment this to see applications

# lines(WI$date_for_graphing[year(WI$date) == "2020"], 
#       WI$apps[year(WI$date) == "2020"],
#       col = alpha("#c0ba79", .75),
#       lwd = 2,
#       type = "o",
#       lty = 3,
#       pch = 16)

# lines(WI$date_for_graphing[year(WI$date) == "2024"], 
#       WI$apps[year(WI$date) == "2024"],
#       col = alpha("#c0ba79", .75),
#       lwd = 2,
#       type = "o",
#       pch = 15)

# The points commented out as in later weeks they make it difficult to see which
# lines are dashed and which are solid

lines(WI$date_for_graphing[year(WI$date) == "2020"], 
      WI$in_person[year(WI$date) == "2020"],
      col = alpha("#948de5", .75),
      lwd = 2,
      # type = "o",
      lty = 3,
      pch = 15)

lines(WI$date_for_graphing[year(WI$date) == "2024"], 
      WI$in_person[year(WI$date) == "2024"],
      col = alpha("#948de5", .75),
      lwd = 2,
      # type = "o",
      pch = 15)

lines(WI$date_for_graphing[year(WI$date) == "2020"], 
      WI$sent[year(WI$date) == "2020"],
      col = alpha("#c0ba79", .75),
      lwd = 2,
      # type = "o",
      lty = 3,
      pch = 16)

lines(WI$date_for_graphing[year(WI$date) == "2020"], 
      WI$returned[year(WI$date) == "2020"],
      col = alpha("#37C256", .75),
      lwd = 2,
      # type = "o",
      lty = 3,
      pch = 16)

lines(WI$date_for_graphing[year(WI$date) == "2024"], 
      WI$sent[year(WI$date) == "2024"],
      col = alpha("#c0ba79", .75),
      lwd = 2,
      # type = "o",
      pch = 15)

lines(WI$date_for_graphing[year(WI$date) == "2024"], 
      WI$returned[year(WI$date) == "2024"],
      col = alpha("#37C256", .75),
      lwd = 2,
      # type = "o",
      pch = 15)


rect(xleft = xlim_dates[1],
      xright = xlim_dates[1] +
      as.numeric((xlim_dates[2] - xlim_dates[1])) / 3.5,
      ytop = max_val * 1.22, 
      ybottom = max_val * 1.05, 
      col = 'white')
legend("topleft", 
      inset = c(0, -0.06), 
      legend = c("Issued"),
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
legend("topleft", 
      inset = c(0, 0.02), 
      legend = c("In Person"),
      col = c("#948de5"), 
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
  inset=c(.28,-.06), 
  legend=c("2024"),
  lty = 1, 
  seg.len = 0.8,
  text.width = 2, 
  bty = 'n', 
  lwd = 2,
  cex = 2,
  # pt.cex = 1,
  # pch = 15
  )
legend("topleft",
  inset=c(.28,-.02), 
  legend=c("2020"),
  lty = 3, 
  seg.len = 0.8,
  text.width = 2, 
  bty = 'n', 
  lwd = 2,
  cex = 2,
  # pt.cex = 1,
  # pch = 16
  )

text(xlim_dates[2], 
  tail(WI$returned[year(WI$date) == "2020"], 1), 
  paste0(signif(tail(WI$returned[year(WI$date) == "2020"], 1) / 
    tail(WI$sent[year(WI$date) == "2020"], 1) * 100, 2), "%"), 
  cex = 1.5,
  pos = 4)

text(xlim_dates[2], 
  tail(WI$returned[year(WI$date) == "2024"], 1), 
  paste0(signif(tail(WI$returned[year(WI$date) == "2024"], 1) / 
    tail(WI$sent[year(WI$date) == "2024"], 1) * 100, 2), "%"), 
  cex = 1.5,
  pos = 4)

mtext("(Sep 16 2024/",
        side = 1, 
        cex  = 1.5, 
        at = xlim_dates[1], 
        line = 1.6)
mtext("Sep 14 2020)",
side = 1, 
cex  = 1.5, 
at = xlim_dates[1], 
line = 2.0)

mtext("For each year, labels show percent of ballots",
        side = 1, 
        cex  = 1.5, 
        at = xlim_dates[2] - as.numeric((xlim_dates[2] - xlim_dates[1])) / 4, 
        line = 4, 
        adj = 0)
mtext('issued in that year which have been returned', 
        side = 1, 
        line = 4.5, 
        cex = 1.5, 
        at =  xlim_dates[2] - as.numeric((xlim_dates[2] - xlim_dates[1])) / 4, 
        adj = 0)


add_std_margin_text(
  'Data Source: Wisconsin Elections Commission, elections.wi.gov', 
  xlim_dates,
  note_count = 0)

save_outputs(WI, "WI", "early")
