import requests

response = requests.get("https://httpbin.org/get")

print("Статус ответа:", response.status_code)
print("Ответ сервера:", response.json())
