import platform
import salt.modules.cmdmod
import salt.utils

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

	grains['model'] = __salt__['cmd.run']('%s hw.model' % sysctl).split(': ')[1]
	grains['serial'] = __salt__['cmd.run']("%s -l | %s '/IOPlatformSerialNumber/ {print $4;}'" % (ioreg, awk)).replace('"', '')

	return grains

def add_grains():
	'''
	Get kernel name and run the function if it matches.
	'''

	osdata = {}
	(osdata['kernel'], osdata['nodename'], osdata['kernelrelease'], osdata['version'], osdata['cpuarch'], _) = platform.uname()

	if osdata['kernel'] == 'Darwin':
		return _osx_grains()
