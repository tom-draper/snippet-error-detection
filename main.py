import os
import re
from pprint import pprint

import requests
from dotenv import load_dotenv
from colorama import Fore

from validation import *

load_dotenv()


def code_snippets(readme: str) -> list[str]:
    matches = re.findall(r'```[^`]*?```', readme)
    return matches


def collect_errors(url: str, snippets: list[str], errors: list[dict]) -> list[dict[str, str]]:
    for snippet in snippets:
        valid = True
        if re.match(r'```py(thon)?', snippet, re.IGNORECASE):
            code = re.sub(f'```py(thon)?|```', '', snippet, re.IGNORECASE)
            valid, error = valid_python(code)
            language = 'python'
        elif re.match(r'```json', snippet, re.IGNORECASE):
            code = re.sub(r'```json|```', '', snippet, re.IGNORECASE)
            valid, error = valid_json(code)
            language = 'json'
        elif re.match(r'```html', snippet, re.IGNORECASE):
            code = re.sub(r'```html|```', '', snippet, re.IGNORECASE)
            valid, error = valid_html(code)
            language = 'html'
        elif re.match(r'```xml', snippet, re.IGNORECASE):
            code = re.sub(r'```xml|```', '', snippet, re.IGNORECASE)
            valid, error = valid_xml(code)
            language = 'xml'
        
        if not valid:
            errors.append({
                'url': url,
                'language': language,
                'code': snippet,
                'error': error
            })

def display_errors(errors: list[dict[str, str]]):
    if errors:
        for i, error in enumerate(errors):
            print(Fore.CYAN + f'{error["url"]}')
            print(Fore.RED + f'Potential error {i + 1} ({error["language"].upper()})' + Fore.WHITE)
            print(error['code'])
            print(Fore.RED + f'Error: {error["error"]}' + Fore.WHITE)
            print()
        print('\n')

def fetch_snippets(pages: int = 1) -> list[dict]:
    TOKEN = os.getenv('TOKEN')  # Read GitHub account TOKEN variable from .env file
    headers = {
        'Authorization': f'Token {TOKEN}'
    }

    num_readmes = 0
    num_snippets = 0
    errors = []
    for p in range(1, pages+1):
        # Search for README.md files containing three tick marks (```) denoting code snippets
        url = f"https://api.github.com/search/code?q=```filename:README.md+language:markdown+page={p}"
        print(f'Fetching {url}')
        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            d = response.json()
            print(f'{d["total_count"]} results')
            num_readmes += 1

            for result in d['items']:
                readme_url = result['html_url']
                readme_raw_url = readme_url.replace(
                    'https://github.com', 'https://raw.githubusercontent.com').replace('blob/', '')

                response = requests.get(readme_raw_url)
                if response.status_code == 200:
                    readme_content = response.text
                    snippets = code_snippets(readme_content)
                    num_snippets += len(snippets)
                    collect_errors(readme_url, snippets, errors)
        else:
            print(f'Error: status code - {response.status_code}')
            break
    
    print(f'{num_readmes} readme\'s analysed')
    print(f'{num_snippets} snippets analyzed')
        
    return errors
    
    

if __name__ == '__main__':
    errors = fetch_snippets(pages=2)
    print(Fore.RED + f'{len(errors)} potential errors detected' + Fore.WHITE)
    display_errors(errors)
