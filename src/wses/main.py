import argparse
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL of the website to scrape')
    parser.add_argument('-d', '--delay', type=int, default=5,
                        help='Delay between requests in seconds (default: 5)')
    return parser.parse_args()


def init_webdriver(user_agent):
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)
    return driver


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


def scrape_ecommerce_website(url, delay):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    driver = init_webdriver(user_agent)
    driver.get(url)

    # Wait for the products to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'product'))
    )

    # Get the page source and parse it with Beautiful Soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all product elements
    product_elements = soup.find_all('div', {'class': 'product'})

    # Extract product information
    products = [get_product_info(product_element)
                for product_element in product_elements]

    next_page = soup.find('a', {'class': 'next-page'})
    if next_page:
        next_page_url = urljoin(url, next_page['href'])
    driver.get(next_page_url)
    time.sleep(delay)

    driver.quit()
    return products


def main():
    args = parse_args()
    url = args.url
    delay = args.delay
    products = scrape_ecommerce_website(url, delay)

    for product in products:
        print(f"Title: {product['title']}")
        print(f"Price: {product['price']}")
        print(f"Description: {product['description']}")
        print(f"Image URL: {product['image_url']}")
        print('-' * 80)


if __name__ == '__main__':
    main()
