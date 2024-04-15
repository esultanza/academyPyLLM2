# Скрипт для запуска API с сайта https://www.edenai.co/ для перевода текстов с русского на английский. Для работы нужно подставить в параметр "text" текст на русском языке, который вы хотите перевести на английский
import json
import os
import requests

# Установка переменной среды с токеном

os.environ['TOKEN'] = 'Bearer XXX'

headers = {"Authorization": os.environ['TOKEN']}

url = "https://api.edenai.run/v2/translation/automatic_translation"
payload = {
    "providers": "google,amazon",
    "source_language": "en",
    "target_language": "rus",
    "text": "laught",
    "fallback_providers": ""
}

response = requests.post(url, json=payload, headers=headers)

result = json.loads(response.text)
print(result['google']['text'])