from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import random
import socket
import time
import unicodedata
import urllib
import requests
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import FirefoxOptions


def randdelay(a, b):
    time.sleep(random.uniform(a, b))


def u_to_s(uni):
    return unicodedata.normalize('NFKD', uni).encode('ascii', 'ignore')

class PinterestDownloader:
    """Class to download Pinterest images."""
    
    def __init__(self):
        print('Initialized image downloader')

    def download(self, image_url: str, query_param: str) -> None:
        """Downloads an image from the given URL.

        Args:
            image_url (str): The URL of the image to be downloaded.
            query_param (str): The query parameter used for organizing the downloaded images.
        """
        print(f'Downloading image from {image_url}')
        img_data = requests.get(image_url).content
        image_url = str(image_url)[:-1].split('/')[-1]
        with open(f'results/{query_param}/{image_url}', 'wb') as handler:
            handler.write(img_data)

class PinterestHelper:
    """Class to interact with Pinterest using Selenium."""

    def __init__(self, url: str, threshold: int = 10):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.browser = webdriver.Firefox(executable_path='./bin/geckodriver', options=opts)
        self.images = []
        tries = 0
        try:
            self.browser.get(url)
            self.images = self.process_images(tries, threshold)
        except (socket.error, socket.timeout):
            pass

    def close(self) -> None:
        """Closes the browser."""
        self.browser.close()

    def process_images(self, tries: int = 0, threshold: int = 500) -> list[str]:
        """Processes images found on the Pinterest page.

        Args:
            tries (int): The number of attempts made for processing.
            threshold (int): Maximum number of processing attempts.

        Returns:
            List of image URLs.
        """
        results = []
        while threshold > 0:
            print(f'Processing {tries}')
            try:
                images = self.browser.find_elements(By.TAG_NAME, "img")
                if tries > threshold - 1:
                    return results
                for i in images:
                    src = i.get_attribute("src")
                    if src:
                        if src.find("/236x/") != -1 or src.find("/474x/") != 1:
                            print(src)
                            src = src.replace("/236x/", "/736x/")
                            src = src.replace("/474x/", "/736x/")
                            results.append(u_to_s(src))
                body = self.browser.find_element(By.XPATH, '/html/body')
                body.send_keys(Keys.PAGE_DOWN)
                randdelay(0, 1)
                tries += 1
            except StaleElementReferenceException:
                tries += 1
        print(f'Processed {len(results)}')
        return results

    def write_results(self, query_param: str, images: list[str]) -> None:
        """Writes image URLs to a text file and downloads images.

        Args:
            query_param (str): The query parameter used for organizing the downloaded images.
            images (list): List of image URLs to be written and downloaded.
        """
        print(f'Saving {len(images)} URLs to text file')
        if not os.path.exists(f'results/{query_param}'):
            print(f'Creating results/{query_param}')
            os.makedirs(f'results/{query_param}')
        else:
            print(f'Cleaning results/{query_param}')
            for root, dirs, files in os.walk(f'results/{query_param}'):
                for file in files:
                    os.remove(os.path.join(root, file))
            print(f'Cleaned folder of previous results')
        
        with open(f'results/{query_param}/'+query_param.replace(" ", "") + "_pins.txt", "w") as file:
            file.write('\n'.join([i.decode('UTF-8') for i in images]))
        
        self.downloader = PinterestDownloader()
        for image in images:
            self.downloader.download(image, query_param)
        print(f'Saved {len(images)} images')

def main():
    args = sys.argv
    if(len(args) > 1):
        term = args[1]
        limit = 10
        try:
            limit = int(args[2])
        except IndexError:
            print(f'No limit passed. Defaulting to 10')
        ph = PinterestHelper('http://pinterest.com/search/pins/?q=' + urllib.parse.quote(term), limit)
        ph.write_results(term, ph.images)
        ph.close()
    else:
        print(f'Parameters passed are wrong. Please check')

if __name__ == '__main__':
    main()
