"""
Simple robot that opens a web page, serach for terms, and takes a screenshot
 of the web page using the RPA.Browser.Selenium librirary
"""
# Import the Selenium library
from RPA.Browser.Selenium import Selenium

# Initialize the browser library
browser = Selenium()


""" Define the functions that implements the operations the robot is supposes to do """
def open_the_website(url):
    browser.open_available_browser(url)



def search_for(term):
    input_field =  "css:input"
    browser.input_text(input_field, term)
    browser.press_key(input_field, "ENTER")


def store_screenshot(filename):
    browser.screenshot(filename=filename)



# Define a main function that calls the other functions in order
def main():
    try:
        open_the_website("https://robocorp.com/docs/")
        search_for("python")
        store_screenshot("output/screenshot.png")
    finally:
        browser.close_all_browsers()


# Call the main function, checking that we are running as a stand-alone script
if __name__ == "__main__":
    main()