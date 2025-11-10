'''
"Keyword file - output_data file"
This code is taking the URLS of the for sale and sold houses in 1,3, and 6 months from the Keyword file and scraps
The number of houses for sale and sold for each period, and export data to the output file
'''



import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape data from a URL
def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find(class_='collapsedListView').text
    for_sale = soup.find(class_='homes summary').text
    return title, for_sale

# Read URLs from the modified CSV file and write scraped data to another CSV file
input_csv_file = 'Keywords.csv'  # Input CSV with URLs
output_csv_file = 'output_data.csv'  # Output CSV to store scraped data

with open(input_csv_file, 'r') as infile, open(output_csv_file, 'w', newline='') as outfile:
    csv_reader = csv.reader(infile)
    csv_writer = csv.writer(outfile)

    # Write header row for the output CSV
    csv_writer.writerow([
        'URL for sale', 'URL1mo', 'URL3mo', 'URL6mo', 'URL1yr', 'Title', 'for sale', 'sold 1mo', 'sold 3mo',
        'sold 6mo','sold 1yr'
    ])

    next(csv_reader)  # Skip header row if present
    for row in csv_reader:
        URLforsale, URL1mo, URL3mo, URL6mo,URL1yr = row[2],row[3],row[4],row[5],row[6]  #position of the URLs

        #Scrap data for URLforSale
        title, for_sale = scrape_data(URLforsale)

        # Scrape data for URL1m
        title, sold_1mo = scrape_data(URL1mo)

        # Scrape data for URL3m
        title, sold_3mo = scrape_data(URL3mo)

        # Scrape data for URL6m
        title, sold_6mo = scrape_data(URL6mo)

        # Scrape data for URL1yr
        title, sold_1yr = scrape_data(URL1yr)

        # Write the scraped data to the output CSV
        csv_writer.writerow([
            URLforsale, URL1mo, URL3mo, URL6mo,URL1yr, title, for_sale, sold_1mo, sold_3mo, sold_6mo, sold_1yr
        ])

        print(f"Scraped for sale and sold months data for : {title}")

print("Data scraping and storage complete.")
