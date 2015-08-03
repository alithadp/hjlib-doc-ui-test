class Tab:
	def __init__(self, name, listDictionary, categoryList):
		self.name = name
		self.listDictionary = listDictionary
		self.categoryList = categoryList

class Category:
	def __init__(self, name, description):
		self.name = name
		self.description = description
		self.constructs = []

	def addConstruct(self, construct):
		self.constructs.append(construct)

class Construct:
	def __init__(self, name, description):
		self.name = name
		self.javaname = ""
		self.description = description
		self.javadocs = []
		self.usedwith = []
		self.methods = []
		self.related = {}

	def addLink(self, link):
		self.javadocs.append(link)

	def addMethod(self, method):
		self.methods.append(method)

	def addUsedWith(self, usedwith):
		self.usedwith.append(usedwith)

class Link:
	def __init__(self, name, link):
		self.name = name
		self.link = link
	def toString(self):
		return str(self.name) + " (" + str(self.link) + ")"

class Method:
	def __init__(self, method, description):
		self.method = method
		self.description = description
	def toString(self):
		return str(self.method) + " | " + str(self.description)

def getTestCat(tag):

	testCat = Category("Actors" + tag, "this is the category")
	#add one construct
	con1 = Construct("Actor" + tag, "Actor-Message_T", "does stuff description")
	javalink = Link("google" + tag,"www.google.com")
	method = Method("start" + tag,"does starting")
	con1.addLink(javalink)
	con1.addMethod(method)
	con1.addUsedWith("usedwithstuff" + tag)

	# add second construct
	con2 = Construct("construct" + tag, "Actor-Message_T", "does stuff description")
	javalink = Link("yahoo" + tag,"www.yahoo.com")
	method = Method("method" + tag,"does method thing")
	con2.addLink(javalink)
	con2.addMethod(method)
	con2.addUsedWith("usedwith" + tag)

	testCat.addConstruct(con1)
	testCat.addConstruct(con2)
	return testCat

def getTestCategories():
	categories = []
	categories.append(getTestCat("1"))
	return categories
	


