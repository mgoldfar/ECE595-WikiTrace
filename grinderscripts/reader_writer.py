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

# small, avg, large
page_description = ["small", "average", "large"]
pages = ["1829_in_sports", "Computer_accessibility", "Ethernet"]
wiki_text = []
requests = []

testName = grinder.properties.getProperty("ece595.testname")
serverURL = grinder.properties.getProperty("ece595.url")
baseID = int(grinder.properties.getProperty("ece595.baseid"))
traceServer = grinder.properties.getProperty("ece595.traceserver")
cacheType = grinder.properties.getProperty("ece595.cachetype")
runs =  int(grinder.properties.getProperty("grinder.runs"))

WRITEPCTS = [10, 25]

# get the raw wiki text (avoid having to parse html output during the test)
for i in range(len(pages)):
	s = Wikiparser.get_page(pages[i], serverURL.replace("http://", "", 1))
	wiki_text.append(s.encode('utf-8'))
	print "Page %d size is %d" % (i, len(s))
	#print s

for i in range(len(pages)):
	test = Test(i+1, "%s-%s" % (page_description[i], testName))
	request = HTTPRequest()
	requests.append(request)
	test.record(request)

class TestRunner:
	def __call__(self):
		for i in range(len(pages)):	
			for j in range(len(WRITEPCTS)):
				writep = float(WRITEPCTS[j])/100

				traceindex = baseID*runs + grinder.runNumber
		
				urlParams = "TraceServer=%s&CompressTrace=gzip&CacheType=%s"% (traceServer, cacheType)
				
				readUrl = serverURL + "/index.php/%s?%s" % (pages[i], urlParams)
				writeEditUrl = serverURL + "/index.php?action=edit&title=%s&%s" % (pages[i], urlParams)
				writeSubmitUrl = serverURL + "/index.php?action=submit&title=%s&%s" % (pages[i], urlParams)
		
				if random.random() < writep:
					print "WRITE"
					print writeEditUrl
					print writeSubmitUrl
					
					# This is for getting the edit form
					requestID = "&RequestID=%s-%s-%s-%d-%d" % (testName, page_description[i], WRITEPCTS[j], 0, traceindex)
					result = requests[i].GET(writeEditUrl + requestID)
					
					# this is the edit form submission:
					edittime = time.strftime("%Y%m%d%H%M%S", time.localtime())
					editsummary = "Edited by grinder test %s at %s" % (requestID.replace("&RequestID=",""), edittime)
					
					editheader = "= %s =" % (editsummary,)
					editheader = editheader.encode('utf-8')
					
					import re
					m = re.match(r"= Edited by grinder test .*? at .*? =", wiki_text[i])
					if(m):
						text = re.sub(r"= Edited by grinder test .*? at .*? =", editheader, wiki_text[i], 1)
					else:
						text = editheader + wiki_text[i]
					
					
					post_data = ( NVPair("wpSection", ""), NVPair("wpStarttime", "0"), NVPair("wpEdittime", edittime),
					NVPair("wpScrolltop", "0"), NVPair("wpAutoSummary", "0"), NVPair("oldid", "0"), NVPair("wpTextbox1", text),
					NVPair("wpSummary", editsummary), NVPair("wpSave", "Save Page"), NVPair("wpEditToken", "+\\"))
					
					requestID = "&RequestID=%s-%s-%s-%d-%d" % (testName, page_description[i], WRITEPCTS[j], 1, traceindex)
					result = requests[i].POST(writeSubmitUrl + requestID, post_data)
					
					requestID = "&RequestID=%s-%s-%s-%d-%d" % (testName, page_description[i], WRITEPCTS[j], 2, traceindex)
					result = requests[i].GET(readUrl + requestID)
			
				else:
					print "READ"
					print readUrl
					
					requestID = "&RequestID=%s-%s-%s-%d-%d" % (testName, page_description[i], WRITEPCTS[j], 0, traceindex)
					result = requests[i].GET(readUrl + requestID)
					
					requestID = "&RequestID=%s-%s-%s-%d-%d" % (testName, page_description[i], WRITEPCTS[j], 1, traceindex)
					result = requests[i].GET(readUrl + requestID)
					
					requestID = "&RequestID=%s-%s-%s-%d-%d" % (testName, page_description[i], WRITEPCTS[j], 2, traceindex)
					result = requests[i].GET(readUrl + requestID)




