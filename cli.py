import argparse
import sys
from config import Config
from bot import BasicBot
from logger import setup_logger

logger = setup_logger()

def main():
    """Main CLI entry point"""

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples
    # Place market buy order
    python cli.py --action buy --amount 0.01 --type market

    # Place limit sell order
    python cli.py --action sell --amount 0.01 --type limit --price 95000
        """
    )

    parser.add_argument(
        '--action',
        required=True,
        choices=['buy', 'sell'],
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
        if args.action in ['buy', 'sell']:
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