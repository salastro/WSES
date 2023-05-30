# Ecommerce Scraper

Ecommerce Scraper is a Python script that scrapes product information from an ecommerce website using Selenium, BeautifulSoup, and CSV libraries. The script is designed to be easy to use and extendable to other websites as needed.

## Features

- Scrape product information (title, price, description, image URL) from an ecommerce website
- Navigate through paginated product listings
- Adjustable delay between requests to avoid overwhelming the server
- Customizable user agent
- Log scraping progress and errors
- Save the scraped data in a CSV file

## Requirements

- Python 3.6 or higher
- Selenium
- BeautifulSoup
- Loguru
- webdriver-manager

To install , run:

```bash
pip install -e .
```

## Usage

To run the script, use the following command:

```bash
wses -u <URL> -d <DELAY> -a <USER_AGENT> -o <OUTPUT>
```

Arguments:

- `-u` / `--url`: The URL of the ecommerce website to scrape (required)
- `-d` / `--delay`: The delay between requests in seconds (default: 5)
- `-a` / `--user-agent`: The user agent to use for web requests (default: Mozilla/5.0)
- `-o` / `--output`: The output file for the scraped data (default: output.csv)

Example:

```bash
wses -u https://example.com/products -d 5 -a "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -o output.csv
```

## Customization

To adapt the script to other ecommerce websites, you may need to modify the following functions:

- `get_product_info(product_element)`: Update the selectors and attributes to match the structure of the target website's product elements.
- `scrape_ecommerce_website(url, delay, user_agent)`: Update the condition that checks for the presence of the next-page link and the extraction of the link's URL.
