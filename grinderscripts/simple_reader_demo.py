from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
from HTTPClient import NVPair
import Wikiparser
import re
import time
import random

# average page len = 726689
# 

# small, avg, large
page_description = ["small"]
pages = ["1829_in_sports"]
requests = []

testName = grinder.properties.getProperty("ece595.testname")
serverURL = grinder.properties.getProperty("ece595.url")
baseID = int(grinder.properties.getProperty("ece595.baseid"))
traceServer = grinder.properties.getProperty("ece595.traceserver")
cacheType = grinder.properties.getProperty("ece595.cachetype")
runs =  int(grinder.properties.getProperty("grinder.runs"))

for i in range(len(pages)):
	test = Test(i+1, "%s-%s" % (page_description[i], testName))
	request = HTTPRequest()
	requests.append(request)
	test.record(request)

class TestRunner:
  def __call__(self):
	for i in range(len(pages)):	
		traceindex = baseID*runs + grinder.runNumber
		theurl = serverURL + "/index.php/%s?RequestID=%s-%s-%d&TraceServer=%s&CompressTrace=gzip&CacheType=%s" % (pages[i], testName, page_description[i], traceindex, traceServer, cacheType)
		print "%s" % (theurl, )
		result = requests[i].GET(theurl)

