## This is a Makefile for the "application-configurations".
## -------------------------------------------------------------------------------
## 
## List of commands:
## 

PYPI_HOST ?= pypi.gannett.com

## + (default) - Does nothing.
all:
	@echo 'MAKE: Doing nothing...'


## + help - Provides a list of callable "make" commands.
help:
	@grep -E '^##' Makefile | sed 's/## //g'


## + test - Runs tests.
test:
	@python processes/tests.py


## + deploy - Deploys your configurations.
deploy: upload-tmp deploy-tmp


## + upload-tmp - Uploads your local configurations to the temp folder.
upload-tmp: test
	@python processes/upload.py


## + deploy-tmp - If you have a temp folder uploaded.
deploy-tmp:
	@python processes/deploy.py


## + revert - Reverts your last configuration deployment.
revert:
	@python processes/revert.py


## + status - Outputs the status of the deployment server.
status:
	@python processes/status.py


## + preview - Generate a preview. See options below.
preview:
	@python processes/preview.py


## + preview-deps - Build the dependencies for the preview script.
preview-deps:
	pip install \
	--upgrade \
	-i http://${PYPI_HOST}/simple \
	--extra-index-url http://pypi.python.org/simple/ \
	firefly-core

## 
## -------------------------------------------------------------------------------
## 
## Preview parameters:
## 
## The "make preview" command accepts optional parameters. An example that uses
## Every optional parameter would look like this:
## 
##    make preview marketAlias=indystar environment=dev productNamespace=ios_ipad excludeAdditionalConfigs=true output=print
## 
## marketAlias (for example "indystar")
## Makes the configuration being generated specific to the provided market
## 
## environment (for example "dev")
## Makes the configuration being generated specific to the provided environment
## 
## productNamespace (for example "ios_ipad")
## Makes the configuration being generated specific to the provided namespace
## 
## excludeAdditionalConfigs
## If this parameter is set, additional configurations will not be included.
## This mimics how SAM consumes configurations internally.
## 
## output ("print" or "file")
## Determines the output method for the config preview.
## 
