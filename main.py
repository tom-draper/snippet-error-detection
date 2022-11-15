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


def check_snippets(snippets: list[str]) -> list[dict[str, str]]:
    errors = []
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
                'language': language,
                'code': snippet,
                'error': error
            })
            
    return errors

def display_errors(readme_url: str, errors: list[dict[str, str]]):
    if errors:
        print(Fore.CYAN + f'{readme_url}')
        print(Fore.RED + f'{len(errors)} errors' + Fore.WHITE)
        for i, error in enumerate(errors):
            title = f' SNIPPET {i + 1} ({error["language"].upper()}) '
            print(f'{title:-^80}')
            print(error['code'])
            print(Fore.RED + f'Error: {error["error"]}' + Fore.WHITE)
            print()
        print('\n')
    

if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')  # Read GitHub account TOKEN variable from .env file
    headers = {
        'Authorization': f'Token {TOKEN}'
    }

    page = 1
    # Search for README.md files containing three tick marks (```) denoting code snippets
    url = f"https://api.github.com/search/code?q=```filename:README.md+language:markdown+page={page}"
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
                errors = check_snippets(snippets)
                display_errors(readme_url, errors)
    else:
        print(f'error: status code - {response.status_code}')
