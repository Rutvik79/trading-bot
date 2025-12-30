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
                timestamp=datetime.now(),
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
        
    def _print_order_details(self, order):
        """ 
        Print formatted order details to console

        Args:
            order (dict): Order Information
        """

        print("\n" + "="*30)
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

        print(f"Time:              {datetime.fromtimestamp(order.get('updateTime', 0)/1000)}")
