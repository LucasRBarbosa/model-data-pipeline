from bin.methods import authenticate
from bin.methods import get_api_data
from bin.methods import get_products_by_category
import pandas as pd

currency_df = get_api_data('https://sdw-wsrest.ecb.europa.eu/service/data/EXR', '2023-02-10', '2023-02-10')
print(currency_df.head())

access_token, refresh_token = authenticate("testing@gmail.com", "react123")

if access_token is not None:   
    category_id = 4  # In this case, 4 corresponds to the Shoes category
    filtered_products = get_products_by_category(category_id, access_token, refresh_token)
    if filtered_products is not None:
        df = pd.DataFrame(filtered_products)
        df = df.rename(columns=lambda x: x.lower())
        df['currency'] = 'USD'
        print(df.head())
        df.to_csv('testing_3.csv')
    else:
        print("Error retrieving products")
else:
    print("Error authenticating")


merged_df = pd.merge(df, currency_df[['currency', 'obs_value', 'time_period']], left_on='currency',right_on='currency', how='left')
merged_df['price_eur'] = merged_df['price'] / merged_df['obs_value']
merged_df.to_csv('end_result.csv')