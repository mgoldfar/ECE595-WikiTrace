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
REQUEST_ID_PREFIX="ReadWriteTest"

# Media wiki will redirect if we don't use the RAW url, this makes the scripting easier
serverURL = 'sdcranch10.ecn.purdue.edu'
pagetitle = 'Collision_domain'
pageURL = serverURL + '/index.php/' + pagetitle

URLsuffix = "?action=view&title=Test&RequestID=%s-%d"

readURL = 'http://' + pageURL + "?action=view&title=Test&RequestID=%s-%d"
writeURL = 'http://' + pageURL + "?action=submit&title=Test&&RequestID=%s-%d"

#readRequest = HTTPRequest(url="http://localhost/~michael/index.php?title=FooLink&action=submit&RequestID=post_test&ShowTrace=1")
request = HTTPRequest()
test.record(request)
      
class TestRunner:
  def __call__(self):

    if random.random() < WRITE_PERCENTAGE:
      print "WRITE"

      edittime = time.strftime("%Y%m%d%H%M%S", time.localtime())
      exitsummary = "Edited by grinder test at %s" % (edittime,)

      wikitext = Wikiparser.get_page(pagetitle,serverURL)
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

      result = request.POST(writeURL % (REQUEST_ID_PREFIX, grinder.runNumber), post_data)
      print result
    else:
      print "READ"
      result = request.GET(readURL % (REQUEST_ID_PREFIX, grinder.runNumber))

    print result



