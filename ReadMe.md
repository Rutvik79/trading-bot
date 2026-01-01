# Binance Futures Trading Bot (Testnet)

This is a simple Python CLI trading bot built for Binance Futures Testnet (USDT-M)/
It allows placing market, limit and stop-limit orders and checking account details using the Binance API.

NOTE: This project is for learning purpose only and works only on Binance Futures Testnet.

---

## Features
- Get account info and balance
- Get current price of a symbol
- Place Market orders
- Place Limit orders
- Place Stop-Limit orders
- View Open orders
- Cancel orders
- CLI based (menu + command arguments)

---

## Requirements
- Python 3.8+
- pip
- Binance Futures Testnet account

---

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

---