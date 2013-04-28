from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
from HTTPClient import NVPair
import Wikiparser
import re
import time
import random

REQUEST_ID_PREFIX="SimpleReader"

serverURL = grinder.properties.getProperty("request.url")
baseID = int(grinder.properties.getProperty("request.baseid"))
runs =  int(grinder.properties.getProperty("grinder.runs"))

test = Test(1, REQUEST_ID_PREFIX)
request = HTTPRequest()
test.record(request)

class TestRunner:
  def __call__(self):
	result = request.GET(serverURL + "/index.php/Ethernet?RequestID=%s-%d" % (REQUEST_ID_PREFIX, baseID*runs + grinder.runNumber))
	print result