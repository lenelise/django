import requests

BASE_URL = 'http://127.0.0.1:8080'
TOKEN_URL = f"{BASE_URL}/api/token/"
EXPENSES_URL = f"{BASE_URL}/api/expenses"

'''
This is a script used during development of JWT authentication only. 
'''

#Step 1: get JWT token: 
data = {
    'username': 'non_staff1', 
    'password': 'password321'
}

response_token = requests.post(TOKEN_URL, json=data)

print("token response: \n", response_token.json())
print("\n fetching access token: \n")
access_token = response_token.json().get('access')

if not access_token:
    print("no access token")
    exit()


#Step 2: Use JWT token to make API request: 

headers = {"Authorization": f"Bearer {access_token}"}
print("Request headers: \n", headers)

response = requests.get(EXPENSES_URL, headers=headers)
print("Status code: ", response.status_code)
print(response.json())

try:
    print("Response JSON:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON. Raw response:", response.text)