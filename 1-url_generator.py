'''
"Keywod file - Keyword file"
That code is for extracting all the needed URLs of every county in the keyword file
'''

import os
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

# Set up ChromeOptions to enable incognito mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")


# Specify the path to the directory containing chromedriver.exe
chromedriver_path = "C:/Users/Mona/.cache/selenium/chromedriver/win64/119.0.6045.105"

# Set the PATH environment variable to include the chromedriver directory
os.environ['PATH'] += os.pathsep + chromedriver_path

# Define the URL of the website
url = "https://www.redfin.com/"

# Create a WebDriver instance with incognito mode
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the CSV file containing keywords
    with open('keywords.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        # Prepare a list to store rows with the additional columns
        updated_rows = []

        for row in reader:
            keyword = row['keyword']

            # Open the website in the browser
            driver.get(url)

            # Locate the search input and enter the keyword
            search_input = driver.find_element(By.NAME, "searchInputBox")
            search_input.send_keys(keyword)
            search_input.send_keys(Keys.RETURN)

            try:
                # Use WebDriverWait to wait for the URL to change
                wait = WebDriverWait(driver, 5)
                wait.until(EC.url_changes(url))

                # Get the current URL after the search
                base_url = driver.current_url

                # Print the resulting URL for the current keyword
                print(f"Keyword: {keyword}")
                print("Resulting URL:", base_url)
                print()

                # Concatenate the URLs for additional columns
                row['base url'] = base_url
                row['URLforsale'] = base_url + "/filter/property-type=land,min-lot-size=4-acre"
                row['URL1mo'] = base_url + "/filter/property-type=land,min-lot-size=4-acre,include=sold-1mo"
                row['URL3mo'] = base_url + "/filter/property-type=land,min-lot-size=4-acre,include=sold-3mo"
                row['URL6mo'] = base_url + "/filter/property-type=land,min-lot-size=4-acre,include=sold-6mo"
                row['URL1yr'] = base_url + "/filter/property-type=land,min-lot-size=4-acre,include=sold-1yr"

            except WebDriverException as e:
                # Handle the pop-up or any WebDriverException
                print(f"Ignoring keyword: {keyword}")
                print("WebDriverException:", e)
                print()

                # Execute JavaScript to stop page loading
                driver.execute_script("window.stop();")

            # Append the updated row to the list
            updated_rows.append(row)

    # Reopen the CSV file for writing
    with open('Keywords.csv', 'w', newline='') as csv_file:
        # Define the column names
        fieldnames = reader.fieldnames + ['base url', 'URLforsale', 'URL1mo', 'URL3mo', 'URL6mo', 'URL1yr']

        # Create a DictWriter to write rows to the CSV
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the updated rows
        writer.writerows(updated_rows)

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()
