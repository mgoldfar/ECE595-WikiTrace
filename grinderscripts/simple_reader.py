from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
from HTTPClient import NVPair
import Wikiparser
import re
import time
import random

testName = grinder.properties.getProperty("ece595.testname")
serverURL = grinder.properties.getProperty("ece595.url")
baseID = int(grinder.properties.getProperty("ece595.baseid"))
traceServer = grinder.properties.getProperty("ece595.traceserver")
cacheType = grinder.properties.getProperty("ece595.cachetype")
runs =  int(grinder.properties.getProperty("grinder.runs"))

test = Test(1, testName)
request = HTTPRequest()
test.record(request)

class TestRunner:
  def __call__(self):
	traceindex = baseID*runs + grinder.runNumber
	theurl = serverURL + "/index.php/Ethernet?RequestID=%s-%d&TraceServer=%s&CompressTrace=gzip&CacheType=%s" % (testName, traceindex, traceServer, cacheType)
	
	print "Making request to %s" % (theurl, )
	result = request.GET(theurl)
	print result
