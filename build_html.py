from genshi.template import TemplateLoader
import os
import dataclasses as data
import xml.etree.ElementTree as ET

constructToCategory = {}
javaToConstruct = {}

def findNodesViaTag(root, tag):
	if tag == "javaname":
		print "-",root.tag
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
	print items
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

def getCategoryList(filename, tabname, hjlib):
	tree = ET.parse(filename)
	root = tree.getroot()
	categoryNodelist = findNodesViaTag(root, "category")
	categoryList = []

	# add categories
	for node in categoryNodelist:
		description = findNodesViaTag(node, "description")
		newCat = data.Category(getAttribute(node, "name"), description[0].text)
		print newCat.name, newCat.description

		# add constructs to category
		constructs = findNodesViaTag(node, "construct")
		for constructNode in constructs:
			if type(constructNode) is not list:
				javaname = getAttribute(constructNode, "java")
				"""
				if hjlib:
					name = getAttribute(constructNode, 1)
					print name, "~~~~~", javaname
					construct = data.Construct(name, getDescription(constructNode))
					construct.javaname = javaname
				else: 
					construct = data.Construct(javaname, getDescription(constructNode))
				"""
				name = getAttribute(constructNode, "name")
				print name, "~~~~~", javaname
				construct = data.Construct(name, getDescription(constructNode))
				construct.javaname = javaname
				construct.methods += getMethods(constructNode)
				construct.usedwith += getUsedWith(constructNode)
				construct.javadocs += getLinks(constructNode)
				print construct.name, construct.description
				print construct.usedwith
				print "=="
				newCat.addConstruct(construct)
				javaToConstruct[construct.javaname] = construct.name
				constructToCategory[construct.name] = newCat.name
		categoryList.append(newCat)
	return data.Tab(tabname, categoryList)

def makeHTML():
	loader = TemplateLoader(
	    os.path.join(os.path.dirname(__file__), 'templates'),
	    auto_reload=True
	)
	tabs = []
	tabs.append(getCategoryList('content/HjlibConstructsTab.xml', "HJLib", True))
	tabs.append(getCategoryList('content/Java8ConstructsTab.xml', "Java8", False))
	print tabs

	tmpl = loader.load('hjdoc.html')
	testCat = tabs
	#testCat = data.getTestCategories()
	stream = tmpl.generate(tabs=testCat, constructToCategory=constructToCategory, javaToConstruct=javaToConstruct)
	f = open("test.html", "w")
	out = stream.render('html', doctype='html')
	f.write(out)

makeHTML()


