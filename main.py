from pprint import pprint
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

def code_snippets(readme: str) -> list[str]:
    matches = re.findall('```[^`]```', readme)
    print('snippets', matches)

TOKEN = os.getenv('TOKEN')
headers = {
  'Authorization': f'Token {TOKEN}'
}

url = "https://api.github.com/search/code?q=```filename:README.md+language:markdown"
response = requests.request("GET", url, headers=headers)

d = response.json()

pprint(d)

for result in d['items']:
    readme_url = result['html_url']
    print(readme_url)
    raw_readme_url = readme_url.replace('https://github.com', 'https://raw.githubusercontent.com').replace('blob/', '')
    print(raw_readme_url)
    
    response = requests.get(raw_readme_url)
    if response.status_code == 200:
        readme = response.text
        print(readme)
        print(code_snippets(readme))