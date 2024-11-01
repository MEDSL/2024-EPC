##############################
## Mail Voting NV graphing
## Sina Shaikh
##############################

# Global -----------------------------------------------------------------------

calculate_sent <- function(date, party) {
  sum(as.Date(statewide_mail_2024$BALLOT_MAIL_DATE, "%m/%d/%Y") <= date &
        statewide_mail_2024$VOTER_REG_PARTY %in% party, na.rm = TRUE) +
  sum(as.Date(clark_mail_2024$BALLOT_MAIL_DATE, "%m/%d/%Y") <= date &
        clark_mail_2024$VOTER_REG_PARTY %in% party, na.rm = TRUE)
}

calculate_accepted <- function(date, party, status) {
  sum(as.Date(statewide_mail_2024$BALLOT_RECEIVE_DATE, "%m/%d/%Y") <= date &
        statewide_mail_2024$BALLOT_STATUS == status &
        statewide_mail_2024$VOTER_REG_PARTY %in% party, na.rm = TRUE) +
  sum(as.Date(clark_mail_2024$BALLOT_RECEIVE_DATE, "%m/%d/%Y") <= date &
        clark_mail_2024$BALLOT_STATUS == status &
        clark_mail_2024$VOTER_REG_PARTY %in% party, na.rm = TRUE)
}

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
setwd(A_PLACE_TO_STORE_DATA_FOR_THIS_STATE)

NV <- data.frame(
  date = seq(as.Date("20241005", "%Y%m%d"),
    Sys.Date() - 1,
    by = "1 day"),
  dem_sent = 0,
  rep_sent = 0,
  other_sent = 0,
  no_party_sent = 0,
  dem_acc = 0,
  rep_acc = 0,
  other_acc = 0,
  no_party_acc = 0
)


files <- list.files(pattern = "statewide")
statewide_mail_2024 <- read.csv(
  files[which.max(sub(".*?(2024\\d{4}).*", "\\1", files))])

print(files[which.max(sub(".*?(2024\\d{4}).*", "\\1", files))])

files <- list.files(pattern = "clark")
clark_mail_2024 <- read.csv(
  files[which.max(sub(".*?(2024\\d{4}).*", "\\1", files))])

print(files[which.max(sub(".*?(2024\\d{4}).*", "\\1", files))])

for (i in 1:nrow(NV)) {
  date <- NV$date[i]
  
  NV$dem_sent[i] <- calculate_sent(date, "DEM")
  NV$rep_sent[i] <- calculate_sent(date, "REP")
  NV$no_party_sent[i] <- calculate_sent(date, c("NP ", "NPP", "RLB"))
  NV$other_sent[i] <- calculate_sent(date, setdiff(unique(statewide_mail_2024$VOTER_REG_PARTY), c("REP", "DEM", "NP ", "NPP", "RLB")))

  NV$dem_acc[i] <- calculate_accepted(date, "DEM", "Accepted")
  NV$rep_acc[i] <- calculate_accepted(date, "REP", "Accepted")
  NV$no_party_acc[i] <- calculate_accepted(date, c("NP ", "NPP", "RLB"), "Accepted")
  NV$other_acc[i] <- calculate_accepted(date, setdiff(unique(statewide_mail_2024$VOTER_REG_PARTY), c("REP", "DEM", "NP ", "NPP", "RLB")), "Accepted")
}

max_val <- max(NV$dem_sent, NV$rep_sent)
xlim_dates <- c(min(NV$date), max(NV$date))

basic_plot(title = "Nevada Mail Ballot Status",
  xlim_dates,
  xlabel = "Days Before the Election",
  ylabel = "Ballots Issued and Accepted",
  y_tics = seq(0, 500000, by = 50000),
  type = "early",
  state = "NV",
  max_val,
  days_before = TRUE)

lines(NV$date, 
      NV$dem_sent,
      col = alpha("#3791ff", .8),
      lwd = 2,
      lty = 3,
      pch = 15)
lines(NV$date, 
      NV$rep_sent,
      col = alpha("#f6573e", .8),
      lwd = 2,
      lty = 3,
      pch = 15)
lines(NV$date, 
      NV$other_sent,
      col = alpha("#c0ba79", .8),
      lwd = 2,
      lty = 3,
      pch = 15)
lines(NV$date, 
      NV$no_party_sent,
      col = alpha("#948de5", .75),
      lwd = 2,
      lty = 3,
      pch = 15)

lines(NV$date, 
      NV$dem_acc,
      col = alpha("#3791ff", .8),
      lwd = 2,
      pch = 15)
lines(NV$date, 
      NV$rep_acc,
      col = alpha("#f6573e", .8),
      lwd = 2,
      pch = 15)
lines(NV$date, 
      NV$other_acc,
      col = alpha("#c0ba79", .8),
      lwd = 2,
      pch = 15)
lines(NV$date, 
      NV$no_party_acc,
      col = alpha("#948de5", .75),
      lwd = 2,
      pch = 15)


rect(xleft = xlim_dates[1],
      xright = xlim_dates[1] +
      as.numeric((xlim_dates[2] - xlim_dates[1])) / 3.5,
      ytop = max_val * 1.22, 
      ybottom = max_val * 1, 
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
legend("topleft", 
        inset = c(0, 0.06), 
        legend = c("No Party"),
        col = c("#948de5"), 
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
  legend=c("Issued"),
  lty = 1, 
  seg.len = 0.8,
  text.width = 2, 
  bty = 'n', 
  lwd = 2,
  cex = 2,
  )
legend("topleft",
  inset=c(.28,-.02), 
  legend=c("Accepted"),
  lty = 3, 
  seg.len = 0.8,
  text.width = 2, 
  bty = 'n', 
  lwd = 2,
  cex = 2,
  )

text(xlim_dates[2], 
  tail(NV$dem_acc, 1), 
  paste0(signif(tail(NV$dem_acc, 1) / 
    tail(NV$dem_sent, 1) * 100, 2), "%"), 
  cex = 1.5,
  pos = 4)

text(xlim_dates[2], 
  tail(NV$rep_acc, 1), 
  paste0(signif(tail(NV$rep_acc, 1) / 
    tail(NV$rep_sent, 1) * 100, 2), "%"), 
  cex = 1.5,
  pos = 4)

text(xlim_dates[2], 
  tail(NV$other_acc, 1), 
  paste0(signif(tail(NV$other_acc, 1) / 
    tail(NV$other_sent, 1) * 100, 2), "%"), 
  cex = 1.5,
  pos = 4)

text(xlim_dates[2], 
  tail(NV$no_party_acc, 1), 
  paste0(signif(tail(NV$no_party_acc, 1) / 
    tail(NV$no_party_sent, 1) * 100, 2), "%"), 
  cex = 1.5,
  pos = 4)

mtext("(Oct 5 2024/",
        side = 1, 
        cex  = 1.5, 
        at = xlim_dates[1], 
        line = 1.6)
mtext("Oct 3 2020)",
side = 1, 
cex  = 1.5, 
at = xlim_dates[1], 
line = 2.0)


add_std_margin_text(
  'Data Source: Nevada Secretary of State, nvsos.gov', 
  xlim_dates,
  note_count = 0)

save_outputs(NV, "NV", "early")
