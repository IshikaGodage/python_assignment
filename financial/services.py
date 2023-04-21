import logging
import math
import json
from datetime import datetime, date, timedelta
from config.config import DBInfo
from financial.utils import validate_date, validate_date_range, validate_count, validate_limit_and_page
from model import get_financial_data_by_date_range_and_symbol, get_total_count_by_date_range_and_symbol, get_statistic_data_by_date_range_and_symbol

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')


def get_financial_data_service(start_date: str | None, end_date: str | None, symbol: str | None, limit: int, page: int) -> json:
    """
    Return result json object of financial data by given start_date, end_date, symbol, limit and page.
    If Exception, it returns the result json with error message'
    """
    result = {
        "data": [],
        "pagination": {},
        "info": {'error': ''}
    }

    try:
        if start_date:
            validate_date(start_date)
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        else:
            # set default start date as 14 days back from today
            start_date = date.today() - timedelta(days=14)

        if end_date:
            validate_date(end_date)
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            # set default end_date as today
            end_date = date.today()

        validate_date_range(start_date, end_date)

        # set default symbol as IBM
        if not symbol:
            symbol = "IBM"

        count = get_total_count_by_date_range_and_symbol(start_date, end_date, symbol, DBInfo.DatabaseURL)
        validate_count(count,start_date,end_date,symbol)
        validate_limit_and_page(limit, page, count)

        pages = math.ceil(count/limit)
        offset = limit * (page - 1)
        rows = get_financial_data_by_date_range_and_symbol(start_date, end_date, symbol, limit, offset, DBInfo.DatabaseURL)

        # Populating the resoponse
        data = []
        pagination = {}
        for row in rows:
            row_data = {
                "symbol": row.symbol,
                "date": row.date,
                "open_price": str(row.open_price),
                "close_price": str(row.close_price),
                "volume": str(row.volume)
            }
            data.append(row_data)

        pagination['count'] = count
        pagination['page'] = page
        pagination['limit'] = limit
        pagination['pages'] = pages

        result['data'] = data
        result['pagination'] = pagination

        return result

    except Exception as e:
        logging.error(f'An exception occurred: {e}')
        # Populating the resoponse with error info
        error = {'error': str(e)}
        result['info'] = error
        return result


def get_statistics_data_service(start_date: str | None, end_date: str | None, symbol: str | None) -> json:
    """
    Return result json object of financial data by given start_date, end_date and symbol.
    If Exception, it returns the result json with error message'
    """
    result = {
        "data": {},
        "info": {'error': ''}
    }

    try:
        validate_date(start_date)
        validate_date(end_date)
        validate_date_range(start_date, end_date)

        count = get_total_count_by_date_range_and_symbol(start_date, end_date, symbol, DBInfo.DatabaseURL)
        validate_count(count,start_date,end_date,symbol)

        row = get_statistic_data_by_date_range_and_symbol(start_date, end_date, symbol, DBInfo.DatabaseURL)
        
        # Populating the resoponse
        data = {}
        data["start_date"] = start_date
        data["end_date"] = end_date
        data["symbol"] = symbol
        data["average_daily_open_price"] = round(row[0]/count, 2)
        data["average_daily_close_price"] = round(row[1]/count, 2)
        data["average_daily_volume"] = round(row[2]/count)

        result['data'] = data
        return result

    except Exception as e:
        logging.error(f'An exception occurred: {e}')
        # Populating the resoponse with error info
        error = {'error': str(e)}
        result['info'] = error
        return result
