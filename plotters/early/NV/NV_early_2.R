##############################
## Early in Person Voting NV graphing
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
  "scales",
  "data.table")
custom_library_load(packages)


# Analysis ---------------------------------------------------------------------

NV_mail_2024 <- read.csv(paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,"early_2024.csv"))
NV_mail_2020 <- read.csv(paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,"early_2020.csv"))

NV_mail_2024$Date <- as.Date(as.character(NV_mail_2024$Date), "%Y%m%d")
NV_mail_2020$Date <- as.Date(as.character(NV_mail_2020$Date), "%Y%m%d") + 2
year(NV_mail_2020$Date) <- 2024

NV_mail_2024 <- NV_mail_2024[NV_mail_2024$Date <= Sys.Date() - 1, ]
NV_mail_2020 <- NV_mail_2020[NV_mail_2020$Date <= Sys.Date() - 1, ]

for (i in 2:nrow(NV_mail_2020)){
    NV_mail_2020[i, 3:6] <- NV_mail_2020[i, 3:6] + NV_mail_2020[i - 1, 3:6]
}
for (i in 2:nrow(NV_mail_2024)){
    NV_mail_2024[i, 3:6] <- NV_mail_2024[i, 3:6] + NV_mail_2024[i - 1, 3:6]
}



# Plotting ---------------------------------------------------------------------



max_val <- max(NV_mail_2024$Dem, 
    NV_mail_2024$Rep, 
    NV_mail_2020$Dem, 
    NV_mail_2020$Rep)
xlim_dates <- c(min(NV_mail_2024$Date), max(NV_mail_2024$Date))

basic_plot(title = "Nevada Early Voting",
  xlim_dates,
  xlabel = "Days Before the Election",
  ylabel = "Early Voters",
  y_tics = seq(0, 500000, by = 50000),
  type = "early",
  state = "NV",
  alt = "ev",
  max_val,
  days_before = TRUE)

lines(NV_mail_2020$Date, 
      NV_mail_2020$Dem,
      col = alpha("#3791ff", .8),
      lwd = 2,
      lty = 3,
      pch = 15)
lines(NV_mail_2020$Date, 
      NV_mail_2020$Rep,
      col = alpha("#f6573e", .8),
      lwd = 2,
      lty = 3,
      pch = 15)
lines(NV_mail_2020$Date, 
      NV_mail_2020$Other,
      col = alpha("#c0ba79", .8),
      lwd = 2,
      lty = 3,
      pch = 15)

lines(NV_mail_2024$Date, 
      NV_mail_2024$Dem,
      col = alpha("#3791ff", .8),
      lwd = 2,
      pch = 15)
lines(NV_mail_2024$Date, 
      NV_mail_2024$Rep,
      col = alpha("#f6573e", .8),
      lwd = 2,
      pch = 15)
lines(NV_mail_2024$Date, 
      NV_mail_2024$Other,
      col = alpha("#c0ba79", .8),
      lwd = 2,
      pch = 15)



rect(xleft = xlim_dates[1],
      xright = xlim_dates[1] +
      as.numeric((xlim_dates[2] - xlim_dates[1])) / 3.5,
      ytop = max_val * 1.22, 
      ybottom = max_val * 1.05, 
      col = 'white')
legend("topleft",
        inset = c(0, -0.06), 
        legend = c("Republican"),
        col = c("#f6573e"), 
        lty = 1, 
        cex = 2, 
        seg.len = 0.8,
        text.width = 2, 
        bty = 'n', 
        lwd = 2)
legend("topleft", 
        inset = c(0, -0.02), 
        legend = c("Democrat"),
        col = c("#3791ff"), 
        lty = 1, 
        cex = 2, 
        seg.len = 0.8,
        text.width = 2, 
        bty = 'n', 
        lwd = 2)
legend("topleft", 
        inset = c(0, 0.02), 
        legend = c("Other"),
        col = c("#c0ba79"), 
        lty = 1, 
        cex = 2, 
        seg.len = 0.8,
        text.width = 2, 
        bty = 'n', 
        lwd = 2)


rect(xleft = xlim_dates[1] + as.numeric((xlim_dates[2] - xlim_dates[1])) / 3.3,
    xright = xlim_dates[1] + as.numeric((xlim_dates[2] - xlim_dates[1])) / 1.75,
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
  )


mtext("(Oct 19 2024/",
        side = 1, 
        cex  = 1.5, 
        at = xlim_dates[1], 
        line = 1.6)
mtext("Oct 17 2020)",
side = 1, 
cex  = 1.5, 
at = xlim_dates[1], 
line = 2.0)


add_std_margin_text(
  'Data Source: Nevada Secretary of State, nvsos.gov', 
  xlim_dates,
  note_count = 0)

dev.off()
  # Save graphing data
  write.csv(NV_mail_2020, 
    file = paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,
        format(Sys.time(), "%Y%m%d"),
        "_NV_early_2020.csv"),
    row.names = FALSE)

  write.csv(NV_mail_2020, 
    file = paste0(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE,
        format(Sys.time(), "%Y%m%d"),
        "_NV_early_2024.csv"),
    row.names = FALSE)

  # Ensure that Rplots.pdf is not created
  pdf(NULL)
