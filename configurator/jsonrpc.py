import json
import sys
import os.path

cfg_dir = './cfg'


class RPCconfig(object):
    protocol = ""
    host = None
    port = None
    path = ""
    user = ""
    password = ""

    # constructor
    def __init__(self, protocol, host, port, path, user, password=''):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.path = path
        self.user = user
        self.password = password

    def get_protocol(self):
        return self.protocol

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_path(self):
        return self.path

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def configure():
        try:  # check to see if a configuration has already been set
            myconfig = read_config()
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

        if not myconfig:
            myconfig = set_config()  # when there is no config we need to set one

        if myconfig.get_user() != '':  # ask for password if a user is specified in the config
            password = input("Monero RPC Password needed to continue: ")
            myconfig.set_password(password)
        return myconfig


def read_config():
    global cfg_dir
    fname = cfg_dir + "/monero-wallet-rpc-config.json"
    if os.path.isfile(fname):
        with open(fname) as infile:
            cfg = json.load(infile)
            return RPCconfig(cfg['protocol'], cfg['host'], cfg['port'], cfg['path'], cfg['user'])
    else:
        return False  # file doesn't exist


def set_config():
    global cfg_dir
    print("Configuring RPC connection...")
    print("Press enter for defaults")
    userprotocol = input("Specify protocol (Default:http): ")
    if userprotocol != 'http' and userprotocol != 'https':
        userprotocol = 'http'
    userhost = input("Specify host (Default: 127.0.0.1): ")
    if not userhost:
        userhost = '127.0.0.1'
    userport = input("Specify port (Default: 18082): ")
    if not userport:
        userport = '18082'
    userpath = input("Specify path (Default: /json_rpc): ")
    if not userpath:
        userpath = '/json_rpc'
    userusername = input("Specify user (Default:empty): ")
    myconfig = RPCconfig(userprotocol, userhost, userport, userpath, userusername, None)
    print("Storing config in " + cfg_dir + "/monero-wallet-rpc-config.json")
    if os.path.isdir(cfg_dir) == False:
        os.mkdir(cfg_dir)
    with open('%s/monero-wallet-rpc-config.json' % (cfg_dir), 'w') as outfile:
        data = {
            'protocol': myconfig.get_protocol(),
            'host': myconfig.get_host(),
            'port': myconfig.get_port(),
            'path': myconfig.get_path(),
            'user': myconfig.get_user()
        }
        json.dump(data, outfile, sort_keys=True, indent=2, separators=(',', ': '))
        return myconfig