import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Function to scroll down and load more products
def scroll_and_load_more(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Function to scrape data from a single page
def scrape_page(url):
    # Initialize a list to store product data
    products = []

    # Use Selenium to load the webpage
    driver = webdriver.Edge()  # Replace with your Edge WebDriver path if needed
    driver.get(url)

    # Scroll down to load more products
    scroll_and_load_more(driver)

    # Get the page source after scrolling
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract product details
    product_elements = soup.find_all('div', class_='product-item')

    for product_element in product_elements:
        product = {}
        product['Product Title'] = product_element.find('h2').text.strip()
        product['Product Image URL'] = product_element.find('img')['src']
        product['Price of the Product'] = product_element.find('span', class_='price').text.strip()
        product['Product Details'] = product_element.find('div', class_='description').text.strip()

        products.append(product)

    driver.quit()

    return products

# Function to scrape data from all pages
def scrape_all_pages(base_url, num_pages):
    all_products = []

    for page_num in range(1, num_pages + 1):
        page_url = f"{base_url}?page={page_num}"
        products = scrape_page(page_url)
        all_products.extend(products)

    return all_products

if __name__ == '__main__':
    base_url = "https://www.zigly.com/shop/dogs/dog-food/dry-food.html"
    num_pages = 5  # Set the number of pages to scrape (example: 5 pages)

    all_products = scrape_all_pages(base_url, num_pages)

    # Save the data as JSON
    with open('dog_food_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_products, json_file, ensure_ascii=False, indent=4)
