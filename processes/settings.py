# General settings
oldExtension = '.old'
revertedExtension = '.reverted'
tmpExtension = '.tmp'
directory = 'configurations'

# FTP settings
ftpHost = '10.189.4.129'
ftpBasePath = '/application-configurations/'
ftpUser = None
ftpPassword = None
try:
	from settings_local import *
except:
	pass
