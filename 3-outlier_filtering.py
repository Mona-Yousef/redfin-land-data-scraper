import csv
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Function to extract numeric values as float and remove text
def extract_numeric(text):
    numeric_values = re.findall(r'\d+\.\d+', text)  # Extract numeric values, including decimals
    return float(numeric_values[0]) if numeric_values else 0.0


# Function to extract numeric part from price text
def extract_price_numeric(price_text):
    numeric_values = re.findall(r'[0-9,]+', price_text)  # Extract numeric values with commas
    numeric_part = "".join(numeric_values).replace(",", "")  # Remove commas
    return float(numeric_part) if numeric_part else 0.0


# Function to calculate price per acre
def calculate_price_per_acre(price, acres):
    if acres > 0:
        return price / acres
    else:
        return 0.0


# Function to scrape data from a URL
def scrape_data(url):
    # Set up the Chrome WebDriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    # Specify the path to the directory containing chromedriver.exe
    chromedriver_path = "C:/Users/Mona/.cache/selenium/chromedriver/win64/119.0.6045.105/chromedriver.exe"

    # Set the PATH environment variable to include the chromedriver directory
    os.environ['PATH'] += os.pathsep + chromedriver_path
    options = Options()
    # options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'collapsedListView'))).text
        print(f"Processing: {title}")

        nearby_views_class = None
        try:
            nearby_views_class = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'NearbyViews')))
        except TimeoutException:
            pass  # Element not found within the specified timeout

        if nearby_views_class:
            property_containers = nearby_views_class.find_elements(By.CLASS_NAME, 'bottomV2')
        else:
            property_containers = driver.find_elements(By.CLASS_NAME, 'bottomV2')

        properties = []

        for container in property_containers:
            price_element = container.find_element(By.CLASS_NAME, 'homecardV2Price')
            acres_element = container.find_elements(By.CLASS_NAME, 'stats')[-1]

            if price_element and acres_element:
                price = price_element.text
                acres = acres_element.text

                acres_numeric = extract_numeric(acres)
                price_numeric = extract_price_numeric(price)
                price_per_acre = calculate_price_per_acre(price_numeric, acres_numeric)

                properties.append({'Price': price_numeric, 'Acres': acres_numeric, 'Price Per Acre': price_per_acre})

        sold_in_1y_text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'homes.summary'))).text
        sold_in_1y = sold_in_1y_text

        return {'Title': title, 'Sold in 1 Year': sold_in_1y, 'Properties': properties}

# Read URLs from input CSV and scrape data
input_filename = 'Keywords.csv'
output_filename = 'return.csv'

with open(input_filename, 'r') as input_csv, open(output_filename, 'w', newline='') as output_csv:
    reader = csv.reader(input_csv)
    next(reader)  # Skip the header row if it exists

    writer = csv.DictWriter(output_csv, fieldnames=['Title', 'Sold in 1 Year', 'Price', 'Acres', 'Price Per Acre'])
    writer.writeheader()

    for row in reader:
        url = row[6]
        data = scrape_data(url)

        for property_info in data['Properties']:
            writer.writerow({
                'Title': data['Title'],
                'Sold in 1 Year': data['Sold in 1 Year'],
                'Price': property_info['Price'],
                'Acres': property_info['Acres'],
                'Price Per Acre': property_info['Price Per Acre']
            })
