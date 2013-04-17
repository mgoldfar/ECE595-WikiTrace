import os, sys
import memcache

class DBTraceStats:
	def __init__(self):
		self.reads = 0
		self.writes = 0
		self.other = 0
		self.read_t = 0.0
		self.write_t = 0.0
		self.other_t = 0.0
	
	def add(self, other):
		r = DBTraceStats()
		r.reads = self.reads + other.reads
		r.writes = self.writes + other.writes
		r.other = self.other + other.other
		r.read_t = self.read_t + other.read_t
		r.write_t = self.write_t + other.write_t
		r.other_t = self.other_t + other.other_t
		return r
	
	def get_total_time(self):
		return self.read_t + self.write_t + self.other_t
	
	def __str__(self):
		return "DB: R %d %2.3f, W %d %2.3f, O %d %2.3f" % (self.reads, self.read_t, self.writes, self.write_t, self.other, self.other_t)
		
class CacheTraceStats:
	def __init__(self):
		self.access = 0
		self.hits = 0
		self.misses = 0
	
	def add(self, other):
		s = CacheTraceStats()
		s.access = self.access + other.access
		s.hits = self.hits + other.hits
		s.misses = self.misses + other.misses
		return s
	
	def __str__(self):
		if self.access > 0:
			hitp = 100*float(self.hits)/self.access
			missp = 100*float(self.misses)/self.access
		else:
			hitp = 0
			missp = 0
	
		return "CACHE: Access %d, Hit %d %2.3f%%, Miss %d %2.3f%%" % (self.access, self.hits, hitp, self.misses, missp)

class Trace:
	
	def __init__(self):
		self.memcache_server = None
		self.memcache_key = None
		self.filename = None
		self.root = None
		
	def loadFromFile(self, filename):
		self.filename = filename
		with open(filename, "r") as f:
			tracestr = f.read()
		
		self.root = fromString(tracestr)
			
	def saveToFile(self, filename):
		with open(filename, "w") as f:
			tracestr = self.root.toString()
			f.write(tracestr)
		
	def loadFromMemcache(self, memcache_key, memcache_server=None):
		if not memcache_server:
			self.memcache_server = "localhost:11211"
		else:	
			self.memcache_server = memcache_server
			
		self.memcache_key = memcache_key
		
		mc = memcache.Client([self.memcache_server])
		tracestr = mc.get(memcache_key)
		if not tracestr:
			raise KeyError(memcache_key)
			
		self.root = fromString(tracestr)
		
class TraceItem:
	def __init__(self, description, parent):
		self.description = description
		self.time = 0.0
		self.memchange_in = 0.0
		self.memchange_out = 0.0
		self.level = 0

		if parent != None:
			self.level = parent.level + 1

		self.items = []
		self.parent = parent

	def clone(self, shallow=False):
		"""Creates a duplicate of this node an all children."""
		new_item = TraceItem(self.description, None)
		new_item.time = self.time
		new_item.memchange_in = self.memchange_in
		new_item.memchange_out = self.memchange_out
		new_item.level = self.level
		
		if not shallow:
			for ch in self.items:
				new_ch = ch.clone()
				new_item.add_item(new_ch)
				new_ch.parent = new_item
		else:
			new_item.items.extend(self.items)
		return new_item
			
	def add_item(self, item):
		item.level = self.level + 1
		self.items.append(item)
	
	def get_time(self, prefixes=None):
		t = 0.0
		nodes = self.get_nodes(prefixes)
		for n in nodes:
			t += n.time				
		return t
			
	def get_cache_stats(self, prefixes=None):
		"""Gets the DB access stats for the nodes contained in the specified prefixes."""
		nodes = self.get_nodes(prefixes)
		stats = CacheTraceStats()
		for n in nodes:
			subnodes_hit = n.get_nodes_containing(["CACHE HIT"])
			subnodes_miss = n.get_nodes_containing(["CACHE MISS"])
			stats.access += len(subnodes_hit) + len(subnodes_miss)
			stats.hits += len(subnodes_hit)
			stats.misses += len(subnodes_miss)
		return stats
		
	def get_database_stats(self, prefixes=None):
		"""Gets the DB access stats for the nodes contained in the specified prefixes."""
		nodes = self.get_nodes(prefixes)
		stats = DBTraceStats()
		for n in nodes: 
			qnodes = n.get_nodes(["query:"])
			nodes_r = []
			nodes_w = []
			nodes_o = []
			for k in range(len(qnodes)):
				qn = qnodes[0]
				if qn.description.startswith("query: SELECT"):
					nodes_r.append(qnodes.pop(0))
				elif qn.description.startswith("query: UPDATE") or qn.description.startswith("query: INSERT") or qn.description.startswith("query: DELETE"):
					nodes_w.append(qnodes.pop(0))
				else:
					nodes_o.append(qnodes.pop(0))
			for m in nodes_r:
				stats.reads += 1
				stats.read_t += m.time
			for m in nodes_w:
				stats.writes += 1
				stats.write_t += m.time
			for m in nodes_o:
				stats.other += 1
				stats.other_t += m.time

		return stats
			
	def get_nodes(self, prefixes=None):
		"""Gets the nodes that contain the specified prefixes"""
	
		if not prefixes:
			return self.items
		
		nodes = []
		
		if any(( self.description.startswith(p) for p in prefixes )):
			return [self]
		else:
			nodes = []
			for ch in self.items:
				nodes.extend(ch.get_nodes(prefixes))
			return nodes
			
	def remove_subtrees(self, nodes):
		"""Removes the subtrees rooted by the elements of nodes. This creates a duplicate trace item."""
				
		# leaf node
		if len(self.items) == 0:
			if self not in nodes:
				return self.clone()
			else:
				return None
		
		new_children = []
		subtracted_time = 0.0
		for ch in self.items:
			if ch not in nodes:
				new_subtree = ch.remove_subtrees(nodes)
				if new_subtree:
					new_children.append(new_subtree)
			else:
				subtracted_time += ch.time
		
		new_root = self.clone(True) # shallow copy
		new_root.items = new_children # repace children
		new_root.time = 0.0 
		for ch in new_root.items: 
			new_root.time += ch.time # reompute node time
			ch.parent = new_root # update parent node
			
		return new_root
		
	def get_nodes_containing(self, substrs=None):
		"""Gets a list of any nodes that contain a substrings"""
		
		if not substrs:
			return self.items
		
		if  any(( self.description.find(p) >= 0 for p in substrs )):
			return [self]
		else:
			nodes = []
			for ch in self.items:
				nodes.extend(ch.get_nodes_containing(substrs))
			return nodes
				
	def __str__(self):
		return "%f %s\n" % (self.time, self.description)
	
	def toString(self, maxdepth=0, depth=0):
		"""Reproduces the oroginal trace string."""
		pad = ""
		for i in range(depth):
			pad += " "
		if len(self.items) > 0:
			
			# special parent object:
			if self.parent == None:
				s = "%-20s %s< %s\n" % ("%f %f" % (self.time, self.memchange_in), pad, self.description)
				if maxdepth > 0 and depth < maxdepth or maxdepth == 0:		
					for ch in self.items:
						s += ch.toString(maxdepth, depth + 1)
				return s
			else:
				s = "%-20s %s> %s\n" % ("- %f" % (self.memchange_in,), pad, self.description)
				if maxdepth > 0 and depth < maxdepth or maxdepth == 0:		
					for ch in self.items:
						s += ch.toString(maxdepth, depth + 1)
				s += "%-20s %s< %s\n" % ("%f %f" % (self.time, self.memchange_out), pad, self.description)
				return s
		else:
			return "%-20s %s+ %s\n" % ("%f %f" % (self.time, self.memchange_in), pad, self.description)
		
	
def fromString(tracestr):
	cur_level = 0
	root = TraceItem("trace", None)
	item_stack = [root]

	linen = 0
	found_start = False
	for line in tracestr.split('\n'):
		line = line.strip().split()
		linen += 1
		
		if not line:
			continue
		
		if not found_start:
			# special -setup line in the trace	
			if len(line) >= 4 and line[2] == "<":
				root.time = float(line[0])
				found_start = True
			continue
			

		if line[2] == ">": # entering function
			parent = item_stack[len(item_stack) - 1]
			item = TraceItem(" ".join(line[3:]), parent)
			item.memchange_in = float(line[1])
			item_stack.append(item)
			parent.add_item(item)

		elif line[2] == "<" and line[3] != "-setup": # exiting a trace
			item = item_stack.pop()
			if item == root:
				raise ValueError("Trace is not properly balanced!")
				
			item.time = float(line[0])
			item.memchange_out = float(line[1])

		elif line[2] == "+" and line[3] != "-setup":
			parent = item_stack[len(item_stack) - 1]
			item = TraceItem(" ".join(line[3:]), parent)
			item.time = float(line[0])
			item.memchange_in = float(line[1])
			parent.add_item(item)
	
	if not found_start:
		raise ValueError("Invalid trace string format!")
	
	# update the root time to reflect its children, the raw trace excludes this time
	for ch in root.items:
		root.time += ch.time
		
	return root
	
