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
REQUEST_ID_PREFIX="BoredWriterTest"
WRITER_OPEN = 0.3
OPEN_AGAIN = 0.2

# Media wiki will redirect if we don't use the RAW url, this makes the scripting easier
serverURL = 'sdcranch10.ecn.purdue.edu'
pagetitle = 'Collision_domain'
pageURL = serverURL + '/index.php/' + pagetitle

URLsuffix = "?action=view&title=Test&RequestID=%s-%d"

readURL = 'http://' + pageURL + "?action=view&title=Test&RequestID=%s-%d"
writeURL = 'http://' + pageURL + "?action=submit&title=Test&&RequestID=%s-%d"


request = HTTPRequest()
test.record(request)


def removeduplicates(oldlist):
  templist = list(set(oldlist))
  
      
class TestRunner:
  def __call__(self):
    reducer = 1
    import Wikiparser
    getlinks = []
    pagecontents = Wikiparser.getpage('http://' + pageURL)
    links = Wikiparser.getlinks(pagecontents)
    for l in links:
      if random.random() < WRITER_OPEN:
        print "Adding new link to edit: " + l
        getlinks.append(l)
        
        edittime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        exitsummary = "Edited by grinder test at %s" % (edittime,)
        import re
        linktext = re.search('/([^/]+)$', l)


        wikitext = Wikiparser.get_page(linktext.group(1),serverURL)

        m = re.match('GRINDEREDIT', wikitext)
        if(m):
          wikitext = re.sub(r'GRINDEREDIT: \d*', 'GRINDEREDIT: ' + str(edittime), wikitext)
        else:
          wikitext = 'GRINDEREDIT: ' + str(edittime) + "\n\n" + wikitext

        post_data = ( NVPair("wpSection", ""), NVPair("wpStarttime", "0"), NVPair("wpEdittime", edittime),
        NVPair("wpScrolltop", "0"), NVPair("wpAutoSummary", "0"), NVPair("oldid", "0"), NVPair("wpTextbox1", wikitext),
        NVPair("wpSummary", exitsummary), NVPair("wpSave", "Save Page"), NVPair("wpEditToken", "+\\"))

        result = request.POST('http://' + serverURL + '/index.php/' + linktext.group(1) + "?action=submit&title=Test&&RequestID=%s-%d" % (REQUEST_ID_PREFIX, grinder.runNumber), post_data)

        print result
    getlinks = list(set(getlinks))
    for l in getlinks:
      print l
    for l in getlinks:
      print "Writer browsing..." + l
      if random.random() < WRITER_OPEN:
        print "Writer editing new page" + l
        newpage = Wikiparser.getpage('http://' + serverURL + l)
        morelinks = Wikiparser.getlinks(newpage)
        for l2 in morelinks:
          print "Writer browsing more..." + l2
          if random.random() < OPEN_AGAIN / reducer:
            reducer = reducer + 1
            print "Writer adding new link to open [again] : " + l2 + " " + str(getlinks.index(l)+1) + " out of " + str(len(getlinks))
            getlinks.append(l2)
            edittime = time.strftime("%Y%m%d%H%M%S", time.localtime())
            exitsummary = "Edited by grinder test at %s" % (edittime,)
            
            linktext = re.search('/([^/]+)$', l)
            wikitext = Wikiparser.get_page(linktext.group(1),serverURL)

            import re
            m = re.match('GRINDEREDIT', wikitext)
            if(m):
              wikitext = re.sub(r'GRINDEREDIT: \d*', 'GRINDEREDIT: ' + str(edittime), wikitext)
            else:
              wikitext = 'GRINDEREDIT: ' + str(edittime) + "\n\n" + wikitext
            #print wikitext
            post_data = ( NVPair("wpSection", ""), NVPair("wpStarttime", "0"), NVPair("wpEdittime", edittime),
            NVPair("wpScrolltop", "0"), NVPair("wpAutoSummary", "0"), NVPair("oldid", "0"), NVPair("wpTextbox1", wikitext),
            NVPair("wpSummary", exitsummary), NVPair("wpSave", "Save Page"), NVPair("wpEditToken", "+\\"))

            result = request.POST('http://' + serverURL + '/index.php/' + linktext.group(1) + "?action=submit&title=Test&&RequestID=%s-%d" % (REQUEST_ID_PREFIX, grinder.runNumber), post_data)
            #print result
      else:
        print "Writer not interested in page "  + l + " " + str(getlinks.index(l)+1) + " out of " + str(len(getlinks))
      #getlinks.popleft()

    

