custom_library_load <- function(packages) {
  # I use base R loading rather than librarian or pacman to avoid dependancies
  # and to manually specify default library path even though the syntax is messier
  .libPaths(new = [A_PLACE_TO_STORE_THE_LIBRARIES])
  
  installed_packages <- packages %in% rownames(installed.packages())
  if (any(installed_packages == FALSE)) {
    install.packages(packages[!installed_packages])
  }
  
  invisible(lapply(packages, library, character.only = TRUE))
}

add_party_legend <- function(xlim_dates, max_val, min_val = 0, note_count = 0) {
  # We add the legend manually piece by piece because running this code on the
  # server stretches the whitespace

  if (min_val == 0){
    y_lim_min = 0
  } else {
    y_lim_min = min_val - (max_val - min_val) * .2
  }

  y_lim_max = max_val + (max_val - min_val) * .2

  rect(xleft = xlim_dates[1],
       xright = xlim_dates[1] +
        as.numeric((xlim_dates[2] - xlim_dates[1])) / 3.5,
       ytop = y_lim_max + (y_lim_max - y_lim_min) * .01, 
       ybottom = y_lim_max - (y_lim_max - y_lim_min) / (7.8 - note_count*.8), 
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
}

add_std_margin_text <- function(text, xlim_dates, note_count = 0) {
  mtext(text,
        side = 1, 
        cex  = 1.5, 
        at = xlim_dates[1] - as.numeric((xlim_dates[2] - xlim_dates[1])) / 6, 
        line = 4 + 2.2 * note_count, 
        adj = 0)
  mtext('Graph Source: MIT Election Data and Science Lab, @MITelectionlab', 
        side = 1, 
        line = 4.5 + 2.2 * note_count, 
        cex = 1.5, 
        at = xlim_dates[1] - as.numeric((xlim_dates[2] - xlim_dates[1])) / 6, 
        adj = 0)
}

save_outputs <- function(data, state, type) {
  dev.off()
  # Save graphing data
  write.csv(data, 
    file = paste0(A_PLACE_TO_SAVE_THE_DATA,
        format(Sys.time(), "%Y%m%d"),
        "_",
        state, 
        "_",
        type,
        ".csv"),
    row.names = FALSE)

  # Ensure that Rplots.pdf is not created
  pdf(NULL)
}


basic_plot <- function(title,
  xlim_dates, 
  xlabel, 
  ylabel, 
  y_tics,
  type, 
  state,
  max_val,
  alt = "",
  days_before = FALSE,
  min_val = 0, 
  note_count = 0,
  y_mil = FALSE) {

  # Note 1.19 by 1 aspect ratio
  png(paste0(A_PLACE_TO_SAVE_THE_FIGURES
             format(Sys.time(), "%Y%m%d"),
             ".png"), 
      pointsize = 7,
      width = 1190,
      height = 1000,
      res = 300)
  
  font_add(THE_FONT_TO_USE)
  showtext_auto()
  par(family = "styrene", mar = c(6.0 + 2 * note_count, 4.1, 4.1, 2.1))
  
  if (min_val == 0){
    y_lim_min = 0
  } else {
    y_lim_min = min_val - (max_val - min_val) * .2
  }

  plot(NULL,
    main = paste0(title,
      ", ",
      format(Sys.time(), 
      "%m/%d/%Y")),
    xlim = c(xlim_dates[1], 
      xlim_dates[2] + as.numeric((xlim_dates[2] - xlim_dates[1]) / 25)),
    ylim = c(y_lim_min, max_val + (max_val - min_val) * .2),
    xlab = xlabel,
    ylab = ylabel,
    pch = 19,
    cex.main = 4,
    cex.lab = 3.5,
    cex.axis = 2,
    xaxt = "n",
    yaxt = "n")


  # Automatically set tics
  x_tics <- c()
  if(length(seq(xlim_dates[1], xlim_dates[2], by = "1 week")) <= 3){
    x_tics <- seq(xlim_dates[1], xlim_dates[2], by = "1 day")
  } else if(length(seq(xlim_dates[1], xlim_dates[2], by = "1 week")) <= 8){
    x_tics <- seq(xlim_dates[1], xlim_dates[2], by = "1 week")
  } else if(length(seq(xlim_dates[1], xlim_dates[2], by = "1 week")) <=16){
    x_tics <- seq(xlim_dates[1], xlim_dates[2], by = "2 weeks")
  } else {
    x_tics <- seq(xlim_dates[1], xlim_dates[2], by = "1 month")
  }

  if(!days_before){
    axis.Date(1, at = x_tics, format = "%b %d", cex.axis = 2)
  } else{
    if(as.Date("20241105", "%Y%m%d") %in% seq(xlim_dates[2], xlim_dates[1], by = "-1 week")){
      x_tics <- rev(seq(xlim_dates[2], xlim_dates[1], by = "-1 week"))
      axis.Date(1, 
        at = x_tics, 
        labels = as.Date("20241105", "%Y%m%d") - x_tics, 
        cex.axis = 2)
    } else {
      axis.Date(1, 
        at = x_tics, 
        labels = as.Date("20241105", "%Y%m%d") - x_tics, 
        cex.axis = 2)
    }

  }

  if(!y_mil){
    axis(2,
    at = y_tics, 
    labels = formatC(y_tics, 
      format ="d", 
      big.mark = ","), 
    cex.axis = 2)
  } else {
    axis(2,
    at = y_tics, 
    labels = c(0, paste0(seq(.5, 20, .5), "M"))[1:length(y_tics)], 
    cex.axis = 2)
  }
  

  abline(h = y_tics, tck = 1, lwd = .5, col = alpha("gray", .75))

  if(!days_before){
    abline(v = x_tics,
      tck = 1, 
      lwd = .5, 
      col = alpha("gray", .75))
  } else {
    abline(v = x_tics,
      tck = 1, 
      lwd = .5, 
      col = alpha("gray", .75))
  }

}