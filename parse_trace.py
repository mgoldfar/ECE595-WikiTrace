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

main_description = "MediaWiki::performRequest"

def generate_performance_summary(root, total_time):
	perf_action_time = root.get_time()
	perf_action_ch = root.get_nodes()
	print "=== %s (%2.3f %2.3f%%) ===" % (root.description, perf_action_time, 100 * perf_action_time / total_time)
	
	db_stats = root.get_database_stats()
	load_bal_time = root.get_time(["LoadBalancer::"])
	db_time = db_stats.get_total_time()
	print "  === DATABASE (%2.3f %2.3f%%) ===" % (db_time + load_bal_time, 100 * (db_time + load_bal_time) / total_time)
	print "  ", db_stats
	print "   Load Balancer Time = %2.3f (%2.3f%%)" % (load_bal_time, 100 * load_bal_time / (load_bal_time + db_time))
	print "   Query Time = %2.3f (%2.3f%%)" % (db_time, 100 * db_time / (load_bal_time + db_time))
	print "   Connections Opened = %d" % (len(root.get_nodes(["LoadBalancer::reallyOpenConnection"]),))
	print

	loc_cache_time = root.get_time(["LocalisationCache::"])
	print "  === LOCALISATION (%2.3f %2.3f%%) ===" % (loc_cache_time, 100 * loc_cache_time / total_time)
	print "  ", root.get_cache_stats(["LocalisationCache::getItem", "LocalisationCache::getSubitem"])
	print "  ", root.get_database_stats(["LocalisationCache::"])
	print 

	res_loader_time = root.get_time(["ResourceLoader::"])
	print "  === RESOURCE LOADER (%2.3f %2.3f%%) ===" % (res_loader_time, 100 * res_loader_time / total_time)
	print "  ", root.get_cache_stats(["ResourceLoader::filter"])
	print "  ", root.get_database_stats(["ResourceLoader::"])
	print

	parser_time = root.get_time(["Parser::"])
	print "  === PARSER (%2.3f %2.3f%%) ===" % (parser_time, 100 * parser_time / total_time)
	print "  ", root.get_cache_stats(["ParserCache::get"])
	print "  ", root.get_database_stats(["Parser::"])
	print
	
	linker_time = root.get_time(["Linker::"])
	print "  === LINKER (%2.3f %2.3f%%) ===" % (linker_time, 100 * linker_time / total_time)
	print "  ", root.get_database_stats(["Linker::"])
	print
	
	everything_else = root.remove_subtrees(root.get_nodes(["LoadBalancer::", "LocalisationCache::", "ResourceLoader::", "Parser", "Linker::", "query:"]))
	print "  === OTHER (%2.3f %2.3f%%) ===" % (everything_else.get_time(), 100 * everything_else.get_time() / total_time)
	#print everything_else.toString()

perf_request_node = root.get_nodes(["MediaWiki::performRequest"])
assert len(perf_request_node) == 1

total_time = root.get_time()
generate_performance_summary(perf_request_node[0], total_time)

print

root_with_out_perform_request = root.remove_subtrees(perf_request_node)
generate_performance_summary(root_with_out_perform_request, total_time)

print "Total time = %f" % (total_time, ) 


sys.exit(0)