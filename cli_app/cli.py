import sys
from config import Config
from bot import BasicBot
from logger import setup_logger
from helpers import *

logger = setup_logger()


def main():
    """Main CLI entry point"""
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"\n Configuration Error: {e}\n")
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

    # Check if arguments provided (command mode) or no arguments (menu mode)
    args = command_mode()

    if args is None:
        # No arguments provided - use Interactive menu mode
        try:
            menu_mode(bot)
        except KeyboardInterrupt:
            print("\n\n Goodbye! \n")
            sys.exit(0)
    
    else:
    # Arguments Provided - use direct command moder
        try:
            if args.action == 'balance':
                display_balance(bot)

            elif args.action == 'info':
                display_account_info(bot)

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

                elif args.type == 'stop-limit':
                    bot.place_stop_limit_order(args.symbol, side, args.amount, args.stop_price, args.price)

        except KeyboardInterrupt:
            print("\n Operation Cancelled by user \n")
            sys.exit(0)

        except Exception as e:
            logger.error(f"\nUnexpected error during execution: {e}\n")
            print(f"\n Error: {e}\n")
            sys.exit(1)
    
if __name__ == '__main__':
    main()