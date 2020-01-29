from itertools import chain, combinations

# A simple Tuple class -- with the only main functionality of retrieving and setting the 
# attribute value through a brute-force search
class RelationTuple: 
	def __init__(self, schema, t):
		self.t = t
		self.schema = schema
	def __str__(self):
		return str(self.t)
	def getAttribute(self, attribute):
		for i,attr in enumerate(self.schema):
			if attr == attribute:
				return self.t[i] 
		raise ValueError("Should not reach here")
	def __eq__(self, other):
		return self.schema == other.schema and self.t == other.t

# A relational contains a bunch of RelationTuples, as well as a "schema"
class Relation: 
	def __init__(self, name, schema):
		self.tuples = list()
		self.name = name
		self.schema = schema 
	def add(self, t):
		self.tuples.append(t)
	def rename(self, newname):
		self.name = newname
	def addIfNotDuplicate(self, t):
		if t not in self.tuples:
			self.tuples.append(t)
	def addTuples(self, list_of_tuples):
		for l in list_of_tuples:
			self.add(RelationTuple(self.schema, l))
		return self
	def printtuples(self):
		for t in self.tuples:
			print(t)
	def prettyprint(self):
		print("==========================")
		print( "	".join(str(x) for x in self.schema))
		for t in self.tuples:
			print("	".join(str(x) for x in t.t))

    	# Overridden dict class which takes a dict in the form {'a': 2, 'b': 3},
    	# and renders an HTML Table in IPython Notebook.
	def _repr_html_(self):
	    html = ["<table style=\"cellpadding:10px;width=30%;display:inline-block;margin-left: 40px\">"] 
	    html.append("<caption style=\"text-align:center\">{}</caption>".format(self.name))
	    html.append("<th style=\"padding:10px\"><b>")
	    html.append("</td><td style=\"padding:10px\"><b>".join(x for x in self.schema))
	    html.append("</td></th>")
	    for t in self.tuples:
		    html.append("<tr><td style=\"padding:10px\">")
		    html.append("</td><td style=\"padding:10px\">".join(str(x) for x in t.t))
		    html.append("</td></tr>")
	    html.append("</table>")
	    return ''.join(html)

class DisplayMultipleTables: 
	def __init__(self, relationList):
		self.relationList = relationList
	def _repr_html_(self):
		return ''.join([r._repr_html_() for r in self.relationList])


# Encodes a predicate to be evaluated against a single tuple
# We allow predicates of the form: attr OP constant, where OP can be ==, >=, <=, !=
class UnaryPredicate: 
	def __init__(self, attrname, op, const):
		self.op = op
		self.const = const
		self.attrname = attrname
	def evaluate(self, t):
		if self.op == '==':
			return t.getAttribute(self.attrname) == self.const
		if self.op == '>=':
			return t.getAttribute(self.attrname) >= self.const
		if self.op == '<=':
			return t.getAttribute(self.attrname) <= self.const
		if self.op == '!=':
			return t.getAttribute(self.attrname) != self.const
		raise ValueError("Unknown operator")

# Binary predicates are similar to above, but both their arguments are tuple attributes
# We allow predicates of the form: attr1 OP attr2, where OP can be ==, >=, <=, !=
# We allow the binary predicate to take two tuples as input or one tuple
class BinaryPredicate: 
	def __init__(self, attrname1, op, attrname2):
		self.op = op
		self.attrname1 = attrname1
		self.attrname2 = attrname2
	def evaluateUnary(self, t):
		if self.op == '==':
			return t.getAttribute(self.attrname1) == t.getAttribute(self.attrname2)
		if self.op == '>=':
			return t.getAttribute(self.attrname1) >= t.getAttribute(self.attrname2)
		if self.op == '<=':
			return t.getAttribute(self.attrname1) <= t.getAttribute(self.attrname2)
		if self.op == '!=':
			return t.getAttribute(self.attrname1) != t.getAttribute(self.attrname2)
		raise ValueError("Unknown operator")
	def evaluateBinary(self, t1, t2):
		if self.op == '==':
			return t1.getAttribute(self.attrname1) == t2.getAttribute(self.attrname2)
		if self.op == '>=':
			return t1.getAttribute(self.attrname1) >= t2.getAttribute(self.attrname2)
		if self.op == '<=':
			return t1.getAttribute(self.attrname1) <= t2.getAttribute(self.attrname2)
		if self.op == '!=':
			return t1.getAttribute(self.attrname1) != t2.getAttribute(self.attrname2)
		raise ValueError("Unknown operator")

# A select (sigma) operation creates a new relation with only those tuples that satisfy the condition
def sigma(r, attrname, op, const):
	# Result relation will have the same schema
	predicate = UnaryPredicate(attrname, op, const)
	result = Relation("sigma_{{{} {} {}}} ({})".format(attrname, op, const, r.name), r.schema)
	for t in r.tuples:
		if predicate.evaluate(t):
			result.add(t) # We assume tuples are immutable here, otherwise a copy is warranted
	return result

# A project (pi) operation creates a new relation with only those tuples that satisfy the condition
def pi(r, attrlist):
	# Result relation will have the schema attrlist
	result = Relation("pi_{{{}}} ({})".format(",".join(attrlist), r.name), attrlist)
	for t in r.tuples:
		newt = RelationTuple(result.schema, [t.getAttribute(attr) for attr in attrlist])
		result.addIfNotDuplicate(newt) 
	return result

# A cartesian (cross) product operation creates a new relation by pairing up every tuple in one relation with every tuple in another relation
def cartesian(r1, r2):
	# Result relation will have attributes from both the relations
	# To disambiguate, we will append the relation name to the attributes
	result = Relation("{} cross product {}".format(r1.name, r2.name), [r1.name + "." + x for x in r1.schema] + [r2.name + "." + x for x in r2.schema])
	for t1 in r1.tuples:
		for t2 in r2.tuples:
			newt = RelationTuple(result.schema, t1.t + t2.t)
			result.add(newt) 
	return result

# A Union is a binary operator -- both the input relations are required to have the same schema
def union(r1, r2):
	result = Relation("{} union {}".format(r1.name, r2.name), r1.schema)
	for t1 in r1.tuples:
		newt = RelationTuple(result.schema, t1.t)
		result.add(newt) 
	for t2 in r2.tuples:
		newt = RelationTuple(result.schema, t2.t)
		result.addIfNotDuplicate(newt) 
	return result

# A Set Difference is a binary operator -- both the input relations are required to have the same schema
def minus(r1, r2):
	result = Relation("{} - {}".format(r1.name, r2.name), r1.schema)
	for t1 in r1.tuples:
		if t1 not in r2.tuples:
			newt = RelationTuple(result.schema, t1.t)
			result.add(newt) 
	return result

# A join is a cartesian product followed by a predicate
def join(r1, r2, attrname1, op, attrname2):
	# Result relation will have attributes from both the relations
	# To disambiguate, we will append the relation name to the attributes
	predicate = BinaryPredicate(attrname1, op, attrname2)
	result = Relation("{} join_{{{} {} {}}} {}".format(r1.name, attrname1, op, attrname2, r2.name), [r1.name + "." + x for x in r1.schema] + [r2.name + "." + x for x in r2.schema])
	for t1 in r1.tuples:
		for t2 in r2.tuples:
			newt = RelationTuple(result.schema, t1.t + t2.t)
			if predicate.evaluateUnary(newt):
				result.add(newt) 
	return result



##### NOT Working properly below


# A full outer-join requires finding the tuples in both relations that don't have matches
# The below is the naive and highly inefficient implementation
# We will see better implementations when we discuss "query processing"
FULLOUTERJOIN = 1
LEFTOUTERJOIN = 2
RIGHTOUTERJOIN = 3
def fullouterjoin(r1, r2, predicate, outerjointype):
	# Result relation will have attributes from both the relations
	# To disambiguate, we will append the relation name to the attributes
	result = Relation("", [r1.name + "." + x for x in r1.schema] + [r2.name + "." + x for x in r2.schema])

	# First add the join results as above
	for t1 in r1.tuples:
		for t2 in r2.tuples:
			newt = RelationTuple(result.schema, t1.t + t2.t)
			if predicate.evaluateUnary(newt):
				result.add(newt) 

	# Now go over one relation and identify tuples that don't have a match
	for t1 in r1.tuples:
		match = False
		for t2 in r2.tuples:
			newt = RelationTuple(result.schema, t1.t + t2.t)
			if predicate.evaluateUnary(newt):
				match = True
				break
		if not match: 
			newt = RelationTuple(result.schema, t1.t + ["null" for x in r2.schema])
			result.add(newt)

	# Do the same for the other relation
	for t2 in r2.tuples:
		match = False
		for t1 in r1.tuples:
			newt = RelationTuple(result.schema, t1.t + t2.t)
			if predicate.evaluateUnary(newt):
				match = True
				break
		if not match: 
			newt = RelationTuple(result.schema, ["null" for x in r1.schema] + t2.t)
			result.add(newt)
	return result

#r4 = fullouterjoin(r, s, BinaryPredicate("r.C", "==", "s.C"))
#r4.prettyprint()
