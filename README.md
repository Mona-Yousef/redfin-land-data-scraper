# Redfin Land Data Scraper

This project contains Python scripts used to extract, clean, and analyze real estate land pricing data from Redfin for research and visualization purposes.

## 🧩 Project Overview
The workflow automates the following steps:
1. Generate property listing URLs for each U.S. county keyword using Selenium automation.
2. Scrape detailed listing data (price, acres, and price per acre) from Redfin using Selenium.
3. Filter outliers and retain valid property records using percentile-based trimming.
4. Analyze price variability to assess market homogeneity, using median, mean, and coefficient of variation metrics.

## 📂 Scripts
| File | Description |
|------|--------------|
| `1-url_generator.py` | Builds Redfin search URLs for multiple regions or keywords |
| `2-redfin_scraper.py` | Extracts property data (price, location, acres, etc.) into CSV |
| `3-outlier_filtering.py` | Removes extreme high/low price-per-acre values |
| `4-price_variability_analysis.py` | Calculates median, mean, and coefficient of variation per title |

## ⚙️ Technologies Used
- Python
- Pandas
- BeautifulSoup
- Selenium automation
- Requests
- OpenPyXL (for Excel output)

## ⚠️ Notes
These scripts were originally developed for educational and testing purposes to extract real estate data from Redfin.
As Redfin’s website structure and CSS selectors frequently change, the current code may no longer function as intended without updates to the element locators or logic.
The repository remains for learning reference and demonstration of the web scraping workflow design.

