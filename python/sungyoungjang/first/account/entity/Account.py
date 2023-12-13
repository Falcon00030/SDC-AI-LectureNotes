class Account:
    # 생성자
    #Account::Account(std::string accountId, std::string password)
    #                                   : accountId(accountId), password(password) {~~~~~}
    def __init__(self, accountId, password):
        self.__accountId = accountId
        self.__password = password

    def getAccountId(self):
        return self.__accountId

    def setAccountId(self, accountId):
        self.__accountId = accountId


    def getPassword(self):
        return self.__password

    def setPassword(self, password):
       self.__password = password

    # print(인스턴스) 할 때 자동으로 아래 내용을 출력
    def __str__(self):
        return f"Account ID: {self.__accountId}, Password: {self.__password}"