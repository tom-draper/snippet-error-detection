import os
import re
from pprint import pprint

import requests
from dotenv import load_dotenv

from validation import *

load_dotenv()


def code_snippets(readme: str) -> list[str]:
    matches = re.findall(r'```[^`]*?```', readme)
    return matches


def check_snippets_lang(snippets: list[str], language_regex: str, valid: callable):
    for snippet in snippets:
        print('---------------- snippet')
        print(snippet)
        if re.match(f'```{language_regex}', snippet, re.IGNORECASE):
            code = re.sub(f'```{language_regex}|```',
                          '', snippet, re.IGNORECASE)
            print(
                '-------------------------------------------------------------------------')
            print(code)
            print(
                '-------------------------------------------------------------------------')
            x = valid(code)
            print(x)


def check_snippets(snippets: list[str]):
    check_snippets_lang(snippets, 'py(thon)?', valid_python)
    check_snippets_lang(snippets, 'json', valid_json)
    check_snippets_lang(snippets, 'html', valid_html)
    check_snippets_lang(snippets, 'xml', valid_xml)


TOKEN = os.getenv('TOKEN')  # Read GitHub account TOKEN variable from .env file
headers = {
    'Authorization': f'Token {TOKEN}'
}

url = "https://api.github.com/search/code?q=```filename:README.md+language:markdown"
response = requests.request("GET", url, headers=headers)

if response.status_code == 200:
    d = response.json()
    pprint(d)

    for result in d['items']:
        readme_url = result['html_url']
        raw_readme_url = readme_url.replace(
            'https://github.com', 'https://raw.githubusercontent.com').replace('blob/', '')

        response = requests.get(raw_readme_url)
        if response.status_code == 200:
            readme = response.text
            snippets = code_snippets(readme)
            check_snippets(snippets)
else:
    print(f'error: status code - {response.status_code}')
