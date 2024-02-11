# NSE Data Scraper

This script is designed to scrape data from the National Stock Exchange (NSE) website. It gathers information about stock indices and individual stock symbols listed on the NSE.

## Features

- Scrapes data for individual stock symbols including company name, metadata, price information, industry info, trade info, value at risk, preopen data, and raw data.
- Scrapes data for stock indices including constituent stock symbols and their respective data.

## Prerequisites

Before running the script, make sure you have Python installed on your system. You'll also need the following Python libraries:

- pandas
- requests

You can install these libraries using pip:

> pip install pandas requests


## Usage

1. Clone the repository or download the script file (`nse_data_scraper.py`) to your local machine.

2. Open a terminal or command prompt and navigate to the directory where the script is located.

3. Run the script by executing the following command:
> python nse_data_scraper.py


4. The script will start scraping data from the NSE website. The scraped data will be saved in JSON format in the `root_data/nseraw_data/` directory.

## Disclaimer

This script is for educational purposes only. It is your responsibility to ensure compliance with the terms of service or any legal restrictions imposed by the NSE website or any other website you scrape data from.

## License

This script is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
