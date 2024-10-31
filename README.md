~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~ The code in this repository supports the daily plots provided in the
~	2024 Stanford-MIT Elections Performance Central
~		On the web at: https://www.elexcentral.org/
~
~ The codebase was written in Cambridge, MA
~	between july 2024 and november 2024,
~	by tired researchers at the Massachusetts Institute of Technology
~	Election Data and Science Lab
~
~ Version history of this readme:
~	first drafted by sbaltz at mit on 28 october 2024
~	modified by sbaltz on 30 october 2024
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
WARNING
	This code will only work after some active and thoughtful modification!

	We do want to polish it and make it easy to run ... we just haven't yet.

	You should know that:
		- We have stripped the code of our personal file paths, so you will
		have to input your own file paths to run these scripts. The file
		path part of the code might now be better viewed as pseudocode,
		indicating the kind of file structure the scripts should be situated
		in

		- We have not supplied any raw datasets that are too big to easily
		share. You will either have to acquire those, or ask us for anything
		you can't acquire

		- Much of the code is set to automatically run from a specific 
		directory, which might require some setting up on your part

		-> **WE DO NOT GUARANTEE THE ACCURACY OF ALL RAW DATA** <-
	Only the plots are rigorously quality assured.
	Some data, including Florida county-level mail ballot data, may not update
	properly, and when that happens in the raw data, we may choose to only
	correct the portions which are necessary for plotting. Please use
	caution with our raw files, and when in doubt, consult
	the official records from the relevant government office. Or ask us!


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PURPOSE OF THE REPOSITORY
	The repository contains three types of code and two types of data.

	*Scrapers
		These scripts collect three types of information from state	websites:
		Mail-in ballot information, in-person early voting information, and
		voter registration information. They run either weekly or daily. We
		run one batch early every morning and one batch later every morning,
		depending on when states tend to update the relevant data source. The
		scrapers are written to be respectful of state's resources, and only
		ask the server to send us information that we absolutely need, as
		infrequently as possible. These scrapers are all written in Python.
	*Bash scripts
		These .sh files call the scrapers all at once, in batches organized by
		how often the scraper should be run. In our practice we added each bash
		file to one user's crontab to run the files at the appropriate times
		and frequencies.
	*Plotters
		Once we collect the raw data, we turn it into a plot. The plotters are
		semi-standardized, but some are written in R and others in Python.
	*Raw data
		We save the raw data that we collect from states, which we translate
		into the data that goes directly into the plots.
	*Plot data
		We have provided in this repository the exact datapoints behind our
		plots. These are produced as a biproduct of the plotter scripts,
		alongside the actual image. In this release we only provide the most
		recent plot_data file, but each plot has a plot_data associated with it
		which is generated automatically when the corresponding plotter is run.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
STRUCTURE OF THE REPOSITORY
	scrapers
		|____*.sh: files that call scrapers, with names describing when to run
		|____*.py: the scrapers that collect data from states' websites
	plotters
		|___early
			|___FOO: a state's folder, using official 2-letter abbreviations
				|___plot_FOO.[R/py]: the script that produces a plot
				|___date.png: one example plot from a recent day
				|___raw
					|___*.csv: the raw data files
				|___plot_data
					|___[date].cvs: the data for the plot made on [date]
		|____reg
			|___[... same structure as early ^]


	The `early` folder holds data for mail-in ballots and in-person early
	voting. The `reg` folder handles voter registration information.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	In this release, the following 26 state-data combinations are covered:
		- FL mail-in voting
		- GA mail-in voting
		- NC mail-in voting
		- NV mail-in voting
		- TX mail-in voting
		- WI mail-in voting
		- PA mail-in voting
		- FL early in-person voting
		- GA early in-person voting
		- NC early in-person voting
		- NV early in-person voting
		- TX early in-person voting
		- WI early in-person voting
		- AZ voter registrations
		- FL voter registrations
		- GA voter registrations
		- MI voter registrations
		- MN voter registrations
		- MT voter registrations
		- NC voter registrations
		- NE voter registrations
		- NV voter registrations
		- PA voter registrations
		- SC voter registrations
		- TX voter registrations
		- WI voter registrations