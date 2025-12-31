from binance import Client
from logger import setup_logger
from binance.exceptions import BinanceAPIException
from binance.enums import ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET, TIME_IN_FORCE_GTC
from datetime import datetime

logger = setup_logger()

class BasicBot:

    def __init__(self, api_key, api_secret, testnet=True):
        # init binance client
    
        self.client = Client(api_key, api_secret, testnet=testnet)

        # set future url
        self.client.API_URL = 'https://testnet.binancefuture.com'
        # self.client.API_URL = 'https://demo-fapi.binance.com'

        logger.info(f"BasicBot initialized (Testnet: {testnet})")
        logger.info(f"Using API URL: {self.client.API_URL}")

    def get_account_info(self):
        try:
            logger.info("Fetching account information...")
            account = self.client.futures_account()

            logger.info("Account info retrieved successfully")
            return account
        except BinanceAPIException as e:
            logger.error(f"API Error getting account info: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting account info: {e}")
            return None
        
    def get_balance(self):
        """
        Get account balance

        Returns:
            list: list of asset balances
        """

        try: 
            logger.info("Fetching account balance...")
            balance = self.client.futures_account_balance()

            logger.info(f"Retrieved balance for {len(balance)} assets")
            return balance
        except BinanceAPIException as e:
            logger.error(f"API Error getting balance: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting balance: {e}")
            return None
    
    def get_current_price(self, symbol):
        """ 
        Get current market price for a symbol

        Args:
            symbol (str): Trading pair symbol (eg. 'BTCUSDT')

        Returns:
            float: Current price or None if error
        """

        try: 
            logger.info(f"Fetching current price for {symbol}...")
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])

            logger.info(f"Current {symbol} price: ${price:,.2f}")
            return price
        except BinanceAPIException as e:
            logger.error(f"API Error getting price for {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting price: {e}")
            return None

    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order (buy/sell at current price)
        
        Args:
            symbol (str): Trading pair (eg. 'BTCUSDT')
            side (str): 'BUY' or 'SELL' 
            quantity(float): Ammount to trade

        Returns: 
            dict: Order details or None if error
        """
        try:
            # Validate inputs
            if side not in ['BUY', 'SELL']:
                raise ValueError("Side must be 'BUY' or 'SELL'")
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            
            # log request details
            logger.info(f"Request - Symbol: {symbol}, Side: {side}, "
                        f"Type: {ORDER_TYPE_MARKET}, Quantity: {quantity}")
            
            # place the order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity,
            )

            # log response
            logger.info(f"Response - Order ID: {order['orderId']}, "
                        f"Status: {order['status']}")
            logger.info(f"Market order executed successfully")

            self._print_order_details(order)

            return order
        
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e}")
            return None
        
        except ValueError as e:
            logger.error(f"Validation Error: {e}")
            return None
        
        except Exception as e:
            logger.error(f"Unexpected error placing market order: {e}")
            return None
        
    def place_limit_order(self, symbol, side, quantity, price):
        """
            Place a limit order (buy/sell at specific price)

            Args:
                symbol (str): Trading pair
                side (str): 'BUY' or 'SELL'
                quantity (float): Ammount to trade
                price (float): Limit price

            Returns:
                dict: Order details or None if error
        """
        try:
            # Validate inputs
            if side not in ['BUY', 'SELL']:
                raise ValueError("Side must be 'BUY' or 'SELL'")
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            if price <= 0:
                raise ValueError("Price must be positive")
            
            logger.info(f"Placing LIMIT {side} order: {quantity} {symbol} @ ${price}")
            # log request details
            logger.info(f"Request - Symbol: {symbol}, Side: {side}, "
                        f"TYPE: {ORDER_TYPE_LIMIT}, Quantity: {quantity}, Price: {price}")
            
            # place the order
            order = self.client.futures_limit_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC, # Good Till Cance
                quantity=quantity,
                price=price,
            )

            # log response
            logger.info(f"Response - Order ID: {order['orderId']}, "
                        f"Status: {order['status']}")
            logger.info(f"Limit order placed successfully!")

            self._print_order_details(order)

            return order

        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e}")
            return None
        except ValueError as e:
            logger.error(f"Validation Error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error placing limit order: {e}")
            return None
        
    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        """  
        Place a STOP-LIMIT order on Binance USDT-M Futures Testnet.
        Triggers a LIMIT order when the stop price is reached.

        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Amount to trade
            stop_price (float): Trigger price
            limit_price (float): Limit price after trigger

        Returns:
            dict: Order details or None if error
        """

        try:

            # Validate inputs
            if side not in ["BUY", "SELL"]:
                raise ValueError("Side must be 'BUY' or 'SELL'")
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            if stop_price <= 0 or limit_price <= 0:
                raise ValueError("Prices must be positive")

            logger.info(
                f"Placing STOP-LIMIT {side} order: {quantity} {symbol} "
                f"(Stop: {stop_price}, Limit: {limit_price})"
            )

            # Place STOP-LIMIT order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP",                 # STOP-LIMIT (NOT algo)
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=limit_price,           # LIMIT price
                stopPrice=stop_price,        # Trigger price
                # workingType="MARK_PRICE"     # or 'CONTRACT_PRICE'
            )
            print("order details: ", order)
            order['orderId'] = order.get('orderId') or order.get('algoId')
            order['status'] = order.get('status') or order.get('algoStatus')

            
            # Log response
            logger.info(
                f"Response - Order ID: {order['orderId']}, "
                f"Status: {order['status']}"
            )
            logger.info("Stop-Limit order placed successfully")

            # Print formatted output
            self._print_order_details(order)

            return order

        except BinanceAPIException as e:
            logger.error(f"Binance API Error placing stop-limit order: {e}")
            return None

        except ValueError as e:
            logger.error(f"Validation Error: {e}")
            return None

        except Exception as e:
            logger.error(f"Unexpected error placing stop-limit order: {e}")
            return None

    def get_open_orders(self, symbol=None):
        """  
        Get all open orders

        Args:
            symbol (str, optional): Filter by symbol

        Returns:
            list: list of open orders
        """
        try:
            logger.info(f"Fetching open orders {' for ' + symbol if symbol else ''}...")
            orders = self.client.futures_get_open_orders(symbol=symbol)

            logger.info(f"Found {len(orders)} open orders")
            return orders
        except BinanceAPIException as e:
            logger.error(f"API Error getting open orders: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting open orders: {e}")
            return None

    def cancel_order(self, symbol, order_id):
        """  
            Cancel an open order

        Args: 
            symbol (str): Trading pair
            order_id (int): Order ID to cancel

        Returns:
            dict: Cancellation result or None if error
        """
        try: 
            logger.info(f"Cacelling order {order_id} for {symbol}...")
            result = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )

            logger.info(f"Order {order_id} cancelled successfully")
            return result
        except BinanceAPIException as e:
            logger.error(f"API error cancelling order: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error cancelling order: {e}")
            return None

    def _print_order_details(self, order):
        """ 
        Print formatted order details to console

        Args:
            order (dict): Order Information
        """

        print("\n" + "="*60)
        print(" ORDER EXECUTION DETAILS")
        print("="*60)
        print(f"Order ID:          {order.get('orderId')}")
        print(f"Symbol:            {order.get('symbol')}")
        print(f"Side:              {order.get('side')}")
        print(f"Type:              {order.get('type')}")
        print(f"Status:            {order.get('status')}")
        print(f"Quantity:          {order.get('origQty')}")
        print(f"Expected Qty:      {order.get('executedQty', 'N/A')}")

        if order.get('price'):
            print(f"Price:             ${float(order.get('price')):,.2f}")
        if order.get('avgPrice'):
            print(f"Avg Price:         ${float(order.get('avgPrice')):,.2f}")

        print(f"Time:              {datetime.fromtimestamp(order.get('updateTime', 0)/1000)}")
        print("="*60 + "\n")