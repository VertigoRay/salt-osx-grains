import json
import salt.modules.cmdmod
import salt.utils
import urllib

# Name of NVRAM Named Variable storing Asset Tag info:
asset_name = 'asset'

__salt__ = {
    'cmd.run': salt.modules.cmdmod._run_quiet,
    'cmd.run_all': salt.modules.cmdmod._run_all_quiet,
}

def _osx_grains():
    '''
    Return custom grains for OS X
    '''
    
    grains = {}
    
    awk = salt.utils.which('awk')
    grep = salt.utils.which('grep')
    ioreg = salt.utils.which('ioreg')
    last = salt.utils.which('last')
    nvram = salt.utils.which('nvram')
    sort = salt.utils.which('sort')
    sysctl = salt.utils.which('sysctl')
    uniq = salt.utils.which('uniq')

    grains['model'] = __salt__['cmd.run']('%(sysctl)s hw.model' % {'sysctl':sysctl}).split(': ')[1]
    
    grains['serial'] = __salt__['cmd.run']("%(ioreg)s -l | %(awk)s '/IOPlatformSerialNumber/ {print $4;}'" % {'ioreg':ioreg, 'awk':awk}).replace('"', '')

    asset = __salt__['cmd.run_all']("%(nvram)s %(asset)s" % {'nvram':nvram, 'asset':asset_name})
    if asset['retcode'] == 0:
        grains[asset_name] = asset['stdout'].split('\t')[1]

    else:
        grains[asset_name] = None

    console_users = {}
    for line in __salt__['cmd.run']("%(last)s | %(awk)s 'match($2, /console/) {print $1}' | %(sort)s | %(uniq)s -c | %(sort)s -nr" % {'last':last, 'awk':awk, 'sort':sort, 'uniq':uniq}).splitlines():
        l = line.strip().split(' ')
        console_users[l[1]] = l[0]

    console_user = __salt__['cmd.run']("%(last)s | %(grep)s 'still logged in' | %(awk)s 'match($2, /console/) {print $1, $3, $4, $5, $6}'" % {'last':last, 'grep':grep, 'awk':awk}).split(' ', 1)

    ttys000_users = {}
    for line in __salt__['cmd.run']("%(last)s | %(awk)s 'match($2, /ttys000/) {print $1}' | %(sort)s | %(uniq)s -c | %(sort)s -nr" % {'last':last, 'awk':awk, 'sort':sort, 'uniq':uniq}).splitlines():
        l = line.strip().split(' ')
        ttys000_users[l[1]] = l[0]

    ttys000_user = __salt__['cmd.run']("%(last)s | %(grep)s 'still logged in' | %(awk)s 'match($2, /ttys000/) {print $1, $3, $4, $5, $6}'" % {'last':last, 'grep':grep, 'awk':awk}).split(' ', 1)

    grains['users'] = {
        'console':{
            'current':{
                'accountname': console_user[0],
                'logontime': console_user[1],
            },
            'history':console_users,
        },
        'ttys000':{
            'current':{
                'accountname': ttys000_user[0],
                'logontime': ttys000_user[1],
            },
            'history':ttys000_users,
        },
    }

    grains['wtfismyip'] = {}
    for k, v in json.load(urllib.urlopen('http://wtfismyip.com/json')).iteritems():
        grains['wtfismyip'][k.replace('YourFucking', '')] = v

    return grains

def add_grains():
    '''
    Get kernel name and run the function if it matches.
    '''

    if salt.utils.is_darwin():
        return _osx_grains()
