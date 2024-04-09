import requests
import json
import uuid
import time
import creds


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
    return response.json()


def text_generate():
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    get_token = str(get_tokens()["access_token"])

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": "Расскажи, о чем 'Марш энтузиастов'"
                # "content": "Расскажи, о чем пели в СССР"
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
        'Authorization': f'Bearer {get_token})'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response["choices"][0]["message"]["content"])


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
        'Authorization': 'Bearer <токен_доступа>'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    text_generate()
