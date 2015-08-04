from genshi.template import TemplateLoader
import os
import dataclasses as data
import xml.etree.ElementTree as ET

categoryToTab = {}
constructToCategory = {}
javaToConstruct = {}

def findNodesViaTag(root, tag):
	# return self if tag matches
	if root.tag == tag:
		return [root]
	# return none if no tag match and no children
	if len(root) <= 0 or root is None:
		return []
	# no tag found, but has children
	matches = []
	for child in root:
		if child.text is not None:
			matches += findNodesViaTag(child, tag)
	return matches

def getAttribute(node, key):
	if key in node.attrib:
		attrib = node.attrib[key]
	else:
		attrib = ""
	return str(attrib)

def getLinks(node):
	linkNodes = findNodesViaTag(node, "javadoc")
	if linkNodes == []:
		return []
	links = []
	for node in linkNodes:
		links.append(data.Link(getAttribute(node, "name"), node.text))
	return links

def getUsedWith(node):
	usedWithNodes = findNodesViaTag(node, "usedwith")
	if usedWithNodes == []:
		return []
	items = []
	for node in usedWithNodes:
		items.append(node.text)
	return items

def getMethods(node):
	methodList = []
	methodNodes = findNodesViaTag(node, "method")
	if methodNodes == []:
		return []
	for mynode in methodNodes:
		methodList.append(data.Method(getAttribute(mynode, "name"), mynode.text))
	return methodList

def getDescription(node):
	description = findNodesViaTag(node, "description")
	return description[0].text

def getOps(node):
	opsList = []
	opNodes = findNodesViaTag(node, "op")
	for node in opNodes:
		opsList.append(data.Method(getAttribute(node, "name"), node.text))
	return opsList

def getStep(node):
	if list(node) == []:
		return "<p>" + node.text + "</p>"
	html_string = ""
	components = []
	for elem in list(node):
		desc_text = elem.text.strip()
		if elem.tag =='description':
			linkNodes = findNodesViaTag(elem, "link")
			"""
			links = {}
			for node in linkNodes:
				links[node.text] = getAttribute(node, "url")
			components.append((elem.tag, elem.text, links))
			"""
			for link in linkNodes:
				old_text = link.text
				new_text = "<a href='" + getAttribute(link, "url") + "'>" + link.text + "</a>"
				desc_text = desc_text.replace(old_text, new_text)
			html_string = html_string + "<p>" + desc_text + "</p>"
		elif elem.tag == 'img':
			html_string = html_string + "<img src='" + desc_text + "'>"
		elif elem.tag == 'code':
			html_string = html_string + "<pre>" + desc_text + "</pre>"
		elif elem.tag == 'quote':
			# components.append((elem.tag, getStep(elem)))
			html_string = html_string + "<blockquote>" + getStep(elem) + "</blockquote>"
		"""
		else:
			components.append((elem.tag, elem.text))
		"""

	return html_string

def getInstruction(node):
	name = getAttribute(node, "name")
	stepList = []
	stepNodes = findNodesViaTag(node, "step")
	for step in stepNodes:
		stepList.append(getStep(step))
	return data.Instructions(name, stepList)

def getInstructionList(filename, tabname):
	tree = ET.parse(filename)
	root = tree.getroot()
	instructionNodes = findNodesViaTag(root, "instruction")
	instructionList = []
	for node in instructionNodes:
		instructionList.append(getInstruction(node))
	return data.Tab(tabname, [], [], instructionList)

def getList(node):
	name = getAttribute(node, 'name')
	items = []
	itemNodes = findNodesViaTag(node, "item")
	for node in itemNodes:
		items.append(node.text)
	return (name, items)

def getListGroup(filename, tabname):
	tree = ET.parse(filename)
	root = tree.getroot()
	listNodes = findNodesViaTag(root, "list")
	myLists = []
	for node in listNodes:
		myLists.append(getList(node))
	return data.Tab(tabname, myLists, [], [])

def getRelatedConstructs():
	tree = ET.parse('content/RelatedConstructs.xml')
	root = tree.getroot()
	pairNodeList = findNodesViaTag(root, "pair")
	relatedConstructsList = {}
	for node in pairNodeList:
		constructs = findNodesViaTag(node, "thing")
		note = findNodesViaTag(node, "note")
		relatedConstructsList[(constructs[0].text, constructs[1].text)] = note[0].text
	return relatedConstructsList

def getCategoryList(filename, tabname, relatedconstructs):
	tree = ET.parse(filename)
	root = tree.getroot()
	categoryNodelist = findNodesViaTag(root, "category")
	categoryList = []

	# add categories
	for node in categoryNodelist:
		description = findNodesViaTag(node, "description")
		newCat = data.Category(getAttribute(node, "name"), description[0].text)

		# add constructs to category
		constructs = findNodesViaTag(node, "construct")
		for constructNode in constructs:
			if type(constructNode) is not list:
				javaname = getAttribute(constructNode, "java")
				name = getAttribute(constructNode, "name")
				print name, "~~~~~", javaname
				construct = data.Construct(name, getDescription(constructNode))
				construct.javaname = javaname
				construct.methods += getMethods(constructNode)
				construct.usedwith += getUsedWith(constructNode)
				construct.javadocs += getLinks(constructNode)
				for key in relatedconstructs:
					if name in key[0] or (javaname != "" and javaname in key[0]):
						construct.related[key[1]] = relatedconstructs[key]
					elif name in key[1] or (javaname != "" and javaname in key[1]):
						construct.related[key[0]] = relatedconstructs[key]
				newCat.addConstruct(construct)
				if javaname != "":
					javaToConstruct[construct.javaname] = construct.name
				constructToCategory[construct.name] = newCat.name
		categoryToTab[newCat.name] = tabname
		categoryList.append(newCat)
	return data.Tab(tabname, [], categoryList, [])

def getMPI(filename):
	tree = ET.parse(filename)
	root = tree.getroot()

	description = findNodesViaTag(root, "description")[0].text
	newMPI = data.Construct(getAttribute(root, "name"), description)
	newMPI.javadocs += getLinks(root)
	newMPI.methods += getMethods(root)
	newMPI.MPIdatatypes += getList(root)[1]
	newMPI.MPIops += getOps(root)

	return data.Tab("MPI", [], [newMPI], [])

def testing(filename):
	tree = ET.parse(filename)
	root = tree.getroot()

	for e in root.iter():
		print e.text

def makeHTML():
	loader = TemplateLoader(
	    os.path.join(os.path.dirname(__file__), 'templates'),
	    auto_reload=True
	)
	relatedConstructsList = getRelatedConstructs()

	tabs = []
	tabs.append(getListGroup('content/OverviewTab.xml', "Overview"))
	tabs.append(getCategoryList('content/HjlibConstructsTab.xml', "HJLib", relatedConstructsList))
	tabs.append(getCategoryList('content/Java8ConstructsTab.xml', "Java8", relatedConstructsList))
	tabs.append(getMPI('content/MPITab.xml'))
	tabs.append(getInstructionList('content/InstallationTab.xml', "InstallationGuide"))
	tabs.append(data.Tab("EnvironmentConfiguration", [], [], []))
	tabs.append(data.Tab("CorrectnessPerformance", [], [], []))
	tabs.append(getInstructionList('content/JavaProfilingTab.xml', "JavaProfiling"))
	tabs.append(data.Tab("FAQs", [], [], []))

	tmpl = loader.load('hjdoc.html')
	testCat = tabs
	#testCat = data.getTestCategories()
	stream = tmpl.generate(tabs=testCat, constructToCategory=constructToCategory, javaToConstruct=javaToConstruct, categoryToTab=categoryToTab)
	f = open("test.html", "w")
	out = stream.render('html', doctype='html')
	f.write(out)

makeHTML()


