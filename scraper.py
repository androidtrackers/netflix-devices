#!/usr/bin/env python3
"""Netflix supported devices tracker"""
import json
from datetime import date
from os import environ, system

from bs4 import BeautifulSoup
from requests import get

GIT_OAUTH_TOKEN = environ['XFU']

# Netflix page variable
URL = "https://help.netflix.com/en/node/23939"
HD_SELECTOR = "div.panels > div.tab-panel:nth-of-type(4) > div.c-wrapper > " \
              "div.accordion > div.c-wrapper > div.tab > div.tab-content > " \
              "div.c-wrapper > div > ul > li > p"
HDR_SELECTOR = "div.panels > div.tab-panel:nth-of-type(5) > div.c-wrapper > " \
               "div.accordion > div.c-wrapper > div.tab > div.tab-content > " \
               "div.c-wrapper > div > ul > li > p"


def fetch(url):
    """Fetch page content from URL"""
    return get(url)


def parse(response):
    """Parse netflix page response"""
    page = BeautifulSoup(response, 'html.parser')
    hd_data = page.select(HD_SELECTOR)
    hdr_data = page.select(HD_SELECTOR)
    return {'hd_devices': [i.text.strip() for i in hd_data], 'hdr_devices': [i.text.strip() for i in hdr_data]}


def write_data(data):
    """Write data to JSON file"""
    with open("netflix_devices.json", "w") as out:
        json.dump(data, out, indent=1, ensure_ascii=False)


def git_commit_push():
    """
    git add - git commit - git push
    """
    system(f'git add *.json && git -c "user.name='
           f'user.name=CI" -c "user.email='
           f'example@example.com" commit -m "[skip ci] sync: {str(date.today())}"'
           f' && git push -q https://{GIT_OAUTH_TOKEN}@github.com/'
           f'androidtrackers/netflix-devices.git HEAD:master')


def main():
    """
    Netflix supported devices tracker
    """
    response = fetch(URL)
    data = parse(response.text)
    write_data(data)
    git_commit_push()


if __name__ == '__main__':
    main()
