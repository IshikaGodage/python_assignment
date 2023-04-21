import uvicorn
from fastapi import FastAPI
from model import setup_db

from config.config import DBInfo
from financial.services import get_financial_data_service, get_statistics_data_service

app = FastAPI()

setup_db(DBInfo.DatabaseURL)

@app.get("/api/financial_data")
async def financial_data(start_date: str | None = None, end_date: str | None = None, symbol: str | None = None, limit: int = 5, page: int = 1):
    result = get_financial_data_service(start_date, end_date, symbol, limit, page)
    return result

@app.get("/api/statistics")
async def statistics(start_date: str, end_date: str, symbol: str):
    result = get_statistics_data_service(start_date, end_date, symbol)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
    