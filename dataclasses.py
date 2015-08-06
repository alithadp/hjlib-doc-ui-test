class Tab:
	def __init__(self, name, order, dropdown, components):
		self.name = name
		self.order = order # number representing its position in the navigation bar
		self.dropdown = dropdown # name of dropdown menu this tab is under, if applicable
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

class Question:
	def __init__(self, name, answer):
		self.name = name # the question
		self.answer = answer # list where each element is a list of (type, string) tuples containing the answer

class ExternalLink:
	def __init__(self, name, link):
		self.name = name
		self.link = link

class InternalLink:
	def __init__(self, name, link=""):
		self.name = name
		self.link = link

class Description:
	def __init__(self, description, links):
		self.description = description
		self.links = links # list of ExternalLinks