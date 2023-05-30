import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def get_product_info(product_element):
    title = product_element.find(
        'div', {'class': 'product-title'}).text.strip()
    price = product_element.find(
        'div', {'class': 'product-price'}).text.strip()
    description = product_element.find(
        'div', {'class': 'product-description'}).text.strip()
    image_url = product_element.find('img')['src']

    return {
        'title': title,
        'price': price,
        'description': description,
        'image_url': image_url
    }


def scrape_ecommerce_website(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    # Wait for the products to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'product'))
    )

    # Bypass captcha or other anti-bot measures if necessary
    bypass_captcha(driver)

    # Get the page source and parse it with Beautiful Soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all product elements
    product_elements = soup.find_all('div', {'class': 'product'})

    # Extract product information
    products = [get_product_info(product_element)
                for product_element in product_elements]

    driver.quit()
    return products


def main():
    url = 'https://www.example-ecommerce-site.com/'
    products = scrape_ecommerce_website(url)

    for product in products:
        print(f"Title: {product['title']}")
        print(f"Price: {product['price']}")
        print(f"Description: {product['description']}")
        print(f"Image URL: {product['image_url']}")
        print('-' * 80)


if __name__ == '__main__':
    main()
