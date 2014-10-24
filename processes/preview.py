import os
import json
import time
import firefly_core.helpers
from firefly_core.config.helpers import ConfigServiceFlatFiles
from firefly_core.config.helpers_django import ConfigFactory


writeDirectory = '/tmp/application-configurations/'


class ConfigServiceFlatFilesLocal(ConfigServiceFlatFiles):
	"""
		Overrides the flat file config service class to open
		local config files rather than requesting them from a URL.
	"""
	def _get(self, configURL):
		configString = None
		try:
			with open(configURL, 'r') as fileStream:
				configString = fileStream.read()
			fileStream.close()
		except:
			pass

		# Decode the JSON
		if configString:
			config = json.loads(configString)
		else:
			config = None

		return config


"""
	Process environment parameters parameters
"""
if os.environ.get('environment'):
	environment = os.environ['environment']
else:
	environment = 'prod'

if os.environ.get('marketAlias'):
	marketAlias = os.environ['marketAlias']
else:
	marketAlias = 'default'

if os.environ.get('excludeAdditionalConfigs'):
	includeAdditionalConfigs = False
else:
	includeAdditionalConfigs = True

if os.environ.get('productNamespace'):
	productNamespace = os.environ['productNamespace']
else:
	productNamespace = 'default'

if os.environ.get('output'):
	output = os.environ['output']
else:
	output = 'file'

baseURL = os.path.realpath(os.path.dirname(os.path.abspath(__file__))+'/../configurations/')+'/'


"""
	Process configuration
"""
configServiceAPI = ConfigServiceFlatFilesLocal(baseURL=baseURL, timeout=60, environment=environment)
configFactory = ConfigFactory(configServiceAPI)
config = configFactory.create(marketAlias=marketAlias, productNamespace=productNamespace, includeAdditionalConfigs=includeAdditionalConfigs)


"""
	Output configuration
"""
if output == 'print':
	print json.dumps(config)
elif output == 'file':
	if not os.path.exists(writeDirectory):
		os.makedirs(writeDirectory)

	writeFile = writeDirectory+'preview-configuration_'+str(int(time.time()))+'.json'
	fileHandler = open(writeFile, 'w')
	fileHandler.write(json.dumps(config))
	fileHandler.close()

	print 'Config preview created at: '+writeFile
