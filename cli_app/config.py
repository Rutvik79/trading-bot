import os
from dotenv import load_dotenv

# load env variables
load_dotenv()


class Config:
    # API Credentials
    API_KEY=os.getenv('BINANCE_FUTURES_API_KEY')
    SECRET_KEY=os.getenv('BINANCE_FUTURES_SECRET_KEY')


    @classmethod
    def validate(cls):
        """Validate API Keys are present"""
        if not cls.API_KEY or not cls.SECRET_KEY:
            raise ValueError(
                "API keys not found.\n"
                "Please create a .env file with:\n" 
                "BINANCE_FUTURES_API_KEY=your_key\n"
                "BINANCE_FUTURES_SECRET_KEY=your_secret"
            )
        
        return True
