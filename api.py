import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()


class GPTApi:
    api_key = os.getenv('API_KEY')
    headers = {'Content-type': 'application/json', 'Authorization': f'Bearer {api_key}'}
    base_url = 'https://api.openai.com/v1'

    def __int__(self, api_key, headers, base_url):
        self.api_key = api_key
        self.headers = headers
        self.base_url = base_url

    def images_api_post(self, data):
        return requests.post(f'{self.base_url}/images/generations', headers=self.headers, data=json.dumps(data)).json()

    def code_api_post(self, data):
        return requests.post(f'{self.base_url}/completions', headers=self.headers, data=json.dumps(data)).json()
