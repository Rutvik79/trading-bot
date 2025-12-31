from logger import setup_logger
import sys
import argparse

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

def display_account_info(bot):
    """Display full account information"""
    account = bot.get_account_info()

    if not account:
        print("Failed to retrieved info")
        return

    print("\n" + "="*60)
    print("ACCOUNT INFORMATION")
    print(f"Total Walllet Balance: ${float(account.get('totalWalletBalance', 0)):,.2f}")
    print(f"Total Unrealized PNL:  ${float(account.get('totalUnrealizedProfit', 0)):,.2f}")
    print(f"Available Balance:     ${float(account.get('availableBalance', 0)):,.2f}")
    print(f"Toatl Margin Balance:  ${float(account.get('totalMarginBalance', 0)):,.2f}")
    print(f"Max Withdraw Amount:   ${float(account.get('maxWithdrawAmount', 0)):,.2f}")
    print("\n" + "="*60)

def get_user_input(prompt, input_type=str, allow_empty=False):
    """Get and validate user input"""
    while True:
        try:
            value = input(prompt).strip()
            if not value and allow_empty:
                return None

            if not value:
                print("Input cannot be empty. Please try again")
                continue

            if input_type == float:
                return float(value)
            elif input_type == int:
                return int(value)
            else:
                return value

        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}")
        except KeyboardInterrupt:
            print("\n\n Operation cancelled by user\n")
            return None
        
def menu_mode(bot):
    """Interactive menu mode"""

    while True:
        # Display menu
        print("\n" + "="*60)
        print("Binance Futures Trading Bot")
        print("="*60)
        print("1. Get Account Info")
        print("2. Get Balance")
        print("3. Get Current Price")
        print("4. Place Market Order")
        print("5. Place Limit Order")
        print("6. Place Stop-Limit Order")
        print("7. View Open Orders")
        print("8. Cancel Order")
        print("9. Exit")
        print("="*60)

        choice = input("\n Select an option (1-9): ").strip()

        try:
            if choice == '1':
                # Get Account info
                display_account_info(bot)

            elif choice == '2':
                # Get Balance
                display_balance(bot)

            elif choice == '3':
                # Get curent Price
                symbol = get_user_input("Enter Symbol (eg. BTCUSDT): ", str).upper()
                if symbol:
                    display_price(bot, symbol)

            elif choice == '4':
                # Place Market Order
                print("\n--- Place Market Order ---")
                symbol = get_user_input("Enter symbol (eg. BTCUSDT): ", str).upper()
                if not symbol:
                    continue
            
                side = get_user_input("Enter side (BUY/SELL): ", str).upper()
                if side not in ['BUY', 'SELL']:
                    print("Invalid side. Must be BUY or SELL")
                    continue

                amount = get_user_input("Enter quantity: ", float)
                if not amount or amount <= 0:
                    print("Quantity must be positive")
                    continue

                confirm = input(f"\n Confirm {side} {amount} {symbol} at MARKET price? (yes/no): ").lower()
                if confirm == 'yes':
                    bot.place_market_order(symbol, side, amount)
                else: 
                    print("Order Cancelled.")

            elif choice == '5':
                # Place Limit Order
                print("\n --- Place Limit Order ---")
                symbol = get_user_input("Enter symbol (eg. BTCUSDT): ", str).upper()
                if not symbol: 
                    continue

                side = get_user_input("Enter side (BUY/SELL): ", str).upper()
                if side not in ['BUY', 'SELL']:
                    print("Invalid Side. Must be BUY or SELL")
                    continue

                amount = get_user_input("Enter quantity: ", float)
                if not amount or amount <= 0:
                    print("Quantity must be positive")
                    continue

                price = get_user_input("Enter limit price: ", float)
                if not price or price <= 0:
                    print("Price must be positive")
                    continue
                
                confirm = input(f"\n  Confirm {side} {amount} {symbol} at ${price}? (yes/no): ").lower()
                if confirm == 'yes':
                    bot.place_limit_order(symbol, side, amount, price)
                else:
                    print("❌ Order cancelled")

            elif choice == '6':
                # Place Stop-Limit Order
                print("\n --- Place Stop-Limit Order ---")
                symbol = get_user_input("Enter symbol (eg. BTCUSDT): ", str).upper()
                if not symbol: 
                    continue

                side = get_user_input("Enter side (BUY/SELL): ", str).upper()
                if side not in ['BUY', 'SELL']:
                    print("Invalid Side. Must be BUY or SELL")
                    continue

                amount = get_user_input("Enter quantity: ", float)
                if not amount or amount <= 0:
                    print("Quantity must be positive")
                    continue

                stop_price = get_user_input("Enter Stop price: ", float)
                if not stop_price or stop_price <= 0:
                    print("Stop price must be positive")
                    continue

                limit_price = get_user_input("Enter limit price: ", float)
                if not limit_price or limit_price <= 0:
                    print("Limit price must be positive")
                    continue

                confirm = input(f"\n Confirm {side} {amount} {symbol} (Stop: ${stop_price}, Limit: ${limit_price})? (yes/no): ").lower()
                if confirm == 'yes':
                    bot.place_stop_limit_order(symbol, side, amount, stop_price, limit_price)
                else: 
                    print("Order cancelled")

            elif choice == '7':
                # View Open Orders
                symbol = get_user_input("Enter symbol (press Enter for all): ", str, allow_empty=True)
                if symbol:
                    symbol = symbol.upper()
                display_open_orders(bot, symbol)

            elif choice == '8':
                # Cancel Order
                print("\n --- Cancel Order ---")
                symbol = get_user_input("Enter symbol: ", str).upper()
                if not symbol: 
                    continue
                
                order_id = get_user_input("Enter order ID: ", int)
                if not order_id:
                    continue

                confirm = input(f"\n Confirm cancel order {order_id} for {symbol}? (yes/no): ").lower()
                if confirm == 'yes':
                    bot.cancel_order(symbol, order_id)
                else:
                    print("Cancellation aborted")
                
            elif choice == '9':
                # Exit
                print("\n Thank you for using Binance Futures Trading Bot!")
                print("="*60 + "\n")
                sys.exit(0)

            else: 
                print("\n Invalid option. Please select 1-9.")
        
        except KeyboardInterrupt:
            print("\n\n Returning to main menu... \n")
        except Exception as e:
            logger.error(f"Error in menu mode: {e}")
            print(f"\n Error: {e}\n")

def command_mode():
    """Direct command mode with arguments"""

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Interactive menu mode (no arguments)
    python cli.py

    # Direct Command mode (with arguments):

    # Check Account Information
    python cli.py --action info

    # Check balance
    python cli.py --action balance

    # Get current price
    python cli.py --action price --symbol BTCUSDT

    # Place market buy order
    python cli.py --action buy --amount 0.01 --type market

    # Place limit sell order
    python cli.py --action sell --amount 0.01 --type limit --price 95000

    # Place stop-limit order
    python cli.py --action buy --amount 0.01 --type stop-limit --stop-price 90000 --price 90500

    # View Open orders
    python cli.py --action orders

    # Cancel order
    python cli.py --action cancel --symbol BTCUSDT --order-id 123456
        """
    )

    parser.add_argument(
        '--action',
        # required=True,
        choices=['buy', 'sell', 'balance', 'orders', 'cancel', 'price', 'info'],
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
        choices=['market', 'limit', 'stop-limit'],
        default='market',
        help='Order type (default: market)'
    )

    parser.add_argument(
        '--price',
        type=float,
        help='Price for limit/stop-limit orders'
    )

    parser.add_argument(
        '--stop-price',
        type=float,
        help='Stop price for stop-limit orders'
    )

    parser.add_argument(
        '--order-id',
        type=int,
        help='Order ID for cancellation'
    )

    args = parser.parse_args()

    if not args.action:
        return None
    
    # validate action-specific inputs
    if args.action in ['buy', 'sell']:
        if not args.amount or args.amount <= 0:
            print("Error: --amount must be a positive number")
            sys.exit(1)
        
        if args.type == 'limit' and (not args.price or args.price <= 0):
            print("Error: Limit orders require --price")
            sys.exit(1)

        if args.type == 'stop-limit':
            if not args.stop_price or args.stop_price <= 0:
                print("Error: Stop-limit orders require --stop-price")
                sys.exit(1)
            if not args.price or args.price <= 0:
                print("Error: Stop-limit orders require --price")
                sys.exit(1)

    if args.action == 'cancel' and not args.order_id:
        print("Error: Cancel action requires --order-id")
        sys.exit(1)

    return args