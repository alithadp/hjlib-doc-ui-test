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

import os.path
from whoosh.index import *
from whoosh.query import *
from whoosh.fields import *
from whoosh.qparser import MultifieldParser

class Search:
	def __init__(self, path):
		self.createIndex(path)
		self.index = open_dir(path)
		self.parser = MultifieldParser(["name", "javaname", "description"], self.index.schema)

	"""
	Creates a new index in the given pathname.
	"""
	def createIndex(self, path):
		schema = Schema(name=TEXT(stored=True), javaname=TEXT, link=ID(stored=True), description=TEXT)
		if not os.path.exists(path):
			os.mkdir(path)
		index = create_in(path, schema)

	"""
	Adds the given document (of type Category, Construct, Question, or Instruction) and corresponding link to the index.
	"""
	def addToIndex(self, document, link):
		writer = self.index.writer()
		if isinstance(document, Construct):
			javaname = document.javaname
		else:
			javaname = ""
		if isinstance(document, Question):
			description = document.answer
		elif document.description == None:
			description = ""
		else:
			description = document.description.description
		writer.add_document(name=unicode(document.name), javaname=unicode(javaname), link=unicode(link), description=unicode(description))
		writer.commit()

	"""
	Returns a list of results that match the given keywords.
	"""
	def searchIndex(self, keywords):
		with index.searcher() as searcher:
			query = self.parser.parse(keywords)
			results = searcher.search(query, limit=None)
		return results