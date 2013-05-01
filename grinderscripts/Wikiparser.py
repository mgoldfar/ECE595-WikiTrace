#!/usr/bin/env python2.6


from HTMLParser import HTMLParser
import sys, os, re, urllib2, httplib

pageURL = 'http://sdcranch10.ecn.purdue.edu/index.php/Collision_domain'

def getpage(URL):
  response = urllib2.urlopen(URL)
  html = response.read()
  return html

def getlinks(page):
  import re
  filter1 = re.findall('<a href="?\'?([^"\'>]*)', page)
  links = []
  for i in filter1:
    m = re.match('/index.php/', i)
    n = re.search(':', i)
    p = re.search("readlink", i)
    if(m and not n and not p):
      links.append(i)

  return links
        
def trim_html(page):
  import re
  m = re.search('.*</span>(.*\'{3}.+?)<span', page, re.DOTALL)
  if (m):
    firstpass =  m.group(1)
    secondpass = re.sub(r';lt;','<', firstpass)
    thirdpass = re.sub(r';gt;','>', secondpass)
    fourthpass = re.sub(r';quot;','\"',thirdpass)
    fifthpass = re.sub(r'&amp','',fourthpass)
    return fifthpass
  else:
    return "No Match"

def get_page(title, server):
	conn = httplib.HTTPConnection(server)
	conn.request("GET", "/api.php?action=query&titles=%s&prop=revisions&rvprop=content" % (title,))
	req = conn.getresponse()
	return trim_html(req.read())
	
#webpage = getpage(pageURL)
#print webpage
#links = getlinks(webpage)

#print "OUTPUTTING LINKS NOW \n\n"

#for i in links:
#  print i
  


