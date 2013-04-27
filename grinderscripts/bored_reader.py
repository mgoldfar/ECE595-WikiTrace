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

test = Test(1, "Wiki Test")

WRITE_PERCENTAGE = 0.1
REQUEST_ID_PREFIX="BoredReaderTest"
READER_OPEN = 0.3
OPEN_AGAIN = 0.2

# Media wiki will redirect if we don't use the RAW url, this makes the scripting easier
serverURL = 'http://sdcranch10.ecn.purdue.edu'
pageURL = serverURL + '/index.php/Collision_domain'
URLsuffix = "?action=view&title=Test&RequestID=%s-%d"


request = HTTPRequest()
test.record(request)


def removeduplicates(oldlist):
  templist = list(set(oldlist))
  
      
class TestRunner:
  def __call__(self):
    reducer = 1
    import Wikiparser
    getlinks = []
    pagecontents = Wikiparser.getpage(pageURL)
    links = Wikiparser.getlinks(pagecontents)
    for l in links:
      if random.random() < READER_OPEN:
        print "Adding new link to open: " + l
        getlinks.append(l)
        result = request.GET(serverURL + l + URLsuffix % (REQUEST_ID_PREFIX, grinder.runNumber))
        print result
    getlinks = list(set(getlinks))
    for l in getlinks:
      print l
    for l in getlinks:
      print "Reader browsing..." + l
      if random.random() < READER_OPEN:
        print "Reader reading the new page" + l
        newpage = Wikiparser.getpage(serverURL + l)
        morelinks = Wikiparser.getlinks(newpage)
        for l2 in morelinks:
          print "Reader browsing more..." + l2
          if random.random() < OPEN_AGAIN / reducer:
            reducer = reducer + 1
            print "Reader adding new link to open [again] : " + l2 + " " + str(getlinks.index(l)+1) + " out of " + str(len(getlinks))
            getlinks.append(l2)
            result = request.GET(serverURL + l2 + URLsuffix % (REQUEST_ID_PREFIX, grinder.runNumber))
            #print result
      else:
        print "Reader not interested in page "  + l + " " + str(getlinks.index(l)+1) + " out of " + str(len(getlinks))
      #getlinks.popleft()

    

