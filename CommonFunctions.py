# coding: utf-8

from base_core import *
#-*- coding: UTF-8 -*-


def get_unspend_txs_from_txs(txs):
    vins = []
    vouts = []
    for tx in txs:
        txid = tx['txid']
        vout = tx['vout']
        vin = tx['vin']
        #  把vout和txid对应起来
        for out in vout:
            out['txid'] = txid
            vouts.append(out)
        #  把所有vin对应起来
        for initem in vin:
            if initem.get('vout') is None:
                continue  # coinbase ignore
            vins.append(initem)
    utxos = []
    #查找vout里的txid没有在vin中出现过
    for vout in vouts:
        index = vout['n']
        vout_txid = vout['txid']
        used = False
        for vin in vins:
            if vin['txid'] == vout_txid and vin['vout'] == index :
                used = True
                break
        if not used:
            utxos.append(vout)
        #返回所有未花费的余额，txid+vout
            # {
            #     "value": 16.67,
            #     "n": 0,
            #     "scriptPubKey": {
            #         "asm": "OP_DUP OP_HASH160 7fadfeebbee2c7d463a7afeed27fa641c5cc86f0 OP_EQUALVERIFY OP_CHECKSIG",
            #         "hex": "76a9147fadfeebbee2c7d463a7afeed27fa641c5cc86f088ac",
            #         "reqSigs": 1,
            #         "type": "pubkeyhash",
            #         "addresses": [
            #             "1Ce7FoVLKMnhssb1X4mQW32X6Tm8bd6Xb9"
            #         ]
            #     }
    return utxos

def get_address_balances_from_utxos(utxos):
    balances = {}
    for utxo in utxos:
        scriptPubKey = utxo['scriptPubKey']
        addresses = scriptPubKey.get('addresses', [])
        if len(addresses) < 1:
            continue
        address = scriptPubKey['addresses'][0]
        value = utxo['value']
        balances[address] = balances.get(address, 0) + value
    return balances

def get_txids(utxos,withdraw_address):
    balances = {}
    txids= []
    for utxo in utxos:
        scriptPubKey = utxo['scriptPubKey']
        addresses = scriptPubKey.get('addresses', [])
        if len(addresses) < 1:
            continue
        address = scriptPubKey['addresses'][0]
        if withdraw_address == address:
            txids.append(utxo["txid"])

    return txids

def get_block_count():
    p = RpcConnect.msocket
    out = run_command("info", [""], bprint=0)
    result = result_from_out(out)
    return result['head_block_num']

def get_private_key(account):
    p = RpcConnect.msocket
    out = run_command("dump_private_key", [account])
    result = result_from_out(out)
    return result[0][1]

def get_account_address(account):
    p = RpcConnect.msocket
    out = run_command("get_account", [account])
    result = result_from_out(out)
    return result.get("addr")
    #return ""

def sleep_until_nextblock():
    p = RpcConnect.msocket
    out = run_command("info", [""], bprint=0)
    result = result_from_out(out)
    curnum = result['head_block_num']
    while get_block_count()-curnum <1 :
        sleep_seconds(1)

def sleep_until_block(block_num):
    p = RpcConnect.msocket
    out = run_command(p, "info", [""], bprint=0)
    result = result_from_out(out)
    curnum = result['head_block_num']
    while get_block_count()-block_num <1 :
        sleep_seconds(1)

def get_account_name(addr):
    p = RpcConnect.msocket
    out = run_command(p, "list_my_accounts", [""], bprint=0)
    res = result_from_out(out)
    account_name = ""
    for item in res:
        if item["addr"] == addr:
            account_name = item["name"]
    return account_name

def create_account(account) :
    p = RpcConnect.msocket
    out = run_command("wallet_create_account", [account])
    res = result_from_out(out)
    return res
def register_account(account) :
    run_command("register_account", [account,True])
    sleep_until_nextblock()

def tassert(cond, msg=None, api=None):

    if not cond:
        if msg:
            print('assert error:', msg)
            raise Exception(msg)

def get_senator_addr():
    out = run_command("list_senator_members", ["", 100])
    res = result_from_out(out)
    senators = []
    for senator in res:
        out = run_command("get_senator_member", [senator[0]], bprint=0)
        member = result_from_out(out)
        if member["formal"] == True :
            out = run_command("get_account", [senator[0]], bprint=0)
            res = result_from_out(out)
            senators.append(res["addr"])
    random.shuffle(senators)
    return senators

def get_proposal_for_voter_id_list(account):

    out = run_command("get_proposal_for_voter", [account])
    res = result_from_out(out)
    ids = []
    for proposal in res:
        ids.append(proposal["id"])

    return ids

def get_miner_addr():
    out = run_command("list_citizens", ["", 100])
    res = result_from_out(out)
    miners = []
    for miner in res:
        out = run_command("get_account", [miner[0]], bprint=0)
        res = result_from_out(out)
        miners.append(res["addr"])
    random.shuffle(miners)
    return miners

def get_miners():
    out = run_command("list_citizens", ["", 100])
    res = result_from_out(out)
    return res

def get_all_senators():
    out = run_command("list_senator_members", ["", 15])
    res = result_from_out(out)
    return res
def get_multisig_account_pair(index,type):

    out = run_command("get_multisig_account_pair", [type],1)
    res = result_from_out(out)
    hot_cold = {}
    if len(res) < index:
        print ("!!!!!!pls check get_multisig_account_pair return value ")
        return None
    hot     = res[len(res)-index]["bind_account_hot"]
    cold    = res[len(res)-index]["bind_account_cold"]
    eff_num = res[len(res)-index]["effective_block_num"]

    hot_cold["hot"]=hot
    hot_cold["cold"]= cold
    hot_cold["eff_num"]= eff_num
    return hot_cold
def get_hotcold_senator_addr_byaddress(address,type):
    out = run_command("get_multi_account_senator", [address, type])
    res = result_from_out(out)
    senators = []
    for item in res:
        out = run_command("get_account", [item["guard_account"]], bprint=0)
        res2 = result_from_out(out)
        name = res2["addr"]
        senators.append(name)
    random.shuffle(senators)
    return senators[0:]

def get_multi_account_senator_name(index,type = "BTC"):
    hot_cold = get_multisig_account_pair(index, type)
    hot_address = hot_cold["hot"]
    out = run_command("get_multi_account_senator", [hot_address, type])
    res = result_from_out(out)
    name_list= []
    for item in res:
        out = run_command("get_account", [item["guard_account"]], bprint=0)
        res2 = result_from_out(out)
        name = res2["name"]
        name_list.append(name)
    return name_list

def get_hotcold_senator_name(index,type):
    senators = get_multi_account_senator_name(index,type)
    random.shuffle(senators)
    return senators

def approve_proposal(senator):
    out = run_command("get_proposal_for_voter", [senator])
    result = result_from_out(out)
    id = result[0]["id"]
    senators = get_senator_addr()
    params = {
        "key_approvals_to_add": senators
    }
    out = run_command("approve_proposal", ["senator0", id, params, True])
    sleep_until_nextblock()

if __name__ == '__main__':
    print  create_account("hzkai111")
