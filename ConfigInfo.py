# coding: utf-8
import random
import string
class chainType :
    def __init__(self,symbol,precision,supply,fee):
        self.symbol=symbol
        self.precision = precision
        self.supply = supply
        self.fee = fee


class ConfigInfo():
    link = ""
    #link相关
    btc_generatetoaddress = "18mxqHAVVGaeTA5EameqMweqUUibBaWXLh"
    btc_tunnel_address = "mpi7hJ9XfQ9NJVsPNHrZ8Z14FfvtmV4J4d"
    btc_withdrawaddress= "14j9ryw3HCBW2eEp2jBBP4o7wCt8oCtE2g"
    btc_tunnel_account = "lktest001"
    btc_url = "http://192.168.1.121:60019"
    # btc_url = "http://192.168.1.121:60011"
    precision = 0.0000001

    ltc_generatetoaddress = "LRdiVwfhwcbDrXsSjkvPY9CQtV77svny7D"
    ltc_tunnel_address = "mqkGydvaYtK9G5oqJhb9QnBjJt125YMit4"
    ltc_withdrawaddress = "Lc3EkVUg8LAudJGKCD5ZNkNeY9hShHib6y"
    ltc_tunnel_account = "lktest002"
    ltc_url = "http://192.168.1.121:60020"
    # ltc_url = "http://192.168.1.121:60012"

    ub_generatetoaddress = "32eXjj3esajY9LYPC22oc5i1j6m56uSt1n"
    ub_tunnel_address = "3Nfs6CEEeQyEUc5s3GfffTGTZghqRJbevt"
    ub_withdrawaddress = "3PBeocrRQ8ZmTkyY3868LzdHzjaRy6bgtC"
    ub_tunnel_account = "lktest003"
    # ltc_url = "http://192.168.1.124:60014"
    ub_url = "http://192.168.1.124:23466"


    link_url = "http://127.0.0.1:50321"
    Link_senator = "lktest002"
    lock_account = "lklock"
    senator_account = "aquila"
    miner_account ="citizen0"

    lock_contract_account=["lock1","lock2","lock3"]
    lock_contract_n = 3
    symbols =  [chainType("BTC",8,210000000,100000),chainType("LTC",8,840000000,100000),chainType("HC",8,860000000,1000000),chainType("ETH",8,10000000000,200000)]
    cold_wallet = "coldwallet.txt"
    caller_name = "hyper-exchange"
    BTC_account_name = "lktest001"
    gas_price = "0.001"
    gas_limit = 10000
    gpc_path = "E:/coding/data/cotract/nofm_contract.gpc"
    first_contract_param =["init_config", '"multisignature_contract,3,2,HXNUWGgmxyLy1VpXN3F6vEVWWTL86negEi46,HXNURNJN62g2N9AAxQx5FKSuJrtCq3sexD9v,HXNZvmcErDutQsCTziWq72i7TR92TpoHs6yr"']

