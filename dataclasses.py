class Tab:
	def __init__(self, name, components):
		self.name = name
		self.components = components

class Category:
	def __init__(self, name, description=None):
		self.name = name
		self.description = description
		self.components = []

class Construct:
	def __init__(self, name, javaname, description):
		self.name = name
		self.javaname = javaname
		self.description = description
		self.components = []

class Instruction:
	def __init__(self, name, description, steps):
		self.name = name
		self.description = description
		self.steps = steps # list where each element is a list of (type, string) tuples for that step

class ListGroup:
	def __init__(self, name, lists):
		self.name = name
		self.lists = lists # list of (title, list) tuples

class InlineList:
	def __init__(self, name, items):
		self.name = name
		self.items = items # list of ExternalLinks, InternalLinks, or plain text

class Table:
	def __init__(self, titles, rows):
		self.titles = titles
		self.rows = rows # list of lists that represent rows

class ExternalLink:
	def __init__(self, name, link):
		self.name = name
		self.link = link

class InternalLink:
	def __init__(self, name, link):
		self.name = name
		self.link = link

class Description:
	def __init__(self, description, links):
		self.description = description
		self.links = links # list of ExternalLinks