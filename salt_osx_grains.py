import salt.modules.cmdmod
import salt.utils

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
    
    sysctl = salt.utils.which('sysctl')
    ioreg = salt.utils.which('ioreg')
    awk = salt.utils.which('awk')
    nvram = salt.utils.which('nvram')

    grains['model'] = __salt__['cmd.run']('%s hw.model' % sysctl).split(': ')[1]
    
    grains['serial'] = __salt__['cmd.run']("%s -l | %s '/IOPlatformSerialNumber/ {print $4;}'" % (ioreg, awk)).replace('"', '')

    asset = __salt__['cmd.run_all']("%(nvram)s %(asset)s" % {'nvram':nvram, 'asset':asset_name})
    if asset['retcode'] == 0:
        grains[asset_name] = asset['stdout'].split('\t')[1]

    else:
        grains[asset_name] = None

    return grains

def add_grains():
    '''
    Get kernel name and run the function if it matches.
    '''

    if salt.utils.is_darwin():
        return _osx_grains()
