from bin.methods import authenticate
from bin.methods import get_api_data
from bin.methods import get_products_by_category
from bin.methods import create_user
from bin.methods import create_result_df
from bin.methods import get_category_id
import pandas as pd
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the value of an environment variable
currency_url = os.getenv('CURRENCY_URL')
start_date = os.getenv('START_DATE')
end_date = os.getenv('END_DATE')
name = os.getenv('NAME')
password = os.getenv('PASSWORD')
email = os.getenv('EMAIL')
avatar = os.getenv('AVATAR')

def main():
    currency_df = get_api_data(currency_url, start_date, end_date)

    access_token, refresh_token = authenticate(email, password)
    if access_token is None:
        user_id = create_user(name, email, password, avatar)
        print(f"New user created with ID {user_id} . Starting processing data")
        access_token, refresh_token = authenticate(email, password)
    else:
        print("Authentication sucessful using an existing user")

    if access_token is not None:
        category_id = get_category_id(category_name="Shoes", access_token=access_token)
        filtered_products = get_products_by_category(category_id, access_token, refresh_token)
        data_df = pd.DataFrame(filtered_products)
        data_df = data_df.rename(columns=lambda x: x.lower())
        data_df['currency'] = 'USD'
        data = create_result_df(data_df, currency_df)
        return data

    else:
        print("Error authenticating")

if __name__ == "__main__":
    main()