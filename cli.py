import argparse
import sys
from config import Config
from bot import BasicBot
from logger import setup_logger

logger = setup_logger()

def display_balance(bot):
    """Display account balance"""
    balance = bot.get_balance()

    if not balance:
        print("Failed to retrieve balance")
        return

    print("\n" + "="*60)
    print(" ACCOUNT BALANCE")
    print("="*60)

    for asset in balance:
        available = float(asset['availableBalance'])
        if available > 0:
            print(f"{asset['asset']:8} - Available: {available:>15,.4f}")

    print("="*60 + "\n")

def display_price(bot, symbol):
    """Display current price"""
    price = bot.get_current_price(symbol)

    if price:
        print(f"\n Current {symbol} Price: ${price:,.2f}\n")
    else:
        print(f"\n Failed to get price for {symbol}")

def display_open_orders(bot, symbol=None):
    """Display open orders"""
    orders = bot.get_open_orders(symbol)
    
    if orders is None:
        print(" Failed to retieve orders")
        return

    if not orders:
        print("\n No open orders\n")
        return
    
    print("\n" + "="*60)
    print(f" OPEN ORDERS ({len(orders)})")
    print("="*60)

    for order in orders:
        print(f"Order ID: {order['orderId']}")
        print(f"  Symbol: {order['symbol']}")
        print(f"  Side: {order['side']}")
        print(f"  Type: {order['type']}")
        print(f"  Quantity: {order['origQty']}")
        print(f"  Price: {order.get('price', 'MARKET')}")
        print(f"  Status: {order['status']}")
        print("-" * 60)
    
    print()

def main():
    """Main CLI entry point"""

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Check balance
    python cli.py --action balance

    # Get current price
    python cli.py --action price --symbol BTCUSDT

    # Place market buy order
    python cli.py --action buy --amount 0.01 --type market

    # Place limit sell order
    python cli.py --action sell --amount 0.01 --type limit --price 95000

    # View Open orders
    python cli.py --action orders

    # Cancel order
    python cli.py --action cancel BTCUSDT --order-id 123456
        """
    )

    parser.add_argument(
        '--action',
        required=True,
        choices=['buy', 'sell', 'balance', 'orders', 'cancel', 'price'],
        help='Action to perform'
    )

    parser.add_argument(
        '--symbol',
        default='BTCUSDT',
        help='Trading pair symbol (default: BTCUSDT)'
    )

    parser.add_argument(
        '--amount',
        type=float,
        help='Quantity to trade'
    )

    parser.add_argument(
        '--type',
        choices=['market', 'limit'],
        default='market',
        help='Order type (default: market)'
    )

    parser.add_argument(
        '--price',
        type=float,
        help='Price for limit orders'
    )

    parser.add_argument(
        '--order-id',
        type=int,
        help='Order ID for cancellation'
    )

    args = parser.parse_args()

    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"\n Configuration Error: {e}\n")
        sys.exit(1)

    # validate action-specific inputs
    if args.action in ['buy', 'sell']:
        if not args.amount or args.amount <= 0:
            print("Error: --amount must be a positive number")
            sys.exit(1)
        
        if args.type == 'limit' and (not args.price or args.price <= 0):
            print("Error: Limit orders require --price")
            sys.exit(1)

    if args.action == 'cancel' and not args.order_id:
        print("Error: Cancel action requires --order-id")
        sys.exit(1)
    
    # initialize bot
    try:
        print("\n Initializing Binance Futures Trading Bot...")    
        bot = BasicBot(
            api_key=Config.API_KEY,
            api_secret=Config.SECRET_KEY
        )
        print("\nBot Initialized successfully\n")
    except Exception as e:
        print(f"\nFailed to initialize bot: {e}\n") 
        sys.exit(1)

    # Execute actioni
    try:
        if args.action == 'balance':
            display_balance(bot)

        elif args.action == 'price':
            display_price(bot, args.symbol)

        elif args.action == 'orders':
            display_open_orders(bot, args.symbol)

        elif args.action == 'cancel':
            bot.cancel_order(args.symbol, args.order_id)
        
        elif args.action in ['buy', 'sell']:
            side = args.action.upper()

            if args.type == 'market':
                bot.place_market_order(args.symbol, side, args.amount)

            elif args.type == 'limit':
                bot.place_limit_order(args.symbol, side, args.amount, args.price)

    except KeyboardInterrupt:
        print("\n Operation Cancelled by user \n")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\nUnexpected error during execution: {e}\n")
        print(f"\n Error: {e}\n")
        sys.exit(1)
 
if __name__ == '__main__':
    main()