import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

load_dotenv(find_dotenv())

@dataclass(frozen=True)
class APIkeys:
    AlphaVintageAPIKeySecret: str = os.getenv('AlphaVintageAPIKeySecret')

@dataclass(frozen=True)
class DBInfo:
    DatabaseURL: str = os.getenv('DatabaseURL')
    DatabaseURLLocal: str = os.getenv('DatabaseURLLocal')