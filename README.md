# Ecommerce Project API
## Description

This Python project makes use of two APIs to retrieve data, specifically:

- European Central Bank's Statistical Data Warehouse API to obtain exchange rates
- A fake eCommerce API to retrieve products data
The program filters and retrieves all the products from the "Shoes" category, and creates a new pandas dataframe that includes the following information:

    - all products
    - price in USD
    - price in EUR
    - date of the exchange rate used

## Project Structure

Copy code
```
.
├── bin
│   └── methods.py
├── .env
├── .gitignore
├── main.py
├── Makefile
├── README.md
└── requirements.txt
```

- bin/methods.py: Contains the implementation of the methods required to execute the project.
- .env: Contains environment variables required to run the program.
- .gitignore: Contains files and folders to ignore in Git version control.
- main.py: Contains the main program code.
- Makefile: Contains commands to simplify common development tasks.
- README.md: Provides an overview of the project, how to set it up, and how to use it.
requirements.txt: Contains all the packages and dependencies needed to run the program.

## Getting Started
### Prerequisites

- Python 3.9 or higher installed
- pip3 installed

### Installation
Clone the repository:
```
git clone <repository-url>
Change directory to the project folder:
``` 
cd <project-folder>
Install the dependencies:
```
pip3 install -r requirements.txt
```

Create a .env file in the root directory, and set the following environment variables:
```
CURRENCY_URL=<currency-api-url>
START_DATE=<yyyy-mm-dd>
END_DATE=<yyyy-mm-dd>
NAME=<user-name>
PASSWORD=<user-password>
EMAIL=<user-email>
AVATAR=<user-avatar-url>

e.g
CURRENCY_URL='https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D..EUR.SP00.A'
START_DATE='2023-02-09'
END_DATE='2023-02-10'
NAME='testing12345'
PASSWORD='abcde12345'
EMAIL='testing12345@gmail.com'
AVATAR="https://api.lorem.space/image/face?w=640&h=480"

```
Run the program:
```
python3 main.py
```
## Usage

The program can be run by executing the main.py file which will give the main dataframe output. 

The program will authenticate the user using the given credentials, and obtain an access token. If the access token has expired, the program will refresh it using the refresh token. If a user does not exist with the given credentials, the program will create a new user with the given information.
