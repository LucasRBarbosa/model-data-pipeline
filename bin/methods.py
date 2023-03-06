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

    if response.status_code == 201:
        response_json = response.json()
        return response_json["access_token"], response_json["refresh_token"]
    else:
        return None, None

def refresh_token_method(refresh_token):
    """
    Use the refresh token to obtain a new access token.
    Returns the new access token.
    """
    url = "https://api.escuelajs.co/api/v1/auth/refresh-token"
    headers = {"Content-Type": "application/json"}
    data = {"refreshToken": refresh_token}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    if response.status_code == 201:
        response_json = response.json()
        return response_json["access_token"], response_json["refresh_token"]
    else:
        return None, None

def create_user(username, email, password, avatar):
    url = "https://api.escuelajs.co/api/v1/users/"
    data =  {
        "name": username,
        "email": email,
        "password": password,
        "avatar": avatar
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        user_id = response.json()["id"]
        return user_id
    else:
        print(response.json())
        return None

def get_category_id(category_name, access_token):
    url = "https://api.escuelajs.co/api/v1/categories/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        categories = response.json()
        for category in categories:
            if category["name"] == category_name:
                return category["id"]
    else:
        print(f"Error {response.status_code}: {response.text}")


def get_products_by_category(category_id, access_token, refresh_token):
    url = "https://api.escuelajs.co/api/v1/products/"
    headers = {"Authorization": f"Bearer {access_token}"}
    products = []
    offset = 0
    limit = 10
    while True:
        response = requests.get(url, headers=headers, params={"offset": offset, "limit": limit, "categoryId": category_id})
        if response.status_code == 200:
            page_products = response.json()
            if not page_products:
                break
            products.extend(page_products)
            offset += 10
            limit +=10
        elif response.status_code == 401:
            access_token, refresh_token = refresh_token_method(refresh_token)
            if not access_token:
                print("Authentication failed.")
                break
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            print(f"Error: {response.status_code}")
            break
    return pd.DataFrame(products)

def create_result_df(data_df, currency_df):
    merged_df = pd.merge(data_df, currency_df[['currency', 'obs_value', 'time_period']], left_on='currency',right_on='currency', how='left')
    merged_df['price_euro'] = merged_df['price'] / merged_df['obs_value']
    # merged_df.to_csv('end_result.csv') # --> Uncomment this line to save the output df as an csv
    print("Completed!")
    return merged_df