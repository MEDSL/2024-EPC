################################################################################
## Voter Registration PA graphing
## Sina Shaikh
################################################################################

# Helper file used for all plotting
source(paste0(A_PLACE_TO_STORE_HELPER_FILES,"plotting_helpers.R"))

# Packages ---------------------------------------------------------------------

packages <- c("data.table", 
  "lubridate", 
  "showtext", 
  "readxl", 
  "dplyr", 
  "scales")
custom_library_load(packages)

# Analysis ---------------------------------------------------------------------

setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

PA <- data.frame(
  date = sub('\\.xls$', '', list.files(path = ".")),
  total = 0,
  dem = 0,
  rep = 0
)

# Iterate through files
for (i in 1:length(list.files(path ="."))){
  
  # Read in data
  total <- data.frame(read_excel(list.files(path =".")[i],
    sheet = "All by Age"))
  dem <- data.frame(read_excel(list.files(path =".")[i], sheet = "Dem by Age"))
  rep <- data.frame(read_excel(list.files(path =".")[i], sheet = "Rep by Age"))
  
  PA$total[i] <- total[total$County == "Grand Total:", ][3,2]
  PA$dem[i] <- dem[dem$County == "Grand Total:", ][4,3]
  PA$rep[i] <- rep[rep$County == "Grand Total:", ][3,3]
  
}

# PA updates don't always come out on the same date so we check to see when
# the data has changed from the day before
PA_diff <- PA[c(TRUE, diff(PA$total) != 0), ]
PA_diff$date <- as.Date(PA_diff$date, "%Y%m%d")
PA_change <- PA_diff

# We want change from the last new data
for (i in 2:nrow(PA_diff)){
  PA_change[-1][i,] <- PA_diff[-1][i,] - PA_diff[-1][(i-1),]
}
PA_change <- PA_change[-1,]

# Calculate other
PA_change$other <- PA_change$total - PA_change$dem - PA_change$rep

# We truncate the dates so that they show up on the Monday of the week they are
# released because that's the date listed in the file but the file is not
# actually always uploaded then
PA_change$date <- floor_date(PA_change$date, "weeks", week_start = 1)

# Plotting ---------------------------------------------------------------------


max_val <- max(PA_change$dem, PA_change$rep, PA_change$other)
min_val <- min(PA_change$dem, PA_change$rep, PA_change$other)
xlim_dates <- c(min(PA_change$date), max(PA_change$date))

basic_plot(title = "Pennsylvania Voter Registration",
  xlim_dates,
  xlabel = "Data as of",
  ylabel = "Net Change in Registration From Week Prior",
  y_tics = seq(-20000, 200000, by = 5000),
  type = "reg",
  state = "PA",
  max_val,
  min_val)

lines(PA_change$date, 
      PA_change$other,
      col = alpha("#c0ba79", .8),
      lwd = 2,
      type = "o")

lines(PA_change$date, 
      PA_change$rep,
      col = alpha("#f6573e", .8),
      lwd = 2,
      type = "o")

lines(PA_change$date, 
      PA_change$dem,
      col = alpha("#3791ff", .8),
      lwd = 2,
      type = "o")

add_party_legend(xlim_dates, max_val, min_val * 1.2)

add_std_margin_text(
  'Data Source: Pennsylvania Department of State, pa.gov', 
  xlim_dates,
  note_count = 0)

mtext('Note: Y-axis represents the week over week change',
  side = 1, 
  cex  = 1.8, 
  at = Sys.Date() - 1, 
  line = 4.25, 
  adj = 1)

save_outputs(PA_change, "PA", "reg")
