## README

The goal of this project is to scrape amazon in order to figure out how to maximize product sales by tweaking various parameters of the seller page.  The files contained in this repo are as follows:

1. AmazonScraper.py
2. Process_Data_vn.ipynb
3. code_file_name (place_codes.csv)
4. url_data.pkl
5. luther.py
6. diagnostic_plots.py
7. cache
8  ENV
9.  This README.md

The contents are as follows.

### I. AmazonScraper

This first looks for the file 'url_data.pkl' and then proceeds to scrape the contents of the urls contained in the .pkl file.  If that file is empty, the code will automatically generate the urls from some hard-coded Amazon directories and then save the resulting urls to 'url_data.pkl'.  T

After generating the list of relevant urls, the scaper will go through them in a randomized order.  (The order is randomized once, but then fixed afterwards.)  Every 100 pages the data is cached in 'cache' and then the IP is changed randomly.  The choice of IP address is determined by feeding the VPN a city code.  These city codes are stored in 'place_codes.csv' and 'place_codes'.  The files are esentially redundant.  

The end result of the scraper file is to produce a function 'build_df()' or 'clean_df()' which produces a dataframe from the scraped data.  This function can be called from the 'Process_Data' notebooks.

### II. Process_Data_vn.ipynb

These are various phases of data processing.  They all read in teh output of 'AmazonScraper'.  

### III.  code_file_name.

City codes used by the VPN.

### IV.  url_data.pkl

This just stores a list of urls for individual items.

### V.  luther.py

A few helper functions for the Process_Data files.

### VI.  diagnostic_plots.py

Some useful plotting functions.

### VII. cache

Where the data is stored.

### VIII.  ENV

Some environment variables are stored here occasionally.

### IX.  README.md

I'm hoping this one is self-explanatory.
