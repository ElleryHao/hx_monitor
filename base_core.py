# coding: utf-8
from __future__ import print_function
import socket
import time
import sys
import json
import functools
import os
import random
from ConfigInfo import *
import requests
#from CommonFunctions import *


BASE_DIR = os.path.abspath(os.curdir)



is_python3 = True if sys.version_info >= (3, 0) else False

def safeunicode(obj, encoding='utf-8'):
    r"""
    Converts any given object to unicode string.
        >>> safeunicode('hello')
        u'hello'
        >>> safeunicode(2)
        u'2'
        >>> safeunicode('\xe1\x88\xb4')
        u'\u1234'
    """
    t = type(obj)
    if t is unicode:
        return obj
    elif t is str:
        return obj.decode(encoding, 'ignore')
    elif t in [int, float, bool]:
        return unicode(obj)
    elif hasattr(obj, '__unicode__') or isinstance(obj, unicode):
        try:
            return unicode(obj)
        except Exception as e:
            return u""
    else:
        return str(obj).decode(encoding, 'ignore')

def sleep_seconds(seconds=0):
    time.sleep(seconds)



def recv_timeout(the_socket, timeout=2):
    the_socket.setblocking(0)
    total_data = []
    data = b''
    begin = time.time()

    while 1:
        # if you got some data, then break after wait sec
        # if you got some data, then break after wait sec
        # if len(total_data)>0 and (datetime.datetime.now() - begin).seconds > timeout:
        #     break
        # if you got no data at all, wait a little longer

        if (time.time() - begin) > timeout:
            print ("********time out,no data")
            print(total_data)
            break
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)

                try:
                    # print(total_data)
                    json.loads(''.join(total_data))

                    break
                except:
                    pass
            else:
                time.sleep(0.1)
        except:
            pass
    return b''.join(total_data)

def run_command(cmd, params=[], bprint = 1,url=ConfigInfo.link_url):
    json_cmd_obj = {'jsonrpc': '2.0', 'method': cmd, 'params': params or [], 'id': 1}
    if bprint ==1:
        pass
        #print(u"cmd: %s" % json.dumps(json_cmd_obj, ensure_ascii=False))
    bytesdata_origin = (json.dumps(json_cmd_obj, ensure_ascii=False) + u'\n')
    bytesdata = bytesdata_origin.encode('utf-8')

    payload = bytesdata
    headers = {
        'Content-Type': "text/plain",
        'authorization': "Basic YTpi",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    stdoutput = response.text
    if(bprint == 1):
        pass
        #print(stdoutput)
    if len(stdoutput)>0:
        code = code_from_out(stdoutput)
        if (code == 100):
            #print("erro cmd: %s" % json.dumps(json_cmd_obj, ensure_ascii=False))
            #print(stdoutput)
            #tassert(code != 0,"error happens")
            print(stdoutput)

    if len(stdoutput) == 0:
            print("@@@@@@@@error stdoutput =0 cmd: %s" % json.dumps(json_cmd_obj, ensure_ascii=False))
            print(stdoutput)

    return stdoutput


def operationId_from_out(out, keyname):
    try:
        jsonpara = json.loads(safeunicode(out))
        print("jsonpara = ", jsonpara)
    except Exception as e:
        print(e)
    #tassert(out.get('code', 0) == 0, out)
    result = json.loads(safeunicode(jsonpara['result']))
    print("result = ", result)
    ids = []
    for i in range(len(result)):
        itempara =json.loads(safeunicode(result[i]))
        print("item = ", itempara)
        ids.append(itempara[keyname])
    print("ids = ", ids)
    return ids

#output: {"id":1,"result":{"contract_name":"","id":"CON7LQJJDXqSyuoqyf6MJqadmdAzuiBq8sRT",
def key_from_out(out, keyname):
    try:
        out = json.loads(safeunicode(out))
        print("out = ",out)
    except Exception as e:
        print(e)
    #tassert(out.get('code', 0) == 0, out)
    result = out['result'][keyname]
    return result

def info_from_out(out, keyname):
    try:
        out = json.loads(safeunicode(out))
    except Exception as e:
         print(e)

    contract_name = out['result'][keyname]
    return contract_name

def result_from_out(out):
    try:
        out = json.loads(safeunicode(out))
        contract_id = out['result']
        return (contract_id)
    except Exception as e:
        print ("exception out=",out)
        print(e)
    #tassert(out.get('code', 0) == 0, out)




def code_from_out(out):
    try:
        out = json.loads(safeunicode(out))
        if out.get('error', None) or out.get('errors', None):
            return 100
        return out.get('code', 0)
    except Exception as e:
        print (out)
        print(e)


def gen_test_contract_name():
    return "test_con_%d" % ((int)(10000 * random.random()))

class RpcConnect():
        msocket = None


def connect():
    json_cmd_obj = {'jsonrpc': '2.0',  'id': 1,'method': 'login', 'params':[ConfigInfo.contract_user, ConfigInfo.contract_password]}
    RpcConnect.msocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RpcConnect.msocket.connect((ConfigInfo.contract_server,ConfigInfo.contract_port))
    RpcConnect.msocket.send(json.dumps(json_cmd_obj).encode('utf-8'))
    data = RpcConnect.msocket.recv(10240)
    if data:
        print(data)
    return RpcConnect.msocket

def close():
    RpcConnect.msocket.close()
def get_proposal_for_voter_id_list(account):

    out = run_command("get_proposal_for_voter", [account])
    res = result_from_out(out)
    ids = []
    for proposal in res:
        ids.append(proposal["id"])

    return ids
