"""
Simple robot that opens a web page, search for terms, and takes a screenshot
 of the web page using the RPA.Browser.Selenium librirary
"""
# Import the Selenium library
from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems
import time
import pandas as pd
from selenium.webdriver.common.by import By

# Get work item variables
wi = WorkItems()
wi.get_input_work_item()

# search term
search_phrase = wi.get_work_item_variable("search_term")

print(search_phrase)

# Initialize the browser library
browser = Selenium()



""" Define the functions that implements the operations the robot is supposes to do """
# 1. Open the site by following the link
def open_the_website(url):
    browser.open_available_browser(url)


# 2. Enter a phrase in the search field
def search_for_results(term):
    # Active the search form
    seach_button = browser.find_element("//button[@class='css-tkwi90 e1iflr850']")
    browser.click_button(seach_button)

    # Write search phrase on the activeted search form
    input_field =  browser.find_element("//input[@placeholder='SEARCH']")
    browser.input_text(input_field, term)

    # Submit the form to get the results of the search term
    go_button = browser.find_element("//button[@class='css-1gudca6 e1iflr852']")
    browser.click_button(go_button)

    #time.sleep(60)
  

# Find all the search result articles, and apply filters
def search_result_articles():

     # Create a list to store the data
    data = []

    # Get ol containing list of articles
    articles = browser.find_elements("//ol[@data-testid='search-results']//li")
    

    # Loop through and extract title, date, and element
    for article in articles:
        # Extract title
        try:
            title = article.find_element(By.TAG_NAME, "h4")
            article_date = article.find_element(By.CLASS_NAME, "css-17ubb9w")
            description = article.find_element(By.CLASS_NAME, "css-16nhkrn")
            
            data.append([title.text, article_date.text, description.text])
        except Exception as e:
            print(e)
            pass

    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data, columns=["Title", "Date", "Description"])

    # Save the DataFrame to an Excel file
    df.to_excel("output/nytimes_search_results.xlsx", index=False)
        

# Define a main function that calls the other functions in order
def main():
    try:
        open_the_website("https://www.nytimes.com/")
        search_for_results(search_phrase)
        search_result_articles()
    finally:
        browser.close_all_browsers()


# Call the main function, checking that we are running as a stand-alone script
if __name__ == "__main__":
    main()