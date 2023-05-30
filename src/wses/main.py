import argparse
import csv
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Configure Loguru
logger.add("scraping.log", level="INFO", format="{time} {level} {message}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='URL of the website to scrape',
                        required=True)
    parser.add_argument('-d', '--delay', type=int, default=5,
                        help='Delay between requests in seconds (default: 5)')
    parser.add_argument('-a', '--user-agent', help='User agent to use',
                        default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    parser.add_argument('-o', '--output', default='output.csv',
                        help='Output file for the scraped data (CSV)')
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


def scrape_ecommerce_website(url, delay, user_agent):
    driver = init_webdriver(user_agent)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product')))

        products = []

        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            product_elements = soup.find_all('div', {'class': 'product'})
            products.extend([get_product_info(product_element)
                             for product_element in product_elements])

            next_page = soup.find('a', {'class': 'next-page'})
            if next_page:
                next_page_url = urljoin(url, next_page['href'])
                logger.info(f'Navigating to next page: {next_page_url}')
                driver.get(next_page_url)
                time.sleep(delay)
            else:
                break

    except Exception as e:
        logger.error(f'Scraping failed: {str(e)}')
        products = []

    finally:
        driver.quit()

    return products


def save_to_csv(output_file, data):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'price', 'description', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main():
    args = parse_args()
    url = args.url
    output_file = args.output
    delay = args.delay

    logger.info(f'Starting to scrape {url}')
    products = scrape_ecommerce_website(url, delay)

    if products:
        logger.info(f'Saving scraped data to {output_file}')
        save_to_csv(output_file, products)
        logger.info(f'Scraping completed successfully')
    else:
        logger.error('No data was scraped')


if __name__ == '__main__':
    main()
