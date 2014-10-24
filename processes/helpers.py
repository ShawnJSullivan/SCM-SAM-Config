from time import time
import os


class ConfigDeployer(object):
	"""
		This helper class assists in deploying configurations via FTP.
	"""

	def __init__(self, ftp, settings):
		self.ftp = ftp
		self.settings = settings
		self.currentTimestamp = str(int(time()))
		self.dirExists = False
		self.dirTmpExists = False
		self.latestArchiveTimestamp = None
		self._update_status()


	def revert(self):
		"""
			Revert the most recent deployment.
		"""
		self._sriahc_lacisum()


	def upload(self):
		"""
			Upload your local configurations to the temp directory.
		"""
		self._upload_temp()


	def deploy(self):
		"""
			Upload and deploy your local configurations.
		"""
		self._musical_chairs()


	def _update_status(self):
		"""
			Update the status of the remote directory.
		"""

		self.dirExists = False
		self.dirTmpExists = False
		self.latestArchiveTimestamp = None

		try:
			fileList = self.ftp.nlst()

			for line in fileList:
				self._process_directory_line(line)

		except:
			pass


	def _process_directory_line(self, line):
		"""
			Analyze lines from a directory list.
		"""

		if line == self.settings.directory:
			self.dirExists = True
		elif line == self.settings.directory+self.settings.tmpExtension:
			self.dirTmpExists = True

		filename = line.split('.')
		if filename[0] == self.settings.directory:
			if filename[-1] == self.settings.oldExtension[1:]:
				fileTimestamp = filename[-2]
				if not self.latestArchiveTimestamp or int(self.latestArchiveTimestamp) < int(fileTimestamp):
					self.latestArchiveTimestamp = fileTimestamp


	def _prepare_temp_directory(self):
		"""
			Prepare the temp configuration directory for an upload.
		"""
		self._update_status()
		if not self.dirTmpExists:
			print self.settings.directory+self.settings.tmpExtension
			self.ftp.mkd(self.settings.directory+self.settings.tmpExtension)


	def get_status(self):
		"""
			Output the current status of the configuration directory.
		"""
		if self.latestArchiveTimestamp is not None:
			latestArchive = self.settings.directory+'.'+self.latestArchiveTimestamp+self.settings.oldExtension
		else:
			latestArchive = 'N/A'

		return """%s
Config Folder Exists: %r
Temporary Folder Exists: %r
Latest Archive: %s
%s""" % (
			('=' * 40),
			self.dirExists,
			self.dirTmpExists,
			latestArchive,
			('=' * 40)
		)


	def _upload_temp(self):
		"""
			Upload local configuration JSON files to temp directory.

			Note: This is not recursive and only supports a depth of 1.
		"""
		localBasePath = os.path.realpath(os.getcwd()+'/configurations/')+'/'

		self._prepare_temp_directory()
		for root, dirs, files in os.walk(localBasePath):
			remoteBasePath = self.settings.directory+self.settings.tmpExtension+'/'
			currentPath = os.path.relpath(root, localBasePath)+'/'
			if currentPath != './':
				print 'FTP: Making "%s" directory.' % remoteBasePath+currentPath[:-1]
				self.ftp.mkd(remoteBasePath+currentPath[:-1])

			for f in files:
				if f.endswith('.json'):
					print 'FTP: Uploading "%s%s%s" to "%s%s%s"...' % (localBasePath, currentPath, f, remoteBasePath, currentPath, f)
					self.ftp.storlines('STOR %s%s%s' % (remoteBasePath, currentPath, f), open('%s%s%s' % (localBasePath, currentPath, f), 'rb'))
					print 'FTP: Upload complete.'


	def _musical_chairs(self):
		"""
			Directory musical chairs to move the current temp directory live.
		"""
		self._update_status()
		if self.dirExists:
			print 'FTP: Renaming "%s" to "%s"...' % (self.settings.directory, self.settings.directory+'.'+self.currentTimestamp+self.settings.oldExtension)
			self.ftp.rename(self.settings.directory, self.settings.directory+'.'+self.currentTimestamp+self.settings.oldExtension)
			print 'FTP: Rename complete.'

		print 'FTP: Renaming "%s" to "%s"...' % (self.settings.directory+self.settings.tmpExtension, self.settings.directory)
		self.ftp.rename(self.settings.directory+self.settings.tmpExtension, self.settings.directory)
		print 'FTP: Rename complete.'
		self._update_status()


	def _sriahc_lacisum(self):
		"""
			Reverse directory musical chairs to restore the last archived configuration.
		"""

		self._update_status()
		print 'FTP: Renaming "%s" to "%s"...' % (self.settings.directory, self.settings.directory+'.'+self.currentTimestamp+self.settings.revertedExtension)
		self.ftp.rename(self.settings.directory, self.settings.directory+'.'+self.currentTimestamp+self.settings.revertedExtension)
		print 'FTP: Rename complete.'

		print 'FTP: Renaming "%s" to "%s"...' % (self.settings.directory+'.'+self.latestArchiveTimestamp+self.settings.oldExtension, self.settings.directory)
		self.ftp.rename(self.settings.directory+'.'+self.latestArchiveTimestamp+self.settings.oldExtension, self.settings.directory)
		print 'FTP: Rename complete.'
		self._update_status()
