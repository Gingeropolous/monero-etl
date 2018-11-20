from targets.target import *
from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from requests.exceptions import ConnectionError
from configurator.jsonrpc import RPCconfig

__version__ = '0.0.2'

def source():
    myConfig = RPCconfig.configure()

    try:
        jsonRPC = JSONRPCWallet(myConfig.get_protocol(), myConfig.get_host(), myConfig.get_port(), myConfig.get_path(), myConfig.get_user(), myConfig.get_password())
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)

    try:
        mywallet = Wallet(jsonRPC)
        return mywallet
    except ConnectionError as e:
        myRpc = '{protocol}://{host}:{port}{path}'.format(
                protocol=myConfig.get_protocol(),
                host=myConfig.get_host(),
                port=myConfig.get_port(),
                path=myConfig.get_path())
        print('Trouble connecting to Monero RPC at: ' + myRpc)
        return e

def main():

    try:
        mywallet = source()
    except:
        print(mywallet)

    targets = {'csv' : csvfile,
                    'SQL' : SQL,
                    'beanCounter' : beanCounter}

    target = input("Specify the target storage format (csv): ")
    currency = input("Specify the target currency (USD, XMR, BTC, etc): ")

    if target and currency:
        targets[target](mywallet, currency=currency)
    else:
        targets['csv'](mywallet) #default

    print(target + " ETL action completed.")

    print("Please donate for further development")


