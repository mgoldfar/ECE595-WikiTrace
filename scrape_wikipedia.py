#!/usr/bin/env python2.6

import sys, os, re, httplib

interwiki_link = re.compile(r'href=[\'"]/wiki/(\w+)[\'"]')
MAX_DEPTH = 3
SCRAPE_DIR = "scrapes"

if not os.path.exists(SCRAPE_DIR):
	os.mkdir(SCRAPE_DIR)

def get_page(title):
	conn = httplib.HTTPConnection("en.wikipedia.org")
	conn.request("GET", "/wiki/%s" % (title,))
	req = conn.getresponse()
	return req.read()
	
def get_links_for_page(title, depth, page_link_map, links):
	page_content = get_page(title)
	
	with open(os.path.join(SCRAPE_DIR, title), "w") as f:
		f.write(page_content)
	
	hrefs = set(interwiki_link.findall(page_content))
	unseen_hrefs = hrefs.difference(links)
	page_link_map[title] = hrefs
	
	print ".",
	
	if depth < MAX_DEPTH:
		for href in unseen_hrefs:
			if href not in links: # may get updated in function
				links.add(href)
				get_links_for_page(href, depth + 1, page_link_map, links)


page_link_map = {}
links = set()

get_links_for_page("Ethernet", 0, page_link_map, links)

print links
	 

# <a href="/wiki/Media_access_control" title="Media access control">media access control</a>

