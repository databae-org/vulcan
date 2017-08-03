# A script to scrape Donald Trump rally attendance from Wikipedia. trumprallies_process.R will process and graph this data.
# Written by David H. Montgomery at SRCCON 2017
# MIT License

library(rvest)
library(jsonlite)
library(stringr)
library(tidyverse)
library(lubridate)
library(scales)

# Scrape the data from two Wikipedia pages 

url <- "https://en.wikipedia.org/wiki/List_of_rallies_for_the_Donald_Trump_presidential_campaign,_2016" # Save the first URL
# Scrape the first table
trump <- url %>% # Load the URL
	read_html() %>% # Read the HTML
	html_nodes(xpath='//*[@id="mw-content-text"]/div/table[2]') %>% # Point to the right table on the page via its xpath ID
	html_table(fill = TRUE) # Fill out any missing cells
trump <- trump[[1]] # Get it into the right format
trump$period <- "Primary" # Label this as Primary rallies

# Scrape the second table, as above
trump2 <- url %>%
	read_html() %>%
	html_nodes(xpath='//*[@id="mw-content-text"]/div/table[3]') %>%
	html_table(fill = TRUE)
trump2 <- trump2[[1]]
trump2$period <- "General"

# Scrape the third table, from the second page
url <- "https://en.wikipedia.org/wiki/List_of_post_election_Donald_Trump_rallies"
trump3 <- url %>%
	read_html() %>%
	html_nodes(xpath='//*[@id="mw-content-text"]/div/table[2]') %>%
	html_table(fill = TRUE)
trump3 <- trump3[[1]]
trump3$period <- "Postelex"

# Scrape the fourth table
trump4 <- url %>%
	read_html() %>%
	html_nodes(xpath='//*[@id="mw-content-text"]/div/table[3]') %>%
	html_table(fill = TRUE)
trump4 <- trump4[[1]]
trump4$period <- "Presidency"

# Combine all four tables into a single data frame.
trump_all <- rbind(trump, trump2, trump3, trump4) %>% select(-Source)
