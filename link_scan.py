"""Link scanner."""
import os
import sys
from urllib import request
from typing import List
from urllib.error import HTTPError, URLError
from urllib.request import Request

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


def is_html_page(url: str) -> bool:
    """Check if the given link is HTML or not.

    The method exists because if the web driver goes to non-HTML page,
    it might download the file. This behavior is undesired by this program.

    Args:
        url: The url to scan for. It must be a valid url.
    Returns:
        bool: True if the link is HTML. It is False otherwise.
    """
    try:
        request_object = Request(url, method='HEAD')
        response = request.urlopen(request_object)
    except HTTPError:
        return False
    except URLError:
        return False
    info = response.info()
    # Unless the server is lying, HTML content will have
    # this content type.
    # If the content type is text/html but the actual content is not HTML,
    # Selenium will handle it. It can't scan the page anyway.
    return info.get_content_type() == 'text/html'


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
    try:
        request_object = Request(url, method='HEAD')
        request.urlopen(request_object)
    except HTTPError as e:
        if e.getcode() != 403:
            return False
    except URLError:
        return False
    return True


def invalid_urls(urllist: List[str]) -> List[str]:
    """Return list of invalid urls from given list of urls.

    Args:
        urllist: List of urls to check

    Returns:
        List[str]: List of invalid urls
    """
    return [url for url in urllist if not is_valid_url(url)]


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        filename = os.path.basename(sys.argv[0])
        print(f'Usage: python3 {filename} url_to_scan')
        sys.exit(1)
    url_to_scan = sys.argv[1]
    if not is_html_page(url_to_scan):
        print(f"{url_to_scan} is not a valid HTML page.")
        sys.exit(1)
    all_links = get_links(url_to_scan)
    for link in all_links:
        print(link)
    print()

    # Print bad links.
    invalid_links = invalid_urls(all_links)
    if invalid_links:
        print("Bad Links:")
        for link in invalid_links:
            print(link)
