import requests

url = 'http://127.0.0.1:8080/api/token/'
data = {
    'username': 'staff1', 
    'password': 'password321'
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
print(response.headers)
