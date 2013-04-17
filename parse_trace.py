#! /usr/bin/env python2.6

import os, sys
import WikiTrace
		
import gzip
import StringIO
import sys

if len(sys.argv) != 2:
	sys.stderr.write("usage: parse_trace.py <trace id>\n")
	sys.exit(1)

trace = WikiTrace.Trace()
trace.loadFromMemcache(sys.argv[1])

root = trace.root

total_time = root.get_time()

db_stats = root.get_database_stats()
load_bal_time = root.get_time(["LoadBalancer::"])
db_time = db_stats.get_total_time()
print "=== DATABASE (%2.3f %2.3f%%) ===" % (db_time + load_bal_time, 100 * (db_time + load_bal_time) / total_time)
print db_stats
print "Load Balancer Time = %2.3f (%2.3f%%)" % (load_bal_time, 100 * load_bal_time / (load_bal_time + db_time))
print "Query Time = %2.3f (%2.3f%%)" % (db_time, 100 * db_time / (load_bal_time + db_time))
print "Connections Opened = %d" % (len(root.get_nodes(["LoadBalancer::reallyOpenConnection"]),))
print

loc_cache_time = root.get_time(["LocalisationCache::"])
print "=== LOCALISATION (%2.3f %2.3f%%) ===" % (loc_cache_time, 100 * loc_cache_time / total_time)
print root.get_cache_stats(["LocalisationCache::getItem", "LocalisationCache::getSubitem"])
print root.get_database_stats(["LocalisationCache::"])
print 

res_loader_time = root.get_time(["ResourceLoader::"])
print "=== RESOURCE LOADER (%2.3f %2.3f%%) ===" % (res_loader_time, 100 * res_loader_time / total_time)
print root.get_cache_stats(["ResourceLoader::filter"])
print root.get_database_stats(["ResourceLoader::"])
print

parser_time = root.get_time(["Parser::"])
print "=== PARSER (%2.3f %2.3f%%) ===" % (parser_time, 100 * parser_time / total_time)
print root.get_cache_stats(["ParserCache::get"])
print root.get_database_stats(["Parser::"])
print

print "Total time = %f" % (total_time, ) 

# get toplevel nodes
#print root.getTraceString()
#for n in root.get_nodes(["Parser::"]):
#	print n.getTraceString()

sys.exit(0)