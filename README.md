# Pinterest Image Scraper

This scrapper will load all pins matching a query term and download the images associated with the pin.

## Requirements:

- Python3
- Selenium
- Requests
- [Geckodriver](https://github.com/mozilla/geckodriver/releases)

## How to Run:
- Edit the `run.sh` script by changing *term* to what your query should be
- Pass a second param to limit number of pages queried. (default 10)
- After running the script, the `results` folder will contain a folder with the name of your query term and the downloaded images from pinterest
