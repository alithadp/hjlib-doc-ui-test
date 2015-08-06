from genshi.template import TemplateLoader
import os
import dataclasses as data
import xml.etree.ElementTree as ET

"""
Returns: A version of the given text with all of the specified chars deleted.
"""
def stripChars(text):
    chars = [' ', '/', '(s)', '-', '(', ')', '<', '>', '.', '&', '?']
    for c in chars:
    	text = text.replace(c, '')
    return text.lower().strip().split('<',1)[0]

"""
Returns: A String containing the internal link/ID for the given name.
"""
def getInternalLink(name):
	link = ""
	if name in javaToConstruct:
		name = javaToConstruct[name]
	if name in toCategory:
		link = stripChars(toTab[toCategory[name]]) + "-" + stripChars(toCategory[name]) + "-" + stripChars(name)
	elif name in toTab:
		link = stripChars(toTab[name]) + "-" + stripChars(name)
	else:
		link = stripChars(name)
	return link

"""
Returns: List of all of the given root's elements that match the given tag.
"""
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

"""
Returns: The given attribute (key) of the node as a String.
"""
def getAttribute(node, key):
	if key in node.attrib:
		attrib = node.attrib[key]
	else:
		attrib = ""
	return str(attrib)

"""
Returns: Either an ExternalLink, InternalLink, or String, depending on the url attribute of node.
"""
def getLink(node):
	url = getAttribute(node, "url")
	if url == "":
		link = data.InternalLink(node.text)
	elif url == "none":
		link = node.text
	else:
		link = data.ExternalLink(node.text, url)
	return link

"""
Returns: An InlineList of ExternalLinks containing the given node's javadocs.
"""
def getJavadoc(node):
	linkNodes = findNodesViaTag(node, "javadoc")
	if linkNodes == []:
		return None
	links = data.InlineList("Javadoc Link(s)", [])
	for n in linkNodes:
		links.items.append(data.ExternalLink(getAttribute(n, "name"), n.text))
	return links

"""
Returns: An InlineList of InternalLinks containing the given node's used with constructs.
"""
def getUsedWith(node):
	usedWithNodes = findNodesViaTag(node, "usedwith")
	if usedWithNodes == []:
		return None
	usedwith = data.InlineList("Used With", [])
	for n in usedWithNodes:
		usedwith.items.append(data.InternalLink(n.text, getInternalLink(n.text)))
	return usedwith

"""
Returns: A Table that contains a Method column and a Description column.
"""
def getMethods(node):
	methodTable = data.Table(["Method", "Description"], [])
	methodNodes = findNodesViaTag(node, "method")
	if methodNodes == []:
		return None
	for mnode in methodNodes:
		methodTable.rows.append([getAttribute(mnode, "name"), mnode.text])
	return methodTable

"""
Returns: A Table that contains a Reduction Operation column and a Description column.
"""
def getOps(node):
	opsTable = data.Table(["Reduction Operation", "Description"], [])
	opNodes = findNodesViaTag(node, "op")
	for onode in opNodes:
		opsTable.rows.append([getAttribute(onode, "name"), onode.text])
	return opsTable

"""
"""
def getFlags(node):
	flagTable = data.Table(["Flag", "Default Value", "Description"], [])
	flagNodes = findNodesViaTag(node, "flag")
	for fnode in flagNodes:
		flagTable.rows.append([getAttribute(fnode, "name"), getAttribute(fnode, "default"), fnode.text])
	return flagTable

"""
Returns: A Description object containing information from the given node.
"""
def getDescription(node):
	description = data.Description(node.text, [])
	linkNodes = findNodesViaTag(node, "link")
	for link in linkNodes:
		description.links.append(data.ExternalLink(link.text, getAttribute(link, "url")))
	return description

"""
Returns: A String containing the description with links embedded using HTML markup.
"""
def descriptionToHTML(desc):
	text = desc.description
	for link in desc.links:
		text = text.replace(link.name, "<a href='" + link.link + "' target='_blank'>" + link.name + "</a>")
	return text

"""
Returns: A dictionary with key=(construct 1, construct 2) and value=note.
"""
def getRelatedConstructs():
	tree = ET.parse('content/RelatedConstructs.xml')
	root = tree.getroot()
	pairNodeList = findNodesViaTag(root, "pair")
	relatedConstructsList = {}
	for node in pairNodeList:
		constructsNode = findNodesViaTag(node, "thing")
		note = findNodesViaTag(node, "note")
		relatedConstructsList[(getLink(constructsNode[0]), getLink(constructsNode[1]))] = note[0].text
	return relatedConstructsList

"""
Returns: A (title, list) tuple.
"""
def getList(node):
	name = getAttribute(node, 'name')
	items = []
	itemNodes = findNodesViaTag(node, "item")
	for n in itemNodes:
		items.append(getLink(n))
	return (name, items)

"""
Returns: A ListGroup containing lists in the node.
"""
def getListGroup(node):
	listNodes = findNodesViaTag(node, "list")
	myLists = data.ListGroup(getAttribute(node, "name"), [])
	for node in listNodes:
		myLists.lists.append(getList(node))
	return myLists

"""
Returns: A list containing the text components (description, quote, code, or image) of the given node.
"""
def getTextComponents(node):
	if list(node) == []:
		return [('description', data.Description(node.text, []))]
	components = []
	for elem in list(node):
		if elem.tag =='description':
			components.append((elem.tag, getDescription(elem)))
		elif elem.tag == 'quote':
			components.append((elem.tag, getTextComponents(elem)))
		else:
			components.append((elem.tag, elem.text.strip()))

	return components

"""
Returns: An Instruction containing information from the given "instruction" node.
"""
def getInstruction(node):
	name = getAttribute(node, "name")
	description = ""
	stepList = []
	for n in list(node):
		if n.tag == "description":
			description = getDescription(n)
		elif n.tag == "step":
			stepList.append(getTextComponents(n))
	return data.Instruction(name, description, stepList)

"""
Returns: A Question object containing the question and corresponding answer contained in the give node.
"""
def getQuestion(node):
	q = node.text
	a = getTextComponents(findNodesViaTag(node, "answer")[0])
	return data.Question(q, a)

"""
Returns: A Construct containing information from the given "construct" node.
"""
def getConstruct(node):
	name = getAttribute(node, "name")
	javaname = getAttribute(node, "java")
	#print name, "~~~~~", javaname
	construct = data.Construct(name, javaname, getDescription(findNodesViaTag(node, "description")[0]))
	processedTags = ["description"]
	for elem in list(node):
		if elem.tag not in processedTags and elem.tag in tagToFunction:
			construct.components.append(tagToFunction[elem.tag](node))
			processedTags.append(elem.tag)
	related = {}
	for key in relatedConstructs:
		mykey = None
		if (isinstance(key[0], str) and (name in key[0] or (javaname != "" and javaname in key[0]))) or (isinstance(key[0], str) == False and (name in key[0].name or (javaname != "" and javaname in key[0].name))):
			if (isinstance(key[1], str) and name != key[1] and javaname != key[1]) or (isinstance(key[1], str) == False and name != key[1].name and javaname != key[1].name):
				mykey = key[1]
		if (isinstance(key[1], str) and (name in key[1] or (javaname != "" and javaname in key[1]))) or (isinstance(key[1], str) == False and (name in key[1].name or (javaname != "" and javaname in key[1].name))):
			if (isinstance(key[0], str) and name != key[0] and javaname != key[0]) or (isinstance(key[0], str) == False and name != key[0].name and javaname != key[0].name):
				mykey = key[0]
		if mykey is not None:
			related[mykey] = relatedConstructs[key]
	if related != {}:
		construct.components.append(related)
	return construct

"""
Returns: A Category containing information from the given "category" node.
"""
def getCategory(node):
	category = data.Category(getAttribute(node, "name"))
	for elem in list(node):
		if elem.tag == "description":
			category.description = getDescription(elem)
		elif elem.tag in tagToFunction:
			if elem.tag == "question":
				nodename = elem.text
			else:
				nodename = getAttribute(elem, "name")
			toCategory[nodename] = category.name
			if elem.tag == "construct":
				javaToConstruct[getAttribute(elem, "java")] = nodename
			category.components.append(tagToFunction[elem.tag](elem))
	return category

"""
Returns: A Tab object that is parsed from the given XML file.
"""
def readTab(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	newTab = data.Tab(getAttribute(root, "name"), int(getAttribute(root, "order")), getAttribute(root, "dropdown"), [])
	print "TAB: " + newTab.name
	for node in list(root):
		if node.tag == "question":
			toTab[node.text] = newTab.name
		else:
			toTab[getAttribute(node, "name")] = newTab.name
		newTab.components.append(tagToFunction[node.tag](node))
	return newTab

"""
Reads all Tab files in the 'content' directory and processes the information into an HTML file.
"""
def makeHTML():
	loader = TemplateLoader(
	    os.path.join(os.path.dirname(__file__), 'templates'),
	    auto_reload=True
	)

	"""
	IMPORTANT: XML files must be read in order of appearance in the navigation bar.
	"""
	tabs = []
	for f in os.listdir('content'):
		if "Tab.xml" in f:
			newTab = readTab('content/' + f)
			if newTab.dropdown != "":
				if len(tabs) > 0 and isinstance(tabs[-1], tuple) and tabs[-1][0] == newTab.dropdown:
					tabs[-1][1].append(newTab)
				else:
					tabs.append((newTab.dropdown, [newTab]))
			else:
				tabs.append(newTab)

	tmpl = loader.load('hjdoc.html')
	stream = tmpl.generate(tabs=tabs)
	f = open("test.html", "w")
	out = stream.render('html', doctype='html')
	f.write(out)

"""
Global variables
"""
javaToConstruct = {}
toCategory = {}
toTab = {}
tagToFunction = {"javadoc": getJavadoc, "usedwith": getUsedWith, "description": getDescription, "instruction": getInstruction, "list": getList,
"listgroup": getListGroup, "construct": getConstruct, "category": getCategory, "method": getMethods, "op": getOps, "flag": getFlags, 
"question": getQuestion}
relatedConstructs = getRelatedConstructs()

makeHTML()