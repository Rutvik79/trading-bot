import logging

def setup_logger(): 
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelnaem)s | %(message)s",
        handlers=[
            logging.FileHandler('trading_bot.log'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)