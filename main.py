"""
Simple robot that opens a web page, search for terms, and takes a screenshot
 of the web page using the RPA.Browser.Selenium librirary
"""
# Import the Selenium library
from RPA.Browser.Selenium import Selenium
from RPA.Robocorp.WorkItems import WorkItems
from RPA.HTTP import HTTP
import time
import pandas as pd
from selenium.webdriver.common.by import By

# Get work item variables
wi = WorkItems()
wi.get_input_work_item()

# search term
search_phrase = wi.get_work_item_variable("search_term")

# Apply categories filters
categories = wi.get_work_item_variable("categories")


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


# 3. Apply filters and choose the latest news
def apply_filters(categories):
    # Click to open the list of categories
    show_category_button = browser.find_element("//button[@data-testid='search-multiselect-button']")
    browser.click_button(show_category_button)


    # Check the categories
    tick_category = browser.find_elements("//ul[@data-testid='multi-select-dropdown-list']//li")

    # Loop through the elements to find the category name
    for t in tick_category:
        cat_name = t.find_element(By.TAG_NAME, "span")

        # Remove numbers at the end of the category name
        cleaned_category_name  = ''.join((z for z in cat_name.text if not z.isdigit()))
    
        
       # Check if the category exist in the provided category list then filter the news
        if categories is []:
            any_input = t.find_element(By.XPATH,"//input[@value='any']")
            browser.click_button(any_input)

        
        elif ('' .join((z for z in cat_name.text if not z.isdigit()))).rstrip() in categories:
            current_input = t.find_element(By.TAG_NAME,"span")
            browser.click_button(current_input)
        pass

    # Click to close the list of categories 
    browser.click_button(show_category_button)


    # Sort by news news
    sort_by_relevance =  browser.find_element("//select[@data-testid='SearchForm-sortBy']")
    browser.click_button(sort_by_relevance)

    # Choose the newst news
    newst = browser.find_element("//option[@value='newest']")
    browser.click_button(newst)

    time.sleep(3)
    #exit()



# 4. Find all the search result articles and store in an Excel file
def search_result_articles():

     # Create a list to store the data
    data = []

    # Get ol containing list of articles
    articles = browser.find_elements("//ol[@data-testid='search-results']//li")
    

    # Loop through and extract title, date, and element
    for article in articles:
        try:
            title = article.find_element(By.TAG_NAME, "h4")
            article_date = article.find_element(By.CLASS_NAME, "css-17ubb9w")
            description = article.find_element(By.CLASS_NAME, "css-16nhkrn")
            
            # Append to data
            data.append([title.text, article_date.text, description.text])
        except Exception as e:
            print(e)
            pass

    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data, columns=["Title", "Date", "Description"])

    # Save the DataFrame to an Excel file
    df.to_excel("output/nytimes_search_results.xlsx", index=False)
    #time.sleep(60)
        

# Define a main function that calls the other functions in order
def main():
    try:
        open_the_website("https://www.nytimes.com/")
        search_for_results(search_phrase)
        apply_filters(categories)
        search_result_articles()
    finally:
        browser.close_all_browsers()


# Call the main function, checking that we are running as a stand-alone script
if __name__ == "__main__":
    main()