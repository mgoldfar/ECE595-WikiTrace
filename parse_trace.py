#! /usr/bin/env python2.6

import os, sys
import WikiTrace
		
import gzip
import StringIO
import sys

if len(sys.argv) != 4 and len(sys.argv) != 5 :
	sys.stderr.write("usage: parse_trace.py <trace id> <start> <end> [trace_archive_dir=traces]\n")
	sys.exit(1)

traceid_base = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
load_from_trace_dir = False
trace_archive_dir="traces"

if len(sys.argv) == 5:
	load_from_trace_dir = True
	trace_archive_dir = sys.argv[4]


if start < 0 or end < 0 or start > end:
	sys.stderr.write("error: start must be less than or equal to end!\n")
	sys.exit(1)


if not os.path.exists(trace_archive_dir):
	os.mkdir(trace_archive_dir)

traces = WikiTrace.TraceSet()

total_exec_time = 0.0
total_db_stats = WikiTrace.DBTraceStats()

loc_cache_time = 0.0
loc_cache_db_stats = WikiTrace.DBTraceStats()
loc_cache_cache_stats = WikiTrace.CacheTraceStats()

parser_time = 0.0
parser_db_stats = WikiTrace.DBTraceStats()
parser_cache_stats = WikiTrace.CacheTraceStats()

resldr_time = 0.0
resldr_db_stats = WikiTrace.DBTraceStats()
resldr_cache_stats = WikiTrace.CacheTraceStats()

rev_time = 0.0
rev_db_stats = WikiTrace.DBTraceStats()
rev_cache_stats = WikiTrace.CacheTraceStats()

linker_time = 0.0
linker_db_stats = WikiTrace.DBTraceStats()
linker_cache_stats = WikiTrace.CacheTraceStats()

for i in range(start, end+1):
	traceid = "%s-%d" % (sys.argv[1], i)
	trace = WikiTrace.Trace()
	
	if not load_from_trace_dir:
		trace.loadFromMemcache(traceid)
		trace.saveToFile(os.path.join(trace_archive_dir, traceid))
	else:
		trace.loadFromFile(os.path.join(trace_archive_dir, traceid))

	total_exec_time += trace.root.get_time()
	total_db_stats.add(trace.root.get_database_stats())

	loc_cache_time += trace.root.get_time(["LocalisationCache::"])
	loc_cache_db_stats.add(trace.root.get_database_stats(["LocalisationCache::"]))
	loc_cache_cache_stats.add(trace.root.get_cache_stats(["LocalisationCache::"]))
	
	parser_time += trace.root.get_time(["Parser::"])
	parser_db_stats.add(trace.root.get_database_stats(["Parser::", "ParserCache::"]))
	parser_cache_stats.add(trace.root.get_cache_stats(["ParserCache::get"]))
	
	resldr_time += trace.root.get_time(["ResourceLoader::"])
	resldr_db_stats.add(trace.root.get_database_stats(["ResourceLoader::"]))
	resldr_cache_stats.add(trace.root.get_cache_stats(["ResourceLoader::"]))
	
	rev_time += trace.root.get_time(["Revision::"])
	rev_db_stats.add(trace.root.get_database_stats(["Revision::"]))
	rev_cache_stats.add(trace.root.get_cache_stats(["Revision::"]))
	
	linker_time += trace.root.get_time(["Linker::", "LinkCache::"])
	linker_db_stats.add(trace.root.get_database_stats(["Linker::", "LinkCache::"]))
	linker_cache_stats.add(trace.root.get_cache_stats(["Linker::", "LinkCache::"]))
	
	print "Processed trace %d" % (i,)
	
	#traces.set(traceid, trace)
	#print trace.root.toString(2)
	
	
print "Total Execution Time = %f" % (total_exec_time,)
print

print "Database Stats:"
print total_db_stats
print

print "Localization Stats:"
print "Time = %f" % (loc_cache_time, )
print loc_cache_db_stats
print loc_cache_cache_stats
print 

print "Parser Stats:"
print "Time = %f" % (parser_time, )
print parser_db_stats
print parser_cache_stats
print

print "Resource Loader Stats:"
print "Time = %f" % (resldr_time, )
print resldr_db_stats
print resldr_cache_stats
print

print "Revision:"
print "Time = %f" % (rev_time,)
print rev_db_stats
print rev_cache_stats
print

print "Linker:"
print "Time = %f" % (linker_time, )
print linker_db_stats
print linker_cache_stats
print



#traces.save("trace_archive")

sys.exit(0)
