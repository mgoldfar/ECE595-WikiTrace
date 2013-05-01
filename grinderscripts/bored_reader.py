# Simple HTTP example
#
# A simple example using the HTTP plugin that shows the retrieval of a
# single page via HTTP. The resulting page is written to a file.
#
# More complex HTTP scripts are best created with the TCPProxy.

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

DEPTH = 5
INITIAL_PAGE = "Ethernet"
READER_OPEN = 0.3
OPEN_AGAIN = 0.2

test = Test(1, testName)
request = HTTPRequest()
test.record(request)

theurl = serverURL + "/index.php/%s?RequestID=%s-%d-%d&TraceServer=%s&CompressTrace=gzip&CacheType=%s"
    
class TestRunner:
	def __call__(self):		
		traceIndex = baseID*runs + grinder.runNumber
		cur_link = INITIAL_PAGE 
		for i in range(DEPTH):
			actual_url = theurl % (cur_link, testName, i, traceIndex, traceServer, cacheType)
			print actual_url
			
			# the the lings from the page 
			result = request.GET(actual_url)
			links = Wikiparser.getlinks(result.getText().encode('utf-8'))
			#print links 
			
			# pick a random link:
			random.shuffle(links)
			cur_link = random.choice(links).replace("/index.php/", "")
			#print cur_link
