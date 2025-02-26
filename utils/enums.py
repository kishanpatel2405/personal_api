from enum import Enum


class ErrorMessageCodes(str, Enum):
    NOT_FOUND = "NOT_FOUND"


class ErrorMessageCodes(Enum):
    SYSTEM_ERROR = "SYSTEM_ERROR"
    IP_RETRIEVAL_FAILED = "IP_RETRIEVAL_FAILED"
    SYSTEM_METRICS_FAILED = "SYSTEM_METRICS_FAILED"
    SYSTEM_UPTIME_FAILED = "SYSTEM_UPTIME_FAILED"
    DISK_USAGE_FAILED = "DISK_USAGE_FAILED"
    NETWORK_STATS_FAILED = "NETWORK_STATS_FAILED"
    BAD_REQUEST = "BAD_REQUEST"


class Ip_Type(Enum):
    LOCAL = "local"
    EXTERNAL = "external"


class RoleEnum(str, Enum):
    User = 1
    Admin = 2


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


class Timezone(str, Enum):
    india_time = "Asia/Kolkata"
    america_time = "America/New_York"
    brazil_time = "America/Sao_Paulo"
    australia_time = "Australia/Sydney"
    canada_time = "America/Toronto"
    uk_time = "Europe/London"
    germany_time = "Europe/Berlin"
    france_time = "Europe/Paris"
    japan_time = "Asia/Tokyo"
    south_africa_time = "Africa/Johannesburg"
    china_time = "Asia/Shanghai"
    mexico_time = "America/Mexico_City"
    russia_time = "Europe/Moscow"
    egypt_time = "Africa/Cairo"
    spain_time = "Europe/Madrid"
    italy_time = "Europe/Rome"
    argentina_time = "America/Argentina/Buenos_Aires"
    singapore_time = "Asia/Singapore"
    indonesia_time = "Asia/Jakarta"
    nigeria_time = "Africa/Lagos"


class SupportedLanguages(str, Enum):
    en = "en"  # English
    es = "es"  # Spanish
    fr = "fr"  # French
    de = "de"  # German
    it = "it"  # Italian
    zh = "zh"  # Chinese
    hi = "hi"  # Hindi
    ar = "ar"  # Arabic
