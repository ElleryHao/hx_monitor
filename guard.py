# coding=utf-8
from base_core import *
from CommonFunctions import *
from ConfigInfo import *

def update_asset(type):

    senators = get_all_senators()

    for senator in senators:
        out = run_command("update_asset_private_keys", [senator[0], type, True])
    sleep_until_nextblock()

def vote() :
    ids = get_proposal_for_voter_id_list(ConfigInfo.senator_account)
    vec = {}
    senators = get_senator_addr()
    senators.remove("HXNcrswvwQa8asEdNAWYMQGxaEqAGDCqiZce")
    senators.remove("HXNgaNKK88asWCCkKMgRCkM5Pz47hxEjnfcf")
    vec["key_approvals_to_add"] = senators
    for id in ids:
        run_command("approve_proposal", [ConfigInfo.senator_account, id, vec, True])


def create_senator(account):
    ret = get_account_address(account)
    if ret == "LNK111111111111111111113MQ7LD" :
        ret = create_account(account)
    register_account(account)
    # miner
    run_command("create_senator_member",[ConfigInfo.senator_account,account,"","100000",True])
    sleep_until_nextblock()
    ids=get_proposal_for_voter_id_list(ConfigInfo.senator_account)
    vec = {}
    vec["key_approvals_to_add"] = [get_senator_addr()]
    for id in ids:
        run_command("approve_proposal",[ConfigInfo.senator_account,id,vec,True])
    sleep_until_nextblock()
    vec["key_approvals_to_add"] = [get_miner_addr()]
    ids = get_proposal_for_voter_id_list(ConfigInfo.miner_account)
    for id in ids :
        run_command("approve_proposal", [ConfigInfo.senator_account, id, vec, True])
    sleep_until_nextblock()

def update_multisig_address() :
    types=["BTC","LTC","HC"]
    for type in types :
        update_asset(type)
        sleep_until_nextblock()
        hot_cold = get_multisig_account_pair(1, type)
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

def senator_sign_transaction() :
    count = 0
    out = run_command("get_crosschain_transaction", [1])
    res = result_from_out(out)
    count = count + 1
    txids_after = []
    for tx in res:
        ops = tx[1]["operations"]
        op_id = ops[0][0]
        if op_id == 62:
            txids_after.append((ops[0][1].get("asset_symbol"),tx[0]))
    txid = ""
    index=1
    for (type,txid) in txids_after:
        senators = get_hotcold_senator_name(index, type)
        for gud in senators:
            if is_my_account(gud) is False :
                continue
            out = run_command("senator_sign_crosschain_transaction", [txid, gud])
    sleep_until_nextblock()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "more args needed"
        exit(1)

    if sys.argv[1] == "sign" :
        while True:
            time.sleep(10)
            senator_sign_transaction()
