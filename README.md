## Project Description
This web application is based on python programming language and wrriten based on FastAPI web framework. Used uvicorn as the webserver and PostgreSQL as the relational database.

This web application supports two main endpoints.
1) GET api/financial_data - It will list financial data
    -   Query Params:
        - start_date (Optional: Default - 14 days before today)
        - end_date (Optional: Default - Today)
        - symbol (Optiona: Default - 'IBM')
        - limit (Optional: Default - 5)
        - page (Optional: Default - 1)

    -   Response
        ```json
        {
            "data": [
                {
                    "symbol": "IBM",
                    "date": "2023-04-18",
                    "open_price": "128.14",
                    "close_price": "127.78",
                    "volume": "3193787"
                },
                {
                    "symbol": "IBM",
                    "date": "2023-04-17",
                    "open_price": "128.3",
                    "close_price": "127.82",
                    "volume": "3657929"
                },
                {
                    "symbol": "IBM",
                    "date": "2023-04-14",
                    "open_price": "128.46",
                    "close_price": "128.14",
                    "volume": "4180614"
                },
                {
                    "symbol": "IBM",
                    "date": "2023-04-13",
                    "open_price": "128.01",
                    "close_price": "127.9",
                    "volume": "5621512"
                },
                {
                    "symbol": "IBM",
                    "date": "2023-04-12",
                    "open_price": "130.4",
                    "close_price": "128.54",
                    "volume": "3957542"
                }
            ],
            "pagination": {
                "count": 9,
                "page": 1,
                "limit": 5,
                "pages": 2
            },
            "info": {
                "error": ""
            }
        }
        ```

2) GET api/statistics - It will statistics data
    -   Query Params:
        - start_date (Required)
        - end_date (Required)
        - symbol (Required)

    -   Response
        ```json
        {
            "data": {
                "start_date": "2022-01-01",
                "end_date": "2024-01-14",
                "symbol": "IBM",
                "average_daily_open_price": 129.15,
                "average_daily_close_price": 128.71,
                "average_daily_volume": 4047018
            },
            "info": {
                "error": ""
            }
        }
        ```

## Tech stack
-   python3 - Python programming language.
-   FastAPI - WEB framework for building APIs in python.
-   uvicorn - ASGI web server implementation for Python. 
-   PostgreSQL - object-relational database system.

## How to run the code
1) Clone the repo

    ```bash
    git clone https://github.com/IshikaGodage/python_assignment.git
    ```
2) Change the directory to python_assignment

    ```bash
    cd python_assignment
    ```
3) Create and activate a python virtual environment (Optional - If already there skip to 4th step)

    ```bash
    pip install virtualenv
    python3 -m venv env
    source env/bin/activate
    ```
4) Install python libraries in local 

    ```bash
    pip install -r requirements.txt
    ```
5) Add a AlphaVintageAPIKeySecret and database urls in .env file
    
    ```bash
    vi config/.env

    AlphaVintageAPIKeySecret="<api-key>"

    DatabaseURLLocal="postgresql://postgres:postgres@localhost:5432/finance_db"
    
    DatabaseURL="postgresql://postgres:postgres@database:5432/finance_db"
    ```
    Note: For this assignemnt .env file won't be icluded in to the .gitignore 
6) Run the application

    ```bash
    docker-compose up
    ```
6) Open a new terminal from the same directory (python_assignment)
7) Run get_raw_data.py to read the data from Alpha Vintage API and Insert in to the database

    ```bash
    source env/bin/activate
    python3 get_raw_data.py 
    ```

7) Access the endpoints

    ```bash
    curl -X GET 'http://0.0.0.0:5000/api/financial_data?start_date=2023-04-01&end_date=2025-05-01&symbol=IBM&limit=2&page=1'

    curl -X GET 'http://0.0.0.0:5000/api/statistics?start_date=2023-04-01&end_date=2025-05-01&symbol=IBM'
    ```

## How to maintain AlphaVantage API key
-   API key should be kept in the config/.env file.
-   .env file should not be pushed to github, Hence need to add .env in .gitignore file