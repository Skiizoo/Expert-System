from display import display_parse_error, display_solve_error


class Error(Exception):

	def __init__(self, message):
		self.message = message


class ParseError(Error):

	def __init__(self, file, line, i, txt, j=None):
		self.file = file
		self.line = line
		self.i = i
		self.txt = txt
		self.j = j

	def __str__(self):
		return display_parse_error(self.file, self.line, self.i, self.txt, self.j)


class SolveError(Error):

	def __init__(self, file, func, line, txt):
		self.file = file
		self.line = line
		self.func = func
		self.txt = txt

	def __str__(self):
		return display_solve_error(self.file, self.func, self.line, self.txt)

