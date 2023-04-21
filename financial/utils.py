import math
from datetime import date

def validate_date(date_text: str) -> None:
    """
    Validate the give str date.
    """
    try:
        date.fromisoformat(date_text)
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

def validate_date_range(start_date: date, end_date: date) -> None:
    """
    Compare the given start abd end date.
    """
    if  start_date > end_date:
        raise Exception(f"Incorrect date range: start_date: {start_date} is greter than end_date: {end_date}, start_date should be less than or equal end_date")

def validate_count(count: int, start_date: date, end_date: date, symbol: str) -> None:
    """
    Validate the count beween the given start, end dates and symbol.
    """
    if count == 0:
        raise Exception(f"Couldn't find data for the start date: {start_date}, end date: {end_date}, symbol: {symbol}")
    
def validate_limit_and_page(limit: int, page: int, count: int) -> None:
    """
    Validate the give limit and page.
    """
    if limit < 1:
        raise Exception(f"Incorrect value for query param <limit>, should be > 0")
    
    if page < 1:
        raise Exception(f"Incorrect value for query param <page>, should be > 0")
    elif page > math.ceil(count/limit):
        raise Exception(f"Incorrect value for query param <page>, should be <= total pages: {str(math.ceil(count/limit))}")