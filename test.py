import requests

url = "http://127.0.0.1:5000/api/post-video"
data = {
    "key": "value"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())