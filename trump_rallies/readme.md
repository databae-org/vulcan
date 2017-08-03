# Scraping Trump rallies

Contains: 

- `trumprallies_scrape.R`: An R script to scrape data on Donald Trump rallies from Wikipedia
- `trump_rallies_raw.csv`: The output of `trumprallies_scrape.R`, an unprocessed spreadsheet from Wikipedia
- `trumprallies_process.R`: A second R script to clean and graph the output of `trumprallies_scrape.R`, `trump_rallies_raw.csv`
- `trump_rallies_clean.csv`: A processed spreadsheet of Trump rally data.

Note that the cleaning process makes several editorial decisions, including taking the lower number whenever a range of attendance was given, and interpreting attendance of "thousands" as "2,000" as a placeholder.

`trumprallies_process.R` will also create a chart in `ggplot`:

![](https://raw.githubusercontent.com/dhmontgomery/vulcan/master/trump_rallies/trumprallies.png)

Written by David H. Montgomery.
