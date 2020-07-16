# Script to scrape laptops on sale from BestBuy.ca
# Personal project by Justin Mikhail, Computer Engineering Student
# July 12/ 2020
import time
import pandas

from selenium import webdriver
from bs4 import BeautifulSoup

# Function to click the button on the page and wait a few seconds
def click_button():
	button = driver.find_element_by_class_name("content_3dXxd") # Must redefine button to avoid stale error
	button.click()
	time.sleep(5) # Time allows the page to load (may depend on internet speeds)

# Function to write csv files with a pandas dataframe
def write_csv(dataframe, file_name):
	#dataframe.index += 1 	## With this line the first laptop will have an index of 1 beside it (optional)
	dataframe.to_csv(f"{file_name}.csv")

url = "https://www.bestbuy.ca/en-ca/collection/laptops-on-sale/46082?path=category%253aComputers%2B%2526%2BTablets%253bcategory%253aLaptops%2B%2526%2BMacBooks%253bsoldandshippedby0enrchstring%253aBest%2BBuy"

options = webdriver.ChromeOptions()
options.add_argument("--incognito") # Fresh start every time so no interference
options.add_argument("--headless") # The chrome window won't pop up on screen and show animations
chrome_options=options

driver = webdriver.Chrome(options=options) # Initialize driver with chrome options defined above
driver.get(url) # Bring the browser to the url specified above
driver.set_window_size(1600, 900) # Set window resolution so that all elements can still load on page

assert "Laptops on Sale" in driver.title # Make sure we are on the right page before proceeding
time.sleep(5) # Give time to load full page

button = driver.find_element_by_class_name("content_3dXxd") # Finding the "Show More" button at the bottom of the page

while True: # If the button exists, click it
	try:
		click_button()
	except:
		break

html = driver.page_source # Once the full page with products is loaded, get the html data
driver.quit() # Close our automated browser

html_soup = BeautifulSoup(html, "html.parser") # Parse the html data for analysis and sorting
laptop_containers = html_soup.find_all("div", class_ ="col-xs-8_1VO-Q col-sm-12_1kbJA productItemTextContainer_HocvR") # Find the containers that contains a products info

# Create lists to be added to
names = []
prices = []
discounts = []
ratings = []
num_reviews = []

for laptop in laptop_containers: # Go through each laptop on page
	# Names
	name = laptop.find("div", class_ = "productItemName_3IZ3c").text
	names.append(name)
	# Prices
	price = laptop.find("div", class_ = "price_FHDfG").text
	prices.append(price)
	# Discounts
	discount = laptop.find("span", class_ = "productSaving_3YmNX").text
	discount = discount.split() # Gets rid of "SAVE" and just leaves the $price
	discounts.append(discount[-1])
	# Ratings
	rating = laptop.find("meta", attrs = {"itemprop": "ratingValue"})
	ratings.append(float(rating["content"])) # Gives the number value of the rating
	# Reviews
	review = laptop.find("span", attrs = {"itemprop": "ratingCount"}).text
	review = review[1:-1] # Removes parentheses around string
	review = review.split() # Splits into [NUMBER, "Reviews"]
	num_reviews.append(int(review[0])) # Only take number

# Dictionary with headers and values of laptop data
laptop_dict = {
	"Name": names,
	"Sale Price": prices,
	"Discount": discounts,
	"Rating": ratings,
	"Number of Reviews": num_reviews
}

#Create structured dataframe of dictionary data for easy access and use
laptop_dataframe = pandas.DataFrame(laptop_dict)

# Finally write file to csv for external use and print end statement
write_csv(laptop_dataframe, "laptops_csv")
print("Web Scraping and CSV file writing complete!")

