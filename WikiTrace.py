import os, sys

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
		
class TraceItem:
	def __init__(self, description, parent):
		self.description = description
		self.time = 0.0
		self.level = 0
		if parent != None:
			self.level = parent.level + 1
		self.items = []
		self.parent = parent
		
	def add_item(self, item):
		item.level = self.level + 1
		self.items.append(item)
	
	def get_time(self, prefixes=None):
		t = 0.0
		if not prefixes:
			t = self.time	
			for n in self.items:
				t += n.get_time(prefixes)
		else:
			nodes = self.get_nodes(prefixes)
			for n in nodes:
				if n != self:
					t += n.get_time()
				else:
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
			return [self]
		
		nodes = []
		if any(( self.description.startswith(p) for p in prefixes )):
			return [self]
		else:
			nodes = []
			for ch in self.items:
				nodes.extend(ch.get_nodes(prefixes))
			return nodes
			
	def get_nodes_containing(self, substrs=None):
		"""Gets a list of any nodes that contain a substrings"""
		
		if not substrs:
			return [self]
		
		if  any(( self.description.find(p) >= 0 for p in substrs )):
			return [self]
		else:
			nodes = []
			for ch in self.items:
				nodes.extend(ch.get_nodes_containing(substrs))
			return nodes
				
	def __str__(self):
		return "%f %s\n" % (self.time, self.description)
	
	def getTraceString(self, maxdepth=0, depth=0):
		pad = ""
		for i in range(self.level):
			pad += " "
				
		s = "%s%s" % (pad, str(self))
		
		if maxdepth > 0 and depth < maxdepth or maxdepth == 0:		
			for ch in self.items:
				s += ch.getTraceString(maxdepth, depth + 1)
			
		return s
		
	
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
			if len(line) >= 4 and line[2] == "<" and line[3] == "-setup":
				root.time = float(line[0])
				found_start = True
			continue
			

		if line[2] == ">": # entering function
			parent = item_stack[len(item_stack) - 1]
			item = TraceItem(" ".join(line[3:]), parent)
			item_stack.append(item)
			parent.add_item(item)

		elif line[2] == "<" and line[3] != "-setup": # exiting a trace
			item = item_stack.pop()
			if item == root:
				raise Exception("Trace is not properly formed!")
				
			item.time = float(line[0])

		elif line[2] == "+" and line[3] != "-setup":
			parent = item_stack[len(item_stack) - 1]
			item = TraceItem(" ".join(line[3:]), parent)
			item.time = float(line[0])
			parent.add_item(item)
			
	return root
	
