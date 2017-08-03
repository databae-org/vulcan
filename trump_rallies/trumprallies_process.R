# Processes data on Trump rallies from Wikipedia, scraped by the trumprallies_scrape.R script.

library(rvest)
library(jsonlite)
library(stringr)
library(tidyverse)
library(lubridate)
library(scales)

# Clean up the Estimated Visitors column 
trump_all$`Estimated Visitors` <- str_replace_all(trump_all$`Estimated Visitors`,",","") # Remove commas
trump_all$`Estimated Visitors` <- str_replace_all(trump_all$`Estimated Visitors`,'"',"") # Remove quotes
trump_all$`Estimated Visitors` <- str_replace_all(trump_all$`Estimated Visitors`,"\\+","") # Remove +s
trump_all$`Estimated Visitors` <- str_replace_all(trump_all$`Estimated Visitors`," or less","") # Remove "or less"
trump_all$`Estimated Visitors` <- str_replace_all(trump_all$`Estimated Visitors`," plus 000s","") # Remove "plus 000s"
trump_all$`Estimated Visitors` <- str_replace_all(trump_all$`Estimated Visitors`,">","") # Remove ">"
trump_all$`Estimated Visitors` <- str_replace_all(trump_all$`Estimated Visitors`, "\\[[^\\]]*\\]", "") # Remove everything between brackets (Wikipedia notes)
trump_all$`Estimated Visitors` <- str_replace_all(trump_all$`Estimated Visitors`,"Thousands","2000") # Several entries list attendance as "thousands". I input 2000 as a placeholder.

# Several rallies have ranges. Here, I split those ranges and pick the lower of two values. 
trump_all$`Estimated Visitors` <- str_split(trump_all$`Estimated Visitors`, "-", simplify = TRUE)[,1]
trump_all$`Estimated Visitors` <- str_split(trump_all$`Estimated Visitors`, "\n", simplify = TRUE)[,1]
trump_all$`Estimated Visitors`[302] <- 6000 # Hard-code one cell that didn't translate

# Convert the Estimated Visitors column into numeric form. This will zap any remaining strings into NAs
trump_all$`Estimated Visitors` <- as.numeric(trump_all$`Estimated Visitors`)

# Convert the date column into a date format
trump_all$`Date of Rally` <- as_date(trump_all$`Date of Rally`, format = "%A, %B %d, %Y") 

# Graph rally attendance over time
ggplot(trump_all, aes(`Date of Rally`, `Estimated Visitors`, color = period)) +
	geom_point() +
	#geom_vline(aes(xintercept = as.numeric(as.Date("2016-11-08"))), color = "blue", linetype = 2) + 
	#geom_vline(aes(xintercept = as.numeric(as.Date("2016-05-26"))), color = "blue", linetype = 2) + 
	scale_y_continuous(labels = comma) +
	theme(text = element_text(size = 20)) +
	labs(title = "Donald Trump rallies and capacity size", 
		 subtitle = "Source: Wikipedia",
		 color = "Period")