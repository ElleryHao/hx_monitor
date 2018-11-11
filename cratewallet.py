from base_core import *
from CommonFunctions import *
from ConfigInfo import *

def export_private(type ):#miner or guard)
    out = []
    if type == 'citizen' :
        out = get_miners()
    elif type == 'senator':
        out = get_all_senators()

    for o in out :
        name = o[0]
        prk = get_private_key(name)
        print name ," ",prk
if __name__ == '__main__':
    #export_private('citizen')
    export_private('senator')

