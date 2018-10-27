# coding=utf-8
from base_core import *
from CommonFunctions import *
from ConfigInfo import *
def create_miner(account):
    ret = get_account_address(account)
    if ret == "LNK111111111111111111113MQ7LD" :
        ret = create_account(account)
    register_account(account)
    # miner
    run_command("create_miner",[account,"",True])
    sleep_until_nextblock()
    run_command("lock_balance_to_miner",[account,ConfigInfo.lock_account,"10000","LNK",True])
    sleep_until_nextblock()


