# Pinterest Image Scraper

This script allows you to search Pinterest for a specific keyword and then download the associated pin images.

## Requirements:

- Python3
- Selenium
- Requests
- [Geckodriver](https://github.com/mozilla/geckodriver/releases)

## Usage

1. Edit the `run.sh` script by changing the *term* variable to your desired query term.
2. Optionally, you can pass a second parameter to limit the number of pages queried (default is 10).
3. Run the script.
4. After running the script, the `results` folder will contain a subfolder with the name of your query term, containing the downloaded images from Pinterest.

## Class Documentation

### PinterestDownloader

A class responsible for downloading Pinterest images.

#### Methods

##### `download(image_url: str, query_param: str) -> None`

Downloads an image from the given URL.

- `image_url` (str): The URL of the image to be downloaded.
- `query_param` (str): The query parameter used for organizing the downloaded images.

### PinterestHelper

A class for interacting with Pinterest using Selenium.

#### Methods

##### `__init__(self, url: str, threshold: int = 10)`

Initializes the PinterestHelper object.

- `url` (str): The URL of the Pinterest search page.
- `threshold` (int): The maximum number of processing attempts.

##### `close(self) -> None`

Closes the browser instance.

##### `process_images(self, tries: int = 0, threshold: int = 500) -> List[str]`

Processes images found on the Pinterest page.

- `tries` (int): The number of attempts made for processing.
- `threshold` (int): Maximum number of processing attempts.

Returns:
- List of image URLs.

##### `write_results(self, query_param: str, images: List[str]) -> None`

Writes image URLs to a text file and downloads images.

- `query_param` (str): The query parameter used for organizing the downloaded images.
- `images` (List): List of image URLs to be written and downloaded.

### main

The main function that initiates the Pinterest image scraping process. Accepts command-line arguments.

To run the script, execute it from the command line with the desired query term and optional limit parameter.

Example:

``` bash
python script_name.py "cats" 5
```

In this example, the script searches for pins related to "cats" and limits the search to 5 pages.
