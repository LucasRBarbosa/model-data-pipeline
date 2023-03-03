import requests
import pandas as pd
import io

def get_api_data(url, startPeriod, endPeriod):
    url = f'{url}?startPeriod={startPeriod}&endPeriod={endPeriod}'
    response = requests.get(url, headers={'Accept': 'text/csv'})

    if response.status_code == 200:
        data = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(data), index_col=False)
        df = df.rename(columns=lambda x: x.lower())
        return df
    else:
        print(f'Request failed with status code {response.status_code}')

def authenticate(email, password):
    url = "https://api.escuelajs.co/api/v1/auth/login"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    print(response)
    if response.status_code == 201:
        response_json = response.json()
        return response_json["access_token"], response_json["refresh_token"]
    else:
        return None, None

def create_user(username, email, password):
    url = "https://api.escuelajs.co/api/v1/users/"
    data = {"username": username, "email": email, "password": password}
    response = requests.post(url, json=data)
    if response.status_code == 201:
        user_id = response.json()["id"]
        return user_id
    else:
        return None

def get_products_by_category(category_id, access_token, refresh_token):
    url = "https://api.escuelajs.co/api/v1/products/"
    params = {"categoryId": category_id}
    headers = {"Authorization": f"Bearer {access_token}"}
    products = []
    page = 1
    while True:
        response = requests.get(url, headers=headers, params={"page": page, "categoryId": category_id})
        if response.status_code == 200:
            page_products = response.json()
            if not page_products:
                break
            products.extend(page_products)
            page += 1
            if page > 10:
                break
            print(page)
        elif response.status_code == 401:
            access_token, refresh_token = authenticate("your_username", "your_password")
            if not access_token:
                print("Authentication failed.")
                break
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            print(f"Error: {response.status_code}")
            break
    return pd.DataFrame(products)
