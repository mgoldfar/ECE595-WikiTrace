#! /usr/bin/env python2.6

import os, sys
import WikiTrace
		
import gzip
import StringIO
import sys

if len(sys.argv) != 4:
	sys.stderr.write("usage: parse_trace.py <trace id> <start> <end>\n")
	sys.exit(1)

traceid_base = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])

if start < 0 or end < 0 or start > end:
	sys.stderr.write("error: start must be less than or equal to end!\n")
	sys.exit(1)

traces = WikiTrace.TraceSet()

for i in range(start, end+1):
	traceid = "%s-%d" % (sys.argv[1], i)
	trace = WikiTrace.Trace()
	trace.loadFromMemcache(traceid)
	traces.set(traceid, trace)
	print trace.root.toString(2)
	print "Loaded Trace %d" % (i,)
print "Total Execution Time = %f" % (traces.getAggergateTimeForNodes())
print

print "Database Stats:"
print traces.getAggergateDBStats() 
print

print "Localization Stats:"
print "Time = %f" % (traces.getAggergateTimeForNodes(["LocalisationCache::"]), )
print traces.getAggergateCacheStats(["LocalisationCache::"])
print traces.getAggergateDBStats(["LocalisationCache::"]) 
print 

print "Parser Stats:"
print "Time = %f" % (traces.getAggergateTimeForNodes(["Parser::", "ParserCache::"]), )
print traces.getAggergateCacheStats(["ParserCache::"])
print traces.getAggergateDBStats(["Parser::", "ParserCache::"]) 
print

print "Resource Loader Stats:"
print "Time = %f" % (traces.getAggergateTimeForNodes(["ResourceLoader::"]), )
print traces.getAggergateCacheStats(["ResourceLoader::filter"])
print traces.getAggergateDBStats(["ResourceLoader::"]) 
print

print "Revision:"
print "Time = %f" % (traces.getAggergateTimeForNodes(["Revision::"]), )
print traces.getAggergateCacheStats(["Revision::"])
print traces.getAggergateDBStats(["Revision::"]) 
print

print "Linker:"
print "Time = %f" % (traces.getAggergateTimeForNodes(["Linker::", "LinkCache::"]), )
print traces.getAggergateCacheStats(["Linker::", "LinkCache::"])
print traces.getAggergateDBStats(["Linker::", "LinkCache::"]) 
print



traces.save("trace_archive")

sys.exit(0)