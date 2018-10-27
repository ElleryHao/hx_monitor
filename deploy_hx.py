# coding=utf-8
'''
this script is just for the hx platform to be deployed
there will be several steps to be completed
1.create all symbols , btc ltc .eg
2.create multisignatures for all the symbols
3.register the first contract created as a mutisigature contract
'''



from base_core import *
from CommonFunctions import *
from ConfigInfo import *

def senator_update_asset(type):
    senators = get_all_senators()
    for senator in senators:
        out = run_command("update_asset_private_keys", [senator[0], type, True])
    sleep_until_nextblock()


def senator_create_symbols(symbols,precision,supply,fee):
    out = run_command("wallet_create_asset", [ConfigInfo.senator_account,symbols,precision,supply,fee,True])
    res = result_from_out(out)
    sleep_seconds(1)

def update_multisig_address() :
    symbols=ConfigInfo.symbols
    types=[]
    for symbol in symbols :
        types.append(symbol.symbol)
    for type in types :
        hot_cold = get_multisig_account_pair(1, type)
        if hot_cold is not None:
            continue
        senator_update_asset(type)
        hot_cold = get_multisig_account_pair(1, type)
        if hot_cold is None:
            continue
        out = run_command("account_change_for_crosschain", [ConfigInfo.senator_account, type, hot_cold["hot"],
                                                            hot_cold["cold"], "10000", True])
        # 之前没加这里的sleep 发现 effectnum会回滚的问题
        sleep_until_nextblock()
        out = run_command("get_proposal_for_voter", ["senator0"])
        result = result_from_out(out)
        id = result[0]["id"]
        senators = get_hotcold_senator_addr_byaddress(hot_cold["hot"], type)
        params = {
            "key_approvals_to_add": senators
        }
        out = run_command("approve_proposal", ["senator0", id, params, True])
        sleep_until_nextblock()
        out = run_command("get_multisig_account_pair", [type])
        res = result_from_out(out)
        print res
def deploy_first_contract() :
    contract_id = run_command("get_first_contract_address",[])
    contract_id = result_from_out(contract_id)
    contract_info = run_command("get_contract_info",[contract_id])
    contract_info = result_from_out(contract_info)
    if contract_info is not None :
        return
    run_command("register_contract",[ConfigInfo.caller_name,ConfigInfo.gas_price,ConfigInfo.gas_limit,ConfigInfo.gpc_path])
    sleep_until_nextblock()
    run_command("invoke_contract",[ConfigInfo.caller_name,ConfigInfo.gas_price,ConfigInfo.gas_limit,contract_id,"init_config",
                                   "multisignature_contract,3,2,HXNUWGgmxyLy1VpXN3F6vEVWWTL86negEi46,HXNURNJN62g2N9AAxQx5FKSuJrtCq3sexD9v,HXNZvmcErDutQsCTziWq72i7TR92TpoHs6yrx"])
    sleep_until_nextblock()



if __name__ == '__main__':
    # create symbols

    for symbol in ConfigInfo.symbols :
        senator_create_symbols(symbol.symbol,symbol.precision,symbol.supply,symbol.fee)
        sleep_seconds(1)
    #update multisignature for all symbols we need but ETH
    update_multisig_address()
    sleep_until_nextblock()

    #register contract
    deploy_first_contract()
    sleep_until_nextblock()



