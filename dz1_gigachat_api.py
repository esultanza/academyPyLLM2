import requests
import json
import uuid
import time
import creds

# https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart?tool=python
def get_tokens():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
        'Authorization': f'Basic {creds.authorize_data}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()["access_token"]


def text_generate():
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": "Расскажи, какими смыслами были наполнены песни в СССР"
            }
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_tokens()}'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response["choices"][0]["message"]["content"])

# платно
def create_embeddings():
    url = "https://gigachat.devices.sberbank.ru/api/v1/embeddings"
    payload = json.dumps({
        "model": "Embeddings",
        "input": [
            "Расскажи о современных технологиях"
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_tokens()}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


if __name__ == '__main__':
    text_generate()
