

from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
from HTTPClient import NVPair


test = Test(1, "Wiki Test")

REQUEST_ID_PREFIX="SearchTest"

searchURL = "http://sdcranch10.ecn.purdue.edu/index.php?search=%s&fulltext=Search&title=Test&RequestID=%s-%d"


request = HTTPRequest()
test.record(request)
      
class TestRunner:
  def __call__(self):

    print "SEARCH REQUEST"
    result = request.GET(searchURL % ('Collision', REQUEST_ID_PREFIX, grinder.runNumber))

    print result




