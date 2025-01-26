from enum import Enum


class ErrorMessageCodes(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"


class Ip_Type(Enum):
    LOCAL = "local"
    EXTERNAL = "external"


class RoleEnum(str, Enum):
    User = 1
    Admin = 2
    SuperAdmin = 3


class TokenType(int, Enum):
    EmailVerificationToken = 1
    ForgotPasswordToken = 2


class Environment(str, Enum):
    TEST = "test"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

    def __str__(self):
        return self.value


class StockSymbol(str, Enum):
    # Stocks
    AAPL = "APPLE"
    MSFT = "MICROSOFT"
    GOOGL = "GOOGLE"
    AMZN = "AMAZON"
    TSLA = "TESLA"

    # Cryptocurrencies
    BTCUSD = "BTC/USD"  # Bitcoin to USD
    ETHUSD = "ETH/USD"  # Ethereum to USD

    # Forex pairs
    EURUSD = "EUR/USD"  # Euro to US Dollar
    GBPUSD = "GBP/USD"  # British Pound to US Dollar
    USDJPY = "USD/JPY"  # US Dollar to Japanese Yen
    XAUUSD = "XAU/USD"  # Gold to US Dollar


class GujaratCities(str, Enum):
    AHMEDABAD = "Ahmedabad"
    SURAT = "Surat"
    VADODARA = "Vadodara"
    RAJKOT = "Rajkot"
    BHAVNAGAR = "Bhavnagar"
    JAMNAGAR = "Jamnagar"
    JUNAGADH = "Junagadh"
    GANDHINAGAR = "Gandhinagar"
    ANAND = "Anand"
    MEHSANA = "Mehsana"
    NAVSARI = "Navsari"
    BHARUCH = "Bharuch"


class TimeLimit(int, Enum):
    thirty_seconds = 30  # 30 seconds
    one_minute = 60  # 1 minute
    two_minutes = 120  # 2 minutes
    five_minutes = 300  # 5 minutes
