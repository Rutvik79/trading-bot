import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()

def get_binance_client():

    # API Credentials
    API_KEY=os.getenv('BINANCE_API_KEY')
    SECRET_KEY=os.getenv('BINANCE_SECRET_KEY')

    if not API_KEY or not SECRET_KEY:
        raise ValueError("API keys not found. Check your .env file")

    client = Client(API_KEY, SECRET_KEY, testnet=True)

    # Testnet url, base url
    client.FUTURES_URL = "https://testnet.binancefuture.com"

    return client