import os, sys
import memcache
import zlib 

class Trace:
	
	def __init__(self):
		self.memcache_server = None
		self.memcache_key = None
		self.filename = None
		self.root = None # root node of the trace tree
		self.info = {} # dictionary of key=value pairs from trace
		
	def loadFromFile(self, filename):
		self.filename = filename
		with open(filename, "r") as f:
			tracestr = f.read()
		
		self.loadFromString(tracestr)
	
	def saveToFile(self, filename):
		with open(filename, "w") as f:
			tracestr = self.root.toString()
			f.write(tracestr)
		
	def loadFromMemcache(self, memcache_key, memcache_server=None):
		if not memcache_server:
			self.memcache_server = "localhost:11211"
		else:
			# use default port if non given	
			server_and_port = memcache_server.split(":", 1)
			if len(srver_and_port) == 1:
				port = 11211
			else:
				port = int(server_and_port[1])
			
			self.memcache_server = "%s:%d" % (server_and_port[0], port)
			
		self.memcache_key = memcache_key
		
		mc = memcache.Client([self.memcache_server])
		tracestr = mc.get(memcache_key)
		if not tracestr:
			raise KeyError(memcache_key)
		
		self.loadFromString(tracestr)
	
	def _is_zlib_compressed(self, s):
		if len(s) < 2:
			return False
			
		cmf = ord(s[0])
		if cmf & 0x0f != 0x08 and cmf & 0xf0 != 0x70:
			return False
		
		flg = ord(s[1])
		
		if (cmf*256 + flg) % 31 != 0:
			return False
	
		return True
		
			
	def loadFromString(self, tracestr):
		
		# Check if the string is zlib compressed
		if self._is_zlib_compressed(tracestr):
			tracestr = zlib.decompress(tracestr)
			
		cur_level = 0
		self.root = TraceItem("trace", None)
		item_stack = [self.root]

		linen = 0
		found_start = False
		for line in tracestr.split('\n'):
			origline = line
			line = line.strip().split()
			linen += 1

			if not line:
				continue

			if not found_start:
				# special -setup line in the trace	
				if len(line) >= 4 and line[2] == "<":
					self.root.time = float(line[0])
					found_start = True
				else:
					# Try to extract a key=value pair:
					kv = origline.split("=", 1)
					if len(kv) == 2:
						self.info[kv[0]] = kv[1]
						
				continue


			if line[2] == ">": # entering function
				parent = item_stack[-1]
				item = TraceItem(" ".join(line[3:]), parent)
				item.memchange_in = float(line[1])
				item_stack.append(item)
				parent.add_item(item)

			elif line[2] == "<": # exiting a trace
				item = item_stack.pop()
				if item == self.root:
					raise ValueError("Trace is not properly balanced!")

				# for nodes with children the time represents the total time spend for the
				# statements in that call, total time is computed by aggergating the children
				item.time = float(line[0])
				item.memchange_out = float(line[1])

			elif line[2] == "+":
				parent = item_stack[-1]
				item = TraceItem(" ".join(line[3:]), parent)
				item.time = float(line[0])
				item.memchange_in = float(line[1])
				parent.add_item(item)

		if not found_start:
			raise ValueError("Invalid trace string format!")

		# update the root time to reflect its children, the raw trace excludes this time
		for ch in self.root.items:
			self.root.time += ch.time
	
	def toString(self):
		s = ""
		for k, v in self.info:
			s += "%s=%s\n" % (k, v)
		s += self.root.toString()
		return s
		
class TraceItem:
	__LastID = 0
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
		
		# Unique ID for items
		TraceItem.__LastID += 1
		self.id = TraceItem.__LastID

	def clone(self, shallow=False):
		"""Creates a duplicate of this node an all children."""
		new_item = TraceItem(self.description, None)
		new_item.time = self.time
		new_item.memchange_in = self.memchange_in
		new_item.memchange_out = self.memchange_out
		new_item.level = self.level
		new_item.id = self.id
		new_item.parent = self.parent
		
		if not shallow:
			for ch in self.items:
				new_ch = ch.clone(shallow)
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
			qnodes = n.get_nodes(["DatabaseBase::query"])
			lbnodes = n.get_nodes(["LoadBalancer::"])
			nodes_r = []
			nodes_w = []
			nodes_o = []
			for k in range(len(qnodes)):
				qn = qnodes[0]
				ch = qn.items[0]
				if ch.description.startswith("DatabaseMysql::doQuery SELECT"):
					nodes_r.append(qnodes.pop(0))
				elif any([ch.description.startswith(x) for x in ["DatabaseMysql::doQuery UPDATE", "DatabaseMysql::doQuery INSERT", "DatabaseMysql::doQuery DELETE"]]):
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
			for m in lbnodes:
				stats.load_balancer_calls += 1
				stats.load_balancer_time += m.get_time()
			stats.connections_opened = len(n.get_nodes(["LoadBalancer::reallyOpenConnection"]))
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
	
	def _get_node_by_id(self, i):
		"""Internal. Gets a the node that matches the specified ID."""
		if self.id == i:
			return self
		
		for ch in self.items:
			foundch = ch._get_node_by_id(i)
			if foundch != None:
				return foundch
		
		return None
		
	def remove_subtrees(self, nodes):
		"""Removes the subtrees rooted by the elements of nodes. This creates a duplicate trace item."""
		worklist = list(nodes)
		new_root = self.clone()

		for n in nodes:
			m = new_root._get_node_by_id(n.id)
			if m == None:
				continue # subtree was already removed because a parent subtree was removed
				
			if m.parent == None:
				raise Exception("Can not remove subtree because node is not a child!")
			
			m.parent.items.remove(m) # remove the item
			
			# propagate the removed time upwards to all parent nodes
			p = m.parent
			while p != None:
				p.time -= m.time
				p = p.parent

		return new_root
		
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
	
		
class TraceSet:
	def __init__(self):
		self.items = {}
	
	def set(self, key, item):
		self.items[key] = item
	
	def get(self, key):
		return self.items[key]
	
	def save(self, directory_name):
		if not os.path.exists(directory_name) and not os.path.isdir(directory_name):
			os.mkdir(directory_name)
			
		for k, v in self.items.iteritems():
			filepath = os.path.join(directory_name, k)
			v.saveToFile(filepath)
	
	def getAggergateTimeForNodes(self, prefixes=None):
		t = 0.0
		for k, v in self.items.iteritems():
			t += v.root.get_time(prefixes)
		return t
			
	def getAggergateDBStats(self, prefixes=None):
		s = DBTraceStats()
		for k, v in self.items.iteritems():
			s = s.add(v.root.get_database_stats(prefixes))
		return s
		
	def getAggergateCacheStats(self, prefixes=None):
		s = CacheTraceStats()
		for k, v in self.items.iteritems():
			s = s.add(v.root.get_cache_stats(prefixes))
		return s

class DBTraceStats:
	def __init__(self):
		self.reads = 0
		self.writes = 0
		self.other = 0
		self.read_t = 0.0
		self.write_t = 0.0
		self.other_t = 0.0
		self.load_balancer_calls = 0
		self.load_balancer_time = 0.0
		self.connections_opened = 0

	def add(self, other):
		#r = DBTraceStats()
		self.reads = self.reads + other.reads
		self.writes = self.writes + other.writes
		self.other = self.other + other.other
		self.read_t = self.read_t + other.read_t
		self.write_t = self.write_t + other.write_t
		self.other_t = self.other_t + other.other_t
		self.load_balancer_calls = self.load_balancer_calls + other.load_balancer_calls
		self.load_balancer_time = self.load_balancer_time + other.load_balancer_time
		self.connections_opened = self.connections_opened + other.connections_opened
		return self

	def get_total_time(self):
		return self.read_t + self.write_t + self.other_t + r.load_balancer_time

	def __str__(self):
		return "DB: Rd %d %f, Wr %d %f, Ot %d %f, LB %d %f, Conns %d" % (self.reads, self.read_t, self.writes, self.write_t, self.other, self.other_t, self.load_balancer_calls, self.load_balancer_time, self.connections_opened)

class CacheTraceStats:
	def __init__(self):
		self.access = 0
		self.hits = 0
		self.misses = 0

	def add(self, other):
		#s = CacheTraceStats()
		self.access = self.access + other.access
		self.hits = self.hits + other.hits
		self.misses = self.misses + other.misses
		return self

	def __str__(self):
		if self.access > 0:
			hitp = 100*float(self.hits)/self.access
			missp = 100*float(self.misses)/self.access
		else:
			hitp = 0
			missp = 0

		return "CACHE: Access %d, Hit %d %f%%, Miss %d %f%%" % (self.access, self.hits, hitp, self.misses, missp)
	