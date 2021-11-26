"""Link scanner module"""
import os
import sys
from http.client import HTTPResponse
from urllib import request
from typing import List
from urllib.error import HTTPError, URLError

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.headless = True
browser = webdriver.Chrome(options=options)


def get_pure_link(link: str) -> str:
    """Delete anthing after # and ? in the given link.

    Args:
        link: The link to delete information from
    Returns:
        Same link but without # and ?

    >>> get_pure_link('https://somerandom.site/index.html#navigation')
    'https://somerandom.site/index.html'
    >>> get_pure_link('https://evenmore.com/index.html#gather?love=12')
    'https://evenmore.com/index.html'
    """
    no_hash = link.split('#')[0]
    no_hash_or_param = no_hash.split('?')[0]
    return no_hash_or_param


def get_links(url: str):
    """Find all links on page at the given url.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    link_set = set()  # Use set to guarantee uniqueness
    browser.get(url)
    all_link_tags = browser.find_elements(By.TAG_NAME, 'a')
    for link_tag in all_link_tags:
        href = link_tag.get_attribute('href')
        if href:
            pure_link = get_pure_link(href)
            if pure_link:
                # It is an actual link.
                # It is not empty after removing whatever after ? and #.
                link_set.add(pure_link)

    # Note: The order may not be fixed.
    return list(link_set)


def is_valid_url(url: str):
    """Check if the given url is valid or not.

    It checks by attempting to create a connection with it.

    Args:
        url: Url to check

    Returns:
        bool: True if the url is valid. Otherwise, it is false.
    """
    response: HTTPResponse = request.urlopen(url)
    try:
        code = response.getcode()
    except URLError:
        return False
    if code == 403:
        return True
    # 4XX means error on the client side.
    # 5XX means error on the server side.
    return 400 <= code < 600


def invalid_urls(urllist: List[str]) -> List[str]:
    """Return list of invalid urls from given list of urls.

    Args:
        urllist: List of urls to check

    Returns:
        List[str]: List of invalid urls
    """
    return [url for url in urllist if is_valid_url(url)]


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        filename = os.path.basename(sys.argv[0])
        print(f"Usage: python3 {filename} url_to_scan")
    else:
        print("Url is valid now.")