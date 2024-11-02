################################################################################
# Voter Registration NC graphing
# Sina Shaikh
################################################################################

# The codebook for NC can be found at:
# https://s3.amazonaws.com/dl.ncsbe.gov/data/layout_ncvoter.txt

# Helper file used for all plotting
source(paste0(A_PLACE_TO_STORE_HELPER_FILES,"/plotting_helpers.R"))

# Packages ---------------------------------------------------------------------

packages <- c("data.table", "lubridate", "showtext")
custom_library_load(packages)

# 2024 Analysis ----------------------------------------------------------------

setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

# File comes zipped
zipped <- list.files(path = '.', pattern = 'zip')
while (length(zipped) != 0) {
	unzip(zipped[1])
	file.rename("ncvoter_Statewide.txt",
    paste0(sub('\\.zip', '', zipped[1]),
    ".txt"))
	file.remove(zipped[1])
}

# We truncate dates as most recent data is not fully up to date. There is no
# guarantee that data will remain stable after 2 weeks. We start at second 
# Friday in the data so we can do week on week change for weeks ending on Friday
NC <- data.frame(
  date = format(seq(as.Date("20240705", "%Y%m%d"),
    Sys.Date() - 14,
    by = "1 week"), "%Y%m%d"),
  total = 0,
  dem = 0,
  rep = 0,
  total_2020 = 0,
  dem_2020 = 0,
  rep_2020 = 0
)

NC_date <- data.frame(
  fread(sort(list.files(path ="."))[length(list.files(path ="."))], sep='\t'))


# Subset to Active and Temporary Status codes
NC_date <- NC_date[NC_date$status_cd %in% c("A", "S"),]


for (i in 1:length(NC$date)) {
  temp <- NC_date[as.Date(NC_date$registr_dt, "%m/%d/%Y") >
    (as.Date(NC$date[i], "%Y%m%d")-7) & 
    as.Date(NC_date$registr_dt, "%m/%d/%Y") <=
    (as.Date(NC$date[i], "%Y%m%d")),]
  
  temp <- na.omit(temp)
    
  NC$total[i] <- nrow(temp)
  NC$dem[i] <- table(temp$party_cd)["DEM"]
  NC$rep[i] <- table(temp$party_cd)["REP"]
}
NC$other <- NC$total - NC$dem - NC$rep


print("First file loaded and processed")

write.csv(NC, 
    file = paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,
        format(Sys.time(), "%Y%m%d"),
        "_NC_reg.csv"),
    row.names = FALSE)

rm(NC_date)
rm(temp)


# 2020 Analysis ----------------------------------------------------------------

NC <- read.csv(paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,
        format(Sys.time(), "%Y%m%d"),
        "_NC_reg.csv"))

setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)
NC_date_2020 <- read.csv("VR_Snapshot_20201103.txt", 
  sep='\t',
  quote = "", 
  fileEncoding = "UTF-16",
  colClasses = c(rep("NULL", 5), 
    NA, 
    rep("NULL", 33), 
    NA, 
    rep("NULL", 5), 
    NA,
    rep("NULL", 44)))
NC_date_2020 <- NC_date_2020[NC_date_2020$stats_cd %in% c("ACTIVE", "TEMPORARY")]

# Modify the 2020 dates
NC_date_2020$registr_dt <- as.Date(NC_date_2020$registr_dt, "%m/%d/%Y")
NC_date_2020 <- NC_date_2020[year(NC_date_2020$registr_dt) == 2020,]
NC_date_2020$registr_dt <- `year<-`(NC_date_2020$registr_dt, 2024)
NC_date_2020$registr_dt <- NC_date_2020$registr_dt + 2


for (i in 1:length(NC$date)) {
  temp <- NC_date_2020[NC_date_2020$registr_dt >
    (as.Date(NC$date[i], "%Y%m%d")-7) & 
    NC_date_2020$registr_dt <=
    (as.Date(NC$date[i], "%Y%m%d")),]
  
  temp <- na.omit(temp)
    
  NC$total_2020[i] <- nrow(temp)
  NC$dem_2020[i] <- table(temp$party_cd)["DEM"]
  NC$rep_2020[i] <- table(temp$party_cd)["REP"]
}


NC$other_2020 <- NC$total_2020 - NC$dem_2020 - NC$rep_2020

write.csv(NC, 
    file = paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,
        format(Sys.time(), "%Y%m%d"),
        "_NC_reg.csv"),
row.names = FALSE)

# Plotting ---------------------------------------------------------------------

NC <- read.csv(paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,
        format(Sys.time(), "%Y%m%d"),
        "_NC_reg.csv"))
NC$date <- as.Date(NC$date, "%Y%m%d")

xlim_dates <- as.Date(c(min(NC$date), max(NC$date)), "%Y%m%d")
max_val <- max(NC$other, NC$rep, NC$dem, NC$other_2020, NC$rep_2020, NC$dem_2020)

basic_plot(title = "North Carolina Voter Registration",
  xlim_dates,
  xlabel = "Week Ending Friday",
  ylabel = "New Registrants",
  y_tics = seq(0, 50000, by = 5000),
  type = "reg",
  state = "NC",
  max_val,
  note_count = 1)

lines(NC$date, 
      NC$other,
      col = "#c0ba79",
      lwd = 2,
      type = "o")
lines(NC$date, 
      NC$rep,
      col = "#f6573e",
      lwd = 2,
      type = "o")
lines(NC$date, 
      NC$dem,
      col = "#3791ff",
      lwd = 2,
      type = "o")

lines(NC$date, 
      NC$other_2020,
      col = "#c0ba79",
      lwd = 2,
      type = "o")
lines(NC$date, 
      NC$rep_2020,
      col = "#f6573e",
      lwd = 2,
      type = "o")
lines(NC$date, 
      NC$dem_2020,
      col = "#3791ff",
      lwd = 2,
      type = "o")


add_party_legend(xlim_dates, max_val, note_count = 1)

mtext('Note: The data points for the last week shown may appear artificially low and may rise as more voter registrations', 
  side = 1, 
  cex  = 1.8, 
  at = xlim_dates[1] - as.numeric((xlim_dates[2] - xlim_dates[1])) / 6, 
  line = 4.5, 
  adj = 0)
mtext('from that week are processed. See https://www.elexcentral.org/state-updates/north-carolina for details', 
  side = 1, 
  line  = 5.2, 
  cex = 1.8, 
  at = xlim_dates[1] - as.numeric((xlim_dates[2] - xlim_dates[1])) / 6, 
  adj = 0)

add_std_margin_text(
  'Data Source: North Carolina State Board of Elections, ncsbe.gov', 
  xlim_dates,
  note_count = 1)

save_outputs(NC, "NC", "reg")
