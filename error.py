class Error(Exception):

	def __init__(self, message):
		self.message = message


class ParseError(Error):

	def __init__(self, message='Error'):
		self.message = message
