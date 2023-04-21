import logging
import sqlalchemy as db
from datetime import date
from decimal import Decimal
from sqlalchemy import asc
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
  
# Create the Metadata Object
metadata_obj = db.MetaData()
engine = None
  
# database name
financial_data = db.Table(
    'financial_data',                                        
    metadata_obj,                                 
    db.Column('id', db.Integer, primary_key=True),  
    db.Column('symbol', db.String(16)),                    
    db.Column('date', db.Date),
    db.Column('open_price', db.String),  
    db.Column('close_price', db.String), 
    db.Column('volume', db.Integer), 
    db.UniqueConstraint("symbol", "date", name="unique_symbol_date"),               
)

def setup_db(database_url: str) -> None:
    """
    Setup db and create tables in not exists
    """
    engine = db.create_engine(database_url, echo=True)
    metadata_obj.create_all(engine)

def get_db_session(database_url: str) -> None:
    """
    Return database session
    """
    global engine
    session = None
    if engine:
        session = Session(bind=engine)
    else:
        engine = db.create_engine(database_url, echo=True)
        session = Session(bind=engine)
    return session

def bulk_insert(list_of_financial_data: list, database_url: str) -> None:
    """
    Insert list of enties to the databse
    """
    try:
        from sqlalchemy.dialects.postgresql import insert as upsert
        stmt = upsert(financial_data).values(list_of_financial_data)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["symbol", "date"]
        )
        session = get_db_session(database_url)
        session.execute(stmt)
        session.commit()
    finally:
        session.close()

def get_all(database_url: str) -> list:
    """
    Return list of all financial data
    """
    try:
        session = get_db_session(database_url)
        data = session.query(financial_data).all()
        return data
    finally:
        session.close()

def get_financial_data_by_date_range_and_symbol(start_date: date, end_date: date, symbol: str, limit: int, offset: int, database_url: str) -> Query:
    """
    Return Query object by given start_date, end_date_symbol, limit and offset.
    """
    session = get_db_session(database_url)
    qry = session.query(financial_data).filter(financial_data.c.symbol==symbol, financial_data.c.date.between(start_date, end_date)).order_by(asc(financial_data.c.date)).limit(limit).offset(offset)
    return qry

def get_total_count_by_date_range_and_symbol(start_date: date, end_date: date, symbol: str, database_url: str) -> int:
    """
    Return number of all entries by given start_date, end_date_symbol.
    """
    session = get_db_session(database_url)
    count = session.query(financial_data).filter(financial_data.c.symbol==symbol, financial_data.c.date.between(start_date, end_date)).count()
    return count

def get_statistic_data_by_date_range_and_symbol(start_date: date, end_date: date, symbol: str, database_url: str) -> tuple:
    """
    Return tuple of open_price_sum, close_price_sum, volume_sum by start_date, end_date and symbol
    """
    session = get_db_session(database_url)
    qry1 = session.query(financial_data.c.open_price).filter(financial_data.c.symbol==symbol, financial_data.c.date.between(start_date, end_date))
    qry2 = session.query(financial_data.c.close_price).filter(financial_data.c.symbol==symbol, financial_data.c.date.between(start_date, end_date))
    qry3 = session.query(financial_data.c.volume).filter(financial_data.c.symbol==symbol, financial_data.c.date.between(start_date, end_date))

    open_price_sum = 0
    close_price_sum = 0
    volume_sum = 0

    for open_price in qry1:
        open_price_sum = open_price_sum + Decimal(open_price[0])
  
    for close_price in qry2:
        close_price_sum = close_price_sum + Decimal(close_price[0])
    
    for volume in qry3:
        volume_sum = volume_sum + int(volume[0])

    logging.info(open_price_sum, close_price_sum, volume_sum)
    return (open_price_sum, close_price_sum, volume_sum)
