from enum import Enum


class CustomProtocol(Enum):
    ACCOUNT_REGISTER = 1
    ACCOUNT_LOGIN = 2
    ACCOUNT_LOGOUT = 3
    ACCOUNT_DELETE = 4

    PRODUCT_LIST = 5
    PRODUCT_REGISTER = 6
    PRODUCT_READ = 7
    PRODUCT_UPDATE = 8
    PRODUCT_DELETE = 9
