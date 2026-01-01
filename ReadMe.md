# Binance Futures Trading Bot (Testnet)

This is a simple Python CLI trading bot built for Binance Futures Testnet (USDT-M).
It allows placing market, limit and stop-limit orders and checking account details using the Binance API.

NOTE: This project is for learning purpose only and works only on Binance Futures Testnet.


## Features
- Get account info and balance
- Get current price of a symbol
- Place Market orders
- Place Limit orders
- Place Stop-Limit orders
- View open orders
- Cancel orders
- CLI based (menu + command arguments)


## Requirements
- Python 3.8+
- pip
- Binance Futures Testnet account


## Setup Instructions
### 1. Clone the repository
```bash
 git clone https://github.com/Rutvik79/trading-bot.git
 cd trading-bot/cli_app
```
### 2. Create virtual environment (optional but recommended)
```bash
python -m venv venv

#Windows
venv\Scripts\activate

#Mac/Linux
source venv/bin/activate
```
### 3. Install dependencies
```
pip install -r requirements.txt
```


## Binance Testnet Configuration
**1. Create Testnet Account**
- Go to: https://testnet.binancefutures.com/
- Register using Google or GitHub
- Test account comes with fake USDT balance

**2. Generate API Keys**
- Go to API Key section
- Generate HMAC_SHA256 keys
- Copy API Key and Secret Key

**3. Create .env file**
Create a .env file inside cli_app/ folder:
```.env
BINANCE_FUTURES_API_KEY=your_api_key_here
BINANCE_FUTURES_SECRET_KEY=your_secret_key_here
```


## Running the Application
Option 1: Interactive Menu Mode
```bash
python cli.py
```
You will see a menu like:
```bash
1. Get Account Info
2. Get Balance
3. Get Current Price
4. Place Market Order
5. Place Limit Order
6. Place Stop-Limit Order
7. View Open Orders
8. Cancel Order
9. Exit
```
Follow the prompts to perform actions.

Option 2: Command Line Mode
Examples:
```bash
# Get balance
python cli.py --action balance

# Get BTC price
python cli.py --action price --symbol BTCUSDT

# Market Buy
python cli.py --action buy --amount 0.01 --type market --symbol BTCUSDT

# Limit sell
python cli.py --action sell --amount 0.01 --type limit --price 95000 --symbol BTCUSDT 

# Stop-Limit order
python cli.py --action buy --amount 0.01 --type stop-limit --stop-price 90000 --price 90500 --symbol BTCUSDT

# View Open orders
python cli.py --action orders

# Cancel order
python cli.py --action cancel --symbol BTCUSDT --order-id 123456789
```


## Project Structure
```bash
trading-bot/
│
├── cli_app/
│   ├── bot.py            # Trading logic
│   ├── cli.py            # Main entry file
│   ├── helpers.py        # Helper functions
│   ├── config.py         # API config
│   ├── logger.py         # Logging setup
│   ├── requirements.txt
│   └── .env              # API keys (not committed)
│
└── README.md
```


## Notes
- This bot uses Binance Futures Testnet only
- All trades use fake funds
- Logging is stored in trading_bot.log
- Make sure you run the script from the cli_app folder
  

## Disclaimer
This project is created only for educational purposes.
Do not use this with real trading accounts.


## Author
Rutvik
GitHub: https://github.com/Rutvik79