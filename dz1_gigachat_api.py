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

    response = requests.request("POST", url, headers=headers, data=payload).json()
    return response["access_token"]


def text_generate():
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    conversation_history=[
        {
            "role": "system",
            "content": "Отвечай как начальник отдела коммунистической цензуры."
        },{
            "role": "user",
            "content": "Расскажи, какими смыслами были наполнены песни в СССР.\\nПриведи редкие примеры песен."
        }
    ]
    payload = json.dumps({
        "model": "GigaChat",
        "messages": conversation_history,
        "temperature": 1,  # Температура генерации
        "top_p": 0.4,  # Параметр top_p для контроля разнообразия ответов
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,  # Потоковая ли передача ответов
        "max_tokens": 200,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1,  # Штраф за повторения
        "update_interval": 0  # Интервал обновления (для потоковой передачи)
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_tokens()}'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload).json()
        response_content=response["choices"][0]["message"]["content"]
        print(response_content)
        # Добавление ответа модели в историю диалога
        conversation_history.append({
            "role": "assistant",
            "content": response_content
        })
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return None, conversation_history

if __name__ == '__main__':
    text_generate()
