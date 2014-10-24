import unittest
import os
import json
import re

class ApplicationConfigTest(unittest.TestCase):
	"""
	"""

	def test_validJSON(self):
		"""
			Run through all the JSON files to confirm that they can be decoded.
		"""
		filePath = os.path.realpath(os.path.dirname(os.path.abspath(__file__))+'/../configurations/')

		for root, dirs, theFiles in os.walk(filePath):
			for theFile in theFiles:
				if theFile.endswith('.json'):
					filePath = '%s/%s' % (root, theFile)
					print 'Testing "%s"...' % filePath
					with open(filePath, 'r') as fileStream:
						content = fileStream.read()
					fileStream.close()

					self._jsonLoad(content)
					self._jsonNewLineEndOfFile(content)
					self._jsonYayForTabs(content)
					self._jsonYayForCleanLineEnds(content)


	def _jsonYayForTabs(self, content):
		"""
			Test that there aren't any dirty rotten spaces out there.
		"""

		for line in content.split('\n'):
			pattern = re.compile(r'\t*(?P<spaces> *)')
			matches = pattern.match(line)
			if matches.groupdict()['spaces']:
				self.fail('Spaces are the devil!')


	def _jsonYayForCleanLineEnds(self, content):
		"""
			Test that no line ends with a space or tab.
		"""

		self.assertNotIn(' \n', content)
		self.assertNotIn('\t\n', content)


	def _jsonNewLineEndOfFile(self, content):
		"""
			Test that the last line is "empty"
		"""

		self.assertEqual(content.endswith('\n\n'), False)
		self.assertEqual(content.endswith('\n'), True)


	def _jsonLoad(self, content):
		"""
			Test if the string can be loaded by the json package
		"""

		try:
			jsonObject = json.loads(content)
			self.assertEqual(isinstance(jsonObject, dict), True)
		except ValueError as e:
			self.fail('Invalid JSON')


if __name__ == '__main__':
	unittest.main()
