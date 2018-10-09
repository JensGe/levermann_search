from bs4 import BeautifulSoup
import requests


def get_url_content(url):
    return requests.get(url).content.decode("utf-8")


def save_content_to_file(content):
    return True


def get_content_from_file(file):
    with open(file, 'r') as f:
        content_file = f.read()
    return content_file


def create_soup_from_content(content):
    return BeautifulSoup(content, "html.parser")