import multiprocessing
import socket
from time import sleep
from decouple import config

from account_form.repository.AccountFormRepositoryImpl import AccountFormRepositoryImpl
from product_form.repository.ProductFormRepositoryImpl import ProductFormRepositoryImpl
# pip3 install python-decouple

from client_socket.repository.ClientSocketRepositoryImpl import ClientSocketRepositoryImpl
from client_socket.service.ClientSocketServiceImpl import ClientSocketServiceImpl
from console_printer.repository.ConsolePrinterRepositoryImpl import ConsolePrinterRepositoryImpl
from console_ui.repository.ConsoleUiRepositoryImpl import ConsoleUiRepositoryImpl
from console_ui.service.ConsoleUiServiceImpl import ConsoleUiServiceImpl
from custom_protocol.entity.CustomProtocol import CustomProtocol
from custom_protocol.service.CustomProtocolServiceImpl import CustomProtocolServiceImpl
from task_manage.repository.TaskManageRepositoryImpl import TaskManageRepositoryImpl
from task_manage.service.TaskManageServiceImpl import TaskManageServiceImpl


def initServerSocketDomain():
    clientSocketRepository = ClientSocketRepositoryImpl()
    ClientSocketServiceImpl(clientSocketRepository)


def initTaskManageDomain():
    taskManageRepository = TaskManageRepositoryImpl()
    TaskManageServiceImpl(taskManageRepository)


def initConsolePrinterDomain():
    consoleUiRepository = ConsoleUiRepositoryImpl()
    ConsoleUiServiceImpl(consoleUiRepository)


def initEachDomain():
    initServerSocketDomain()
    initTaskManageDomain()
    initConsolePrinterDomain()
    
    # initProductFormRepository()


def registerProtocol():
    customProtocolService = CustomProtocolServiceImpl.getInstance()
    accountFormRepository = AccountFormRepositoryImpl.getInstance()
    productFormRepository = ProductFormRepositoryImpl.getInstance()

    customProtocolService.registerCustomProtocol(
        CustomProtocol.ACCOUNT_REGISTER.value,
        accountFormRepository.createAccountRegisterForm
    )

    customProtocolService.registerCustomProtocol(
        CustomProtocol.ACCOUNT_LOGIN.value,
        accountFormRepository.createAccountLoginForm
    )

    customProtocolService.registerCustomProtocol(
        CustomProtocol.ACCOUNT_LOGOUT.value,
        accountFormRepository.createAccountLogoutForm
    )

    customProtocolService.registerCustomProtocol(
        CustomProtocol.ACCOUNT_DELETE.value,
        accountFormRepository.createAccountDeleteForm
    )

    customProtocolService.registerCustomProtocol(
        CustomProtocol.PRODUCT_LIST.value,
        productFormRepository.createProductListForm
    )

    customProtocolService.registerCustomProtocol(
        CustomProtocol.PRODUCT_REGISTER.value,
        productFormRepository.createProductRegisterForm
    )

    customProtocolService.registerCustomProtocol(
        CustomProtocol.PRODUCT_READ.value,
        productFormRepository.createProductReadForm
    )

    customProtocolService.registerCustomProtocol(
        CustomProtocol.PRODUCT_UPDATE.value,
        productFormRepository.createProductUpdateForm
    )

    customProtocolService.registerCustomProtocol(
        CustomProtocol.PRODUCT_DELETE.value,
        productFormRepository.createProductDeleteForm
    )


if __name__ == '__main__':
    print("\033[92m화면 출력 UI 서버가 구동되었습니다.")

    initEachDomain()
    registerProtocol()

    clientSocketService = ClientSocketServiceImpl.getInstance()

    clientSocketService.createClientSocket(config('TARGET_HOST'), int(config('PORT')))
    clientSocketService.connectToTargetHost()

    taskManageService = TaskManageServiceImpl.getInstance()

    lock = multiprocessing.Lock()
    transmitQueue = multiprocessing.Queue()
    receiveQueue = multiprocessing.Queue()

    taskManageService.createTransmitTask(lock, transmitQueue)
    taskManageService.createReceiveTask(lock, receiveQueue)
    taskManageService.createPrinterTask(transmitQueue, receiveQueue)

    while True:
        try:
            sleep(5.0)

        except socket.error:
            sleep(0.5)

