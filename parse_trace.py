#! /usr/bin/env python2.6

import os, sys, glob
import WikiTrace
		
import gzip
import StringIO
import progressbar

if len(sys.argv) <= 3:
	sys.stderr.write("usage: parse_trace.py <trace id> <start> <end> [--delete_only] [--trace_archive_dir=traces] [--trace_server=localhost] [--download_only] [--trace_id_is_glob]\n")
	sys.exit(1)

traceid_base = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])

print_summary = True
load_from_trace_dir = False
delete_traces = False
trace_id_is_glob = False
trace_archive_dir="traces"
trace_server = "localhost"

for arg in sys.argv[4:]:
	if arg.startswith("--trace_archive_dir="):
		load_from_trace_dir = True
		trace_archive_dir = arg.replace("--trace_archive_dir=", "", 1)
	
	if arg.startswith("--trace_server="):
		trace_server = arg.replace("--trace_server=", "", 1)
		
	if arg.startswith("--download_only"):
		print_summary = False
		
	if arg.startswith("--delete_only"):
		print_summary = False
		delete_traces = True
		
	if arg.startswith("--trace_id_is_glob"):
		trace_id_is_glob = True

if start < 0 or end < 0 or start > end:
	sys.stderr.write("error: start must be less than or equal to end!\n")
	sys.exit(1)

if not load_from_trace_dir and trace_id_is_glob:
	sys.stderr.write("error: memcached does not support globs!\n")
	sys.exit(1)


if delete_traces:
	answer = raw_input("Really delete traces? ").trim()
	if answer != "YES":
		print "Aborting..."
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


def process_trace(trace):
	global total_exec_time, total_db_stats, loc_cache_time, loc_cache_db_stats, loc_cache_cache_stats, parser_time, parser_db_stats, parser_cache_stats, resldr_time, resldr_db_stats, resldr_cache_sats, rev_time, rev_db_stats, rev_cache_stats, linker_time, linker_db_stats, linker_cache_stats
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
		
print "Processing traces..."
progbar = progressbar.ProgressBar(maxval=end-start+1, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

j=0
for i in range(start, end+1):
	traceid = "%s-%d" % (sys.argv[1], i)
	
	if trace_id_is_glob:
		# multiple trace files that match the globs...                                                                                                                                   
		for tracefile in glob.glob(os.path.join(trace_archive_dir, traceid)):
			trace = WikiTrace.Trace()
			trace.loadFromFile(tracefile)
			if print_summary:
				process_trace(trace)
				
	elif delete_traces:
		trace = WikiTrace.Trace()
		trace.deleteFromMemcache(traceid, trace_server)
		continue
	else:
		trace = WikiTrace.Trace()
		if not load_from_trace_dir:
			trace.loadFromMemcache(traceid, trace_server)
			trace.saveToFile(os.path.join(trace_archive_dir, traceid))
		else:
			trace.loadFromFile(os.path.join(trace_archive_dir, traceid))

		if print_summary:
			process_trace(trace)

	#print "Processed trace %d" % (i,)
	progbar.update(j)
	j+=1
	
progbar.finish()	

if print_summary:
	print
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

sys.exit(0)
