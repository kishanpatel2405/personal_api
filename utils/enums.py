from enum import Enum


class ErrorMessageCodes(Enum):
    SYSTEM_ERROR = "SYSTEM_ERROR"
    IP_RETRIEVAL_FAILED = "IP_RETRIEVAL_FAILED"
    SYSTEM_METRICS_FAILED = "SYSTEM_METRICS_FAILED"
    SYSTEM_UPTIME_FAILED = "SYSTEM_UPTIME_FAILED"
    DISK_USAGE_FAILED = "DISK_USAGE_FAILED"
    NETWORK_STATS_FAILED = "NETWORK_STATS_FAILED"
    BAD_REQUEST = "BAD_REQUEST"
    NOT_FOUND = "NOT_FOUND"


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
    BTCUSD = "BTC/USD"
    ETHUSD = "ETH/USD"

    # Forex
    EURUSD = "EUR/USD"
    GBPUSD = "GBP/USD"
    USDJPY = "USD/JPY"
    XAUUSD = "XAU/USD"


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


class Currency(str, Enum):
    INR = "₹"  # Indian Rupee
    USD = "$"  # US Dollar
    EUR = "€"  # Euro
    GBP = "£"  # British Pound
    JPY = "¥"  # Japanese Yen
    CNY = "¥"  # Chinese Yuan
    KRW = "₩"  # Korean Won
    BTC = "₿"  # Bitcoin
    PHP = "₱"  # Philippine Peso
    THB = "฿"  # Thai Baht
    VND = "₫"  # Vietnamese Dong
    NGN = "₦"  # Nigerian Naira
    RUB = "₽"  # Russian Ruble
    TRY = "₺"  # Turkish Lira
