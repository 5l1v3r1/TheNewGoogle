from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import os


scanned_urls = []
titles = []
outer_links = []


def is_outer_url(url, base_url):
    if base_url in url:
        return False
    return True


def prepare_link(url, href):
    return urljoin(url, href)


def check_security(url):
    if "https://" in url:
        return True
    return False


def clean(request, html, soup):
    request = None
    html = None
    soup = None


def url_checker(url):
    path = urlparse(url).path
    extension = os.path.splitext(path)[1]

    if extension != "":
        return False

    if url in scanned_urls or url in outer_links:
        return False

    if "#" in url or "share" in url:
        outer_links.append(url)
        return False
    return True


def scan_page(url, base_url):
    if url_checker(url):
        request = requests.get(url)
        html = request.text
        soup = BeautifulSoup(html)

        print (url)
        if soup.title:
            if url not in scanned_urls:
                scanned_urls.append(url)
                titles.append(soup.title.string.encode('utf-8'))

            for link in soup.find_all("a"):
                new_link = prepare_link(url, link.get("href"))
                clean(request, html, soup)
                if not is_outer_url(new_link, base_url):
                    scan_page(new_link, base_url)
                elif is_outer_url(new_link, base_url):
                    outer_links.append(new_link)
                    scan_page(new_link, base_url)
    else:
        return

    return scanned_urls
