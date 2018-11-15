from destinations import csvfile
from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from requests.exceptions import ConnectionError
from configurator.jsonrpc import RPCconfig

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
    except ConnectionError as e:
        myRpc = '{protocol}://{host}:{port}{path}'.format(
                protocol=myConfig.get_protocol(),
                host=myConfig.get_host(),
                port=myConfig.get_port(),
                path=myConfig.get_path())
        print('Trouble connecting to Monero RPC at: ' + myRpc)


    return mywallet

def csv(mywallet):
    csvfile.etl(mywallet)

def SQL(mywallet):
    print('Yet to be developed')

def beanCounter(mywallet):
    print('Yet to be developed')

def main():

    mywallet = source()

    destinations = {'csv' : csv,
                    'SQL' : SQL,
                    'beanCounter' : beanCounter}

    destination = input("Specify the target destination (csv): ")

    if destination:
        destinations[destination](mywallet)
    else:
        destinations['csv'](mywallet) #default

    print(destination + " ETL action completed.")

    print("Please donate for further development")
    print("")


