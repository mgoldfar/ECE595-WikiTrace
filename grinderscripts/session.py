# The Grinder 3.11
# HTTP script recorded by TCPProxy at Apr 25, 2013 4:47:56 PM

from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
from net.grinder.plugin.http import HTTPPluginControl, HTTPRequest
from HTTPClient import NVPair
connectionDefaults = HTTPPluginControl.getConnectionDefaults()
httpUtilities = HTTPPluginControl.getHTTPUtilities()

# To use a proxy server, uncomment the next line and set the host and port.
# connectionDefaults.setProxyServer("localhost", 8001)

def createRequest(test, url, headers=None):
    """Create an instrumented HTTPRequest."""
    request = HTTPRequest(url=url)
    if headers: request.headers=headers
    test.record(request, HTTPRequest.getHttpMethodFilter())
    return request

# These definitions at the top level of the file are evaluated once,
# when the worker process is started.

connectionDefaults.defaultHeaders = \
  [ NVPair('Accept-Encoding', 'gzip, deflate'),
    NVPair('Accept-Language', 'en-US,en;q=0.5'),
    NVPair('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0'), ]

headers0= \
  [ NVPair('Accept', 'text/css,*/*;q=0.1'),
    NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php/Ethernet'), ]

headers1= \
  [ NVPair('Accept', '*/*'),
    NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php/Ethernet'), ]

headers2= \
  [ NVPair('Accept', '*/*'),
    NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php?title=Ethernet&action=edit'), ]

headers3= \
  [ NVPair('Accept', 'image/png,image/*;q=0.8,*/*;q=0.5'),
    NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php?title=Ethernet&action=edit'), ]

headers4= \
  [ NVPair('Accept', 'application/json, text/javascript, */*; q=0.01'),
    NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php/Main_Page'), ]

url0 = 'http://sdcranch10.ecn.purdue.edu:80'
url1 = 'http://ping.chartbeat.net:80'

request101 = createRequest(Test(101, 'GET Ethernet'), url0)

request201 = createRequest(Test(201, 'GET load.php'), url0, headers0)

request301 = createRequest(Test(301, 'GET load.php'), url0, headers1)

request401 = createRequest(Test(401, 'GET load.php'), url0, headers1)

request501 = createRequest(Test(501, 'GET load.php'), url0, headers0)

request601 = createRequest(Test(601, 'GET load.php'), url0, headers1)

request701 = createRequest(Test(701, 'GET load.php'), url0, headers1)

request801 = createRequest(Test(801, 'GET load.php'), url0, headers1)

request901 = createRequest(Test(901, 'GET load.php'), url0, headers1)

request1001 = createRequest(Test(1001, 'GET index.php'), url0)

request1101 = createRequest(Test(1101, 'GET load.php'), url0, headers2)

request1201 = createRequest(Test(1201, 'GET index.php'), url0, headers2)

request1202 = createRequest(Test(1202, 'GET button_bold.png'), url0, headers3)

request1203 = createRequest(Test(1203, 'GET button_italic.png'), url0, headers3)

request1204 = createRequest(Test(1204, 'GET button_link.png'), url0, headers3)

request1205 = createRequest(Test(1205, 'GET button_headline.png'), url0, headers3)

request1206 = createRequest(Test(1206, 'GET button_nowiki.png'), url0, headers3)

request1207 = createRequest(Test(1207, 'GET button_extlink.png'), url0, headers3)

request1208 = createRequest(Test(1208, 'GET button_hr.png'), url0, headers3)

request1209 = createRequest(Test(1209, 'GET button_sig.png'), url0, headers3)

request1301 = createRequest(Test(1301, 'POST index.php'), url0)

request1401 = createRequest(Test(1401, 'GET ping'), url1)

request1501 = createRequest(Test(1501, 'GET Main_Page'), url0)

request1601 = createRequest(Test(1601, 'GET api.php'), url0, headers4)

request1701 = createRequest(Test(1701, 'GET api.php'), url0, headers4)

request1801 = createRequest(Test(1801, 'GET api.php'), url0, headers4)

request1901 = createRequest(Test(1901, 'GET api.php'), url0, headers4)

request2001 = createRequest(Test(2001, 'GET api.php'), url0, headers4)

request2101 = createRequest(Test(2101, 'GET index.php'), url0)

request2201 = createRequest(Test(2201, 'GET load.php'), url0)

request2301 = createRequest(Test(2301, 'GET load.php'), url0)


class TestRunner:
  """A TestRunner instance is created for each worker thread."""

  # A method for each recorded page.
  def page1(self):
    """GET Ethernet (request 101)."""
    result = request101.GET('/index.php/Ethernet', None,
      ( NVPair('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), ))

    return result

  def page2(self):
    """GET load.php (request 201)."""
    self.token_modules = \
      'mediawiki.legacy.commonPrint,shared|skins.vector'
    self.token_only = \
      'styles'
    result = request201.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&only=' +
      self.token_only +
      '&skin=' +
      self.token_skin +
      '&*')

    return result

  def page3(self):
    """GET load.php (request 301)."""
    self.token_modules = \
      'startup'
    self.token_only = \
      'scripts'
    self.token_skin = \
      'vector'
    result = request301.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&only=' +
      self.token_only +
      '&skin=' +
      self.token_skin +
      '&*')

    return result

  def page4(self):
    """GET load.php (request 401)."""
    self.token_modules = \
      'skins.vector'
    self.token_only = \
      'scripts'
    result = request401.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&only=' +
      self.token_only +
      '&skin=' +
      self.token_skin +
      '&*')

    return result

  def page5(self):
    """GET load.php (request 501)."""
    self.token_modules = \
      'site'
    self.token_only = \
      'styles'
    result = request501.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&only=' +
      self.token_only +
      '&skin=' +
      self.token_skin +
      '&*')

    return result

  def page6(self):
    """GET load.php (request 601)."""
    self.token_debug = \
      'false'
    self.token_lang = \
      'en'
    self.token_modules = \
      'site'
    self.token_only = \
      'scripts'
    self.token_skin = \
      'vector'
    result = request601.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&only=' +
      self.token_only +
      '&skin=' +
      self.token_skin +
      '&*')

    return result

  def page7(self):
    """GET load.php (request 701)."""
    self.token_modules = \
      'jquery,mediawiki'
    self.token_only = \
      'scripts'
    self.token_version = \
      '20130418T015549Z'
    result = request701.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&only=' +
      self.token_only +
      '&skin=' +
      self.token_skin +
      '&version=' +
      self.token_version)
    self.token_ = \
      httpUtilities.valueFromHiddenInput('') # 'false'

    return result

  def page8(self):
    """GET load.php (request 801)."""
    self.token_modules = \
      'jquery.client,cookie,mwExtension|mediawiki.legacy.ajax,wikibits|mediawiki.notify,util|mediawiki.page.startup'
    self.token_version = \
      '20130422T023353Z'
    result = request801.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&skin=' +
      self.token_skin +
      '&version=' +
      self.token_version +
      '&*')

    return result

  def page9(self):
    """GET load.php (request 901)."""
    self.token_modules = \
      'jquery.autoEllipsis,checkboxShiftClick,highlightText,makeCollapsible,mw-jump,placeholder,suggestions|mediawiki.api,searchSuggest,user|mediawiki.page.ready'
    self.token_version = \
      '20130422T023354Z'
    result = request901.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&skin=' +
      self.token_skin +
      '&version=' +
      self.token_version +
      '&*')
    self.token_fulltext = \
      httpUtilities.valueFromHiddenInput('fulltext') # '1'

    return result

  def page10(self):
    """GET index.php (request 1001)."""
    self.token_title = \
      'Ethernet'
    self.token_action = \
      'edit'
    result = request1001.GET('/index.php' +
      '?title=' +
      self.token_title +
      '&action=' +
      self.token_action, None,
      ( NVPair('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php/Ethernet'), ))

    return result

  def page11(self):
    """GET load.php (request 1101)."""
    self.token_modules = \
      'jquery.byteLength,byteLimit,client,cookie,mwExtension,textSelection|mediawiki.action.edit|mediawiki.legacy.ajax,wikibits|mediawiki.notify,util|mediawiki.page.startup'
    self.token_version = \
      '20130422T023353Z'
    result = request1101.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&skin=' +
      self.token_skin +
      '&version=' +
      self.token_version +
      '&*')

    return result

  def page12(self):
    """GET index.php (requests 1201-1209)."""
    self.token_title = \
      'MediaWiki:Common.js/edit.js'
    self.token_action = \
      'raw'
    self.token_ctype = \
      'text/javascript'
    result = request1201.GET('/index.php' +
      '?title=' +
      self.token_title +
      '&action=' +
      self.token_action +
      '&ctype=' +
      self.token_ctype)

    request1202.GET('/skins/common/images/button_bold.png')

    request1203.GET('/skins/common/images/button_italic.png')

    request1204.GET('/skins/common/images/button_link.png')

    request1205.GET('/skins/common/images/button_headline.png')

    request1206.GET('/skins/common/images/button_nowiki.png')

    request1207.GET('/skins/common/images/button_extlink.png')

    request1208.GET('/skins/common/images/button_hr.png')

    request1209.GET('/skins/common/images/button_sig.png')

    return result

  def page13(self):
    """POST index.php (request 1301)."""
    self.token_title = \
      'Ethernet'
    self.token_action = \
      'submit'
    result = request1301.POST('/index.php' +
      '?title=' +
      self.token_title +
      '&action=' +
      self.token_action,
      ( NVPair('wpSection', ''),
        NVPair('wpStarttime', '20130425212914'),
        NVPair('wpEdittime', '20130327104055'),
        NVPair('wpScrolltop', '0'),
        NVPair('wpAutoSummary', 'd41d8cd98f00b204e9800998ecf8427e'),
        NVPair('oldid', '0'),
        NVPair('wpTextbox1', '''GRINDEREDIT: page edited at 4:49 4-25\r
\r
{{Use mdy dates|date=September 2011}}\r
\r
[[Image:Ethernet RJ45 connector p1160054.jpg|thumb|An [[8P8C|8P8C modular connector]] ([[registered jack naming confusion|often called \'\'RJ45\'\']]) commonly used on [[Category 5 cable|cat 5 cable]]s in Ethernet networks]]\r
\r
\'\'\'Ethernet\'\'\' {{IPAc-en|icon|Ë|iË|Î¸|Ér|n|É|t}} is a family of [[computer network]]ing technologies for [[local area network]]s (LANs). Ethernet was commercially introduced in 1980 and standardized in 1985 as [[IEEE 802.3]]. Ethernet has largely replaced competing wired LAN technologies.\r
\r
The [[:Category:Ethernet_standards|Ethernet standards]] comprise several wiring and signaling variants of the [[Physical layer|OSI physical layer]] in use with Ethernet. The original [[10BASE5]] Ethernet used [[coaxial cable]] as a [[shared medium]]. Later the coaxial cables were replaced by [[twisted pair]] and [[optical fiber|fiber optic]] links in conjunction with [[Ethernet hub|hubs]] or [[Ethernet switch|switches]]. Data rates were periodically increased from the original 10 megabits per second to 100 gigabits per second.\r
\r
Systems communicating over Ethernet divide a stream of data into shorter pieces called [[Frame (networking)|frame]]s. Each frame contains source and destination addresses and error-checking data so that damaged data can be detected and re-transmitted. As per the [[OSI model]] Ethernet provides services up to and including the [[data link layer]].\r
\r
Since its commercial release, Ethernet has retained a good degree of compatibility. Features such as the 48-bit [[MAC address]] and [[Ethernet frame]] format have influenced other networking protocols.\r
\r
==History==\r
Ethernet was developed at [[Xerox PARC]] between 1973 and 1974.<ref name=\"metcalfe video\">{{cite video |url=http://www.youtube.com/watch?v=g5MezxMcRmk |title=The History of Ethernet |publisher=NetEvents.tv |date=2006 |accessdate=September 10, 2011}}</ref><ref>{{cite web |url=http://americanhistory.si.edu/collections/object.cfm?key=35&objkey=96 |title=Ethernet Prototype Circuit Board |year=1973 |publisher=Smithsonian National Museum of American History |accessdate=September 2, 2007}}</ref> It was inspired by [[ALOHAnet]], which [[Robert Metcalfe]] had studied as part of his PhD dissertation.<ref name=\"brock\">{{cite book |title=The Second Information Revolution |author=Gerald W. Brock |publisher=Harvard University Press |date=September 25, 2003 |isbn=0-674-01178-3 |page=151}}</ref> The idea was first documented in a memo that Metcalfe wrote on May 22, 1973, where he named it after the disproven [[luminiferous ether]] as an \"omnipresent, completely-passive medium for the propagation of electromagnetic waves\".<ref name=\"metcalfe video\"/><ref name=\"Ethernet name history\">{{Cite journal|publisher=The Register |title=Ethernet â a <strike>networking protocol</strike> name for the ages: Michelson, Morley, and Metcalfe |url=http://www.theregister.co.uk/2009/03/13/metcalfe_remembers/page2.html |accessdate=March 04, 2013 |date=March 13, 2009 |author=Cade Metz |Page=2}}</ref><ref>{{Cite web |title=Inventors of the Modern Computer |url=http://inventors.about.com/library/weekly/aa111598.htm |author=Mary Bellis |publisher=About.com |accessdate=September 10, 2011}}</ref> In 1975, [[Xerox]] filed a patent application listing Metcalfe, [[David Boggs]], [[Chuck Thacker]] and [[Butler Lampson]] as inventors.<ref>{{US patent|4063220}} \"Multipoint data communication system (with collision detection)\"</ref> In 1976, after the system was deployed at PARC, Metcalfe and Boggs published a seminal paper.<ref>{{cite journal\r
 |author1= Robert Metcalfe |author2= David Boggs\r
 | year = 1976\r
 | month = July\r
 | title = Ethernet: Distributed Packet Switching for Local Computer Networks\r
 | journal=[[Communications of the ACM]]\r
 | volume = 19\r
 | issue = 7\r
 | pages = 395â405\r
 | url = http://www.acm.org/classics/apr96/\r
 | doi = 10.1145/360248.360253\r
 |authorlink1= Robert Metcalfe\r
 |authorlink2= David Boggs\r
}}</ref>{{#tag:ref |The experimental Ethernet described in the 1976 paper ran at 2.94&nbsp;Mbit/s and had eight-bit destination and source address fields, so the original Ethernet addresses were not the [[MAC address]]es they are today.<ref>{{cite journal |title= Evolution of the Ethernet Local Computer Network |author1= John F. Shoch |author2= Yogen K. Dalal |author3= David D. Redell |author4= Ronald C. Crane |work=IEEE Computer |date= August 1982 |volume=15 |issue=8 |pages= 14â26 |url= http://ethernethistory.typepad.com/papers/EthernetEvolution.pdf |doi= 10.1109/MC.1982.1654107 |journal= Computer |authorlink1= John F. Shoch }}</ref> By software convention, the 16 bits after the destination and source address fields specified a \"packet type\", but, as the paper says, \"different protocols use disjoint sets of packet types\". Thus the original packet types could vary within each different protocol. This is in contrast to the [[EtherType]] in the IEEE Ethernet standard, which specifies the protocol being used. |group=note }}\r
\r
Metcalfe left Xerox in June 1979 to form [[3Com]].<ref name=\"metcalfe video\"/><ref name=VonBurg2003/> He convinced [[Digital Equipment Corporation]] (DEC), [[Intel]], and Xerox to work together to promote Ethernet as a standard. The so-called \"DIX\" standard, for \"Digital/Intel/Xerox\" specified 10&nbsp;Mbit/s Ethernet, with 48-bit destination and source addresses and a global 16-bit [[Ethertype]]-type field. It was published on September 30, 1980 as \"The Ethernet, A Local Area Network. Data Link Layer and Physical Layer Specifications\".<ref name=\"blue\">{{Cite document |url=http://ethernethistory.typepad.com/papers/EthernetSpec.pdf |date=30 September 1980 |title=The Ethernet, A Local Area Network. Data Link Layer and Physical Layer Specifications, Version 1.0 |author=Digital Equipment Corporation, Intel Corporation and Xerox Corporation |publisher=Xerox Corporation |accessdate=2011-12-10 |postscript=.}}</ref> Version 2 was published in November, 1982<ref>{{Cite document |url=http://decnet.ipv7.net/docs/dundas/aa-k759b-tk.pdf |title=The Ethernet, A Local Area Network. Data Link Layer and Physical Layer Specifications, Version 2.0 |date=November 1982 |author=Digital Equipment Corporation, Intel Corporation and Xerox Corporation |publisher=Xerox Corporation |accessdate=2011-12-10 |postscript=.}}</ref> and defines what has become known as [[Ethernet II]]. Formal [[#Standardization|standardization efforts]] proceeded at the same time.\r
\r
Ethernet initially competed with two largely proprietary systems, [[Token Ring]] and [[Token Bus]]. Because Ethernet was able to adapt to market realities and shift to inexpensive and ubiquitous [[twisted pair]] wiring, these [[proprietary protocol]]s soon found themselves competing in a market inundated by Ethernet products and by the end of the 1980s, Ethernet was clearly the dominant network technology.<ref name=\"metcalfe video\"/> In the process, 3Com became a major company. 3Com shipped its first 10&nbsp;Mbit/s Ethernet 3C100 transceiver in March 1981, and that year started selling adapters for [[PDP-11]]s and [[VAX]]es, as well as [[Multibus]]-based Intel and [[Sun Microsystems]] computers.<ref name=Breyer1999>{{cite book |title=Switched, Fast, and Gigabit Ethernet |year=1999 |author=Robert Breyer & Sean Riley |publisher=Macmillan |isbn=1-57870-073-6}}</ref>{{rp|9}} This was followed quickly by DEC\'s [[Unibus]] to Ethernet adapter, which DEC sold and used internally to build its own corporate network, which reached over 10,000 nodes by 1986, making it one of the largest computer networks in the world at that time.<ref>{{cite book |title=Digital at Work |author=Jamie Parker Pearson |year=1992 |publisher=Digital Press |isbn=1-55558-092-0 |page=163}}</ref> An Ethernet adapter card for the IBM PC was released in 1982 and by 1985, 3Com had sold 100,000.<ref name=VonBurg2003/>\r
\r
Since then Ethernet technology has evolved to meet new bandwidth and market requirements.<ref>{{Cite journal|url=http://www.eetimes.com/electronics-news/4211609/Shifts-growth-ahead-for-10G-Ethernet |title=Shifts, growth ahead for 10G Ethernet |publisher=E Times |date=December 20, 2010 |author=Rick Merritt |accessdate=September 10, 2011}}</ref> In addition to computers, Ethernet is now used to interconnect appliances and other [[Personal Mobile Electronics|personal devices]].<ref name=\"metcalfe video\"/> It is used in [[Industrial Ethernet|industrial applications]] and is quickly replacing legacy data transmission systems in the world\'s telecommunications networks.<ref>{{Cite news |url=http://www.jaymiescotto.com/jsablog/2011/07/29/my-oh-my-ethernet-growth-continues-to-soar-surpasses-legacy/ |title=My oh My â Ethernet Growth Continues to Soar; Surpasses Legacy |date=July 29, 2011 |publisher=Telecom News Now |accessdate=September 10, 2011}}</ref> By 2010, the market for Ethernet equipment amounted to over $16&nbsp;billion per year.<ref>{{Cite journal|publisher=Network World |title=Cisco, Juniper, HP drive Ethernet switch market in Q4 |url=http://www.networkworld.com/news/2010/022210-ethernet-switch-market.html |accessdate=September 10, 2011 |date=February 22, 2010 |author=Jim Duffy}}</ref>\r
\r
==Standardization==\r
In February 1980, the [[Institute of Electrical and Electronics Engineers]] (IEEE) started project 802 to standardize local area networks (LAN).<ref>{{cite web |url=http://www.ieeeusa.org/policy/policy/2001/01aug27IEEE802.pdf |title=Letter to FCC |author=Vic Hayes |date=August 27, 2001 |quote=IEEE 802 has the basic charter to develop and maintain networking standards... IEEE 802 was formed in February 1980... |accessdate=October 22, 2010}}</ref><ref name=VonBurg2003/> The \"DIX-group\" with Gary Robinson (DEC), Phil Arst (Intel), and Bob Printis (Xerox) submitted the so-called \"Blue Book\" [[Carrier sense multiple access with collision detection|CSMA/CD]] specification as a candidate for the LAN specification.<ref name=\"blue\"/> In addition to CSMA/CD, Token Ring (supported by IBM) and Token Bus (selected and henceforward supported by [[General Motors]]) were also considered as candidates for a LAN standard. Competing proposals and broad interest in the initiative led to strong disagreement over which technology to standardize. In December 1980, the group was split into three subgroups, and standardization proceeded separately for each proposal.<ref name=VonBurg2003>{{cite web |url=http://hcd.ucdavis.edu/faculty/webpages/kenney/articles_files/Sponsors,%20Communities,%20and%20Standards:%20Ethernet%20vs.%20Token%20Ring%20in%20the%20Local%20Area%20Networking%20Business.pdf |title=Sponsors, Communities, and Standards: Ethernet vs. Token Ring in the Local Area Networking Business |archiveurl=http://www.webcitation.org/66LCgXKhx |archivedate=2012-03-21 |deadurl=no |author1=Urd Von Burg |author2=Martin Kenny |date=December 2003}}</ref>\r
\r
Delays in the standards process put at risk the market introduction of the [[Xerox Star]] workstation and 3Com\'s Ethernet LAN products. With such business implications in mind, [[David Liddle]] (General Manager, Xerox Office Systems) and Metcalfe (3Com) strongly supported a proposal of Fritz RÃ¶scheisen ([[Siemens]] Private Networks) for an alliance in the emerging office communication market, including Siemens\' support for the international standardization of Ethernet (April 10, 1981). Ingrid Fromm, Siemens\' representative to IEEE 802, quickly achieved broader support for Ethernet beyond IEEE by the establishment of a competing Task Group \"Local Networks\" within the European standards body ECMA TC24. As early as March 1982 ECMA TC24 with its corporate members reached agreement on a standard for CSMA/CD based on the IEEE 802 draft.<ref name=Breyer1999/>{{rp|8}} Because the DIX proposal was most technically complete and because of the speedy action taken by ECMA which decisively contributed to the conciliation of opinions within IEEE, the IEEE 802.3 CSMA/CD standard was approved in December 1982.<ref name=VonBurg2003/> IEEE published the 802.3 standard as a draft in 1983 and as a standard in 1985.\r
\r
Approval of Ethernet on the international level was achieved by a similar, cross-[[partisan (political)|partisan]] action with Fromm as [[liaison officer]] working to integrate [[International Electrotechnical Commission]], TC83 and [[International Organization for Standardization]] (ISO) TC97SC6, and the ISO/IEEE 802/3 standard was approved in 1984.{{Citation needed|date=March 2012}}\r
\r
==Evolution==\r
Ethernet evolved to include higher bandwidth, improved [[media access control]] methods, and different physical media. The coaxial cable was replaced with point-to-point links connected by [[Ethernet repeater]]s or [[Network switch|switches]] to reduce installation costs, increase reliability, and improve management and troubleshooting. Many variants of Ethernet remain in common use.\r
\r
Ethernet stations communicate by sending each other data packets: blocks of data individually sent and delivered. As with other [[IEEE 802]] LANs, each Ethernet station is given a 48-bit [[MAC address]]. The MAC addresses are used to specify both the destination and the source of each data packet. Ethernet establishes link level connections, which can be defined using both the destination and source addresses. On reception of a transmission, the receiver uses the destination address to determine whether the transmission is relevant to the station or should be ignored. Network interfaces normally do not accept packets addressed to other Ethernet stations. Adapters come programmed with a globally unique address.<ref group=note>In some cases, the factory-assigned address can be overridden, either to avoid an address change when an adapter is replaced or to use locally administered addresses.</ref> An [[Ethertype]] field in each frame is used by the operating system on the receiving station to select the appropriate protocol module (i.e. the [[Internet protocol]] module). Ethernet frames are said to be \'\'self-identifying\'\', because of the frame type. Self-identifying frames make it possible to intermix multiple protocols on the same physical network and allow a single computer to use multiple protocols together.<ref>{{cite book |author=[[Douglas E. Comer]] |year=2000 |title=Internetworking with TCP/IP â Principles, Protocols and Architecture |edition=4th |publisher=Prentice Hall |isbn=0-13-018380-6}} 2.4.9 â Ethernet Hardware Addresses, p. 29, explains the filtering.</ref> Despite the evolution of Ethernet technology, all generations of Ethernet (excluding early experimental versions) use the same frame formats<ref>{{cite web|author=Iljitsch van Beijnum|title=Speed matters: how Ethernet went from 3Mbps to 100Gbps... and beyond|url=http://arstechnica.com/gadgets/2011/07/ethernet-how-does-it-work/3/|publisher=[[Ars Technica]]|accessdate=July 15, 2011|quote=All aspects of Ethernet were changed: its MAC procedure, the bit encoding, the wiring... only the packet format has remained the same.}}</ref> (and hence the same interface for higher layers), and can be readily interconnected through [[Ethernet bridge|bridging]].\r
\r
Due to the ubiquity of Ethernet, the ever-decreasing cost of the hardware needed to support it, and the reduced panel space needed by twisted pair Ethernet, most manufacturers now build Ethernet interfaces directly into [[PC motherboard]]s, eliminating the need for installation of a separate network card.<ref>{{cite web |url=http://pcquest.ciol.com/content/search/showarticle.asp?artid=63428 |title=Motherboard Chipsets Roundup |publisher=PCQuest |date=November 1, 2004 |author=Geetaj Channana |quote=While comparing motherboards in the last issue we found that all motherboards support Ethernet connection on board. |accessdate=October 22, 2010}}</ref>\r
\r
===Shared media===<!-- linked from [[5-4-3 rule]] -->\r
[[File:10Base5transcievers.jpg|thumb|[[10BASE5]] Ethernet equipment]]\r
Ethernet was originally based on the idea of computers communicating over a shared coaxial cable acting as a broadcast transmission medium. The methods used were similar to those used in radio systems,<ref group=note>There are fundamental differences between wireless and wired shared-medium communications, such as the fact that it is much easier to detect collisions in a wired system than a wireless system.</ref> with the common cable providing the communication channel likened to the \'\'[[Luminiferous aether]]\'\' in 19th century physics, and it was from this reference that the name \"Ethernet\" was derived.<ref name=\"Spurgeon 2000\">{{cite book |title=Ethernet: The Definitive Guide |author=Charles E. Spurgeon |publisher=O\'Reilly |isbn=978-1-56592-660-8 |year=2000}}</ref>\r
\r
Original Ethernet\'s shared [[coaxial cable]] (the shared medium) traversed a building or campus to every attached machine. A scheme known as [[carrier sense multiple access with collision detection]] (CSMA/CD) governed the way the computers shared the channel. This scheme was simpler than the competing [[token ring]] or [[token bus]] technologies.<ref group=note>In a CSMA/CD system packets must be large enough to guarantee that the leading edge of the propagating wave of the message got to all parts of the medium before the transmitter could stop transmitting, thus guaranteeing that [[collisions]] (two or more packets initiated within a window of time that forced them to overlap) would be discovered. Minimum packet size and the physical medium\'s total length were, thus, closely linked.</ref> Computers were connected to an [[Attachment Unit Interface]] (AUI) [[transceiver]], which was in turn connected to the cable (later with [[thin Ethernet]] the transceiver was integrated into the network adapter). While a simple passive wire was highly reliable for small networks, it was not reliable for large extended networks, where damage to the wire in a single place, or a single bad connector, could make the whole Ethernet segment unusable.<ref group=note>Multipoint systems are also prone to strange failure modes when an electrical discontinuity reflects the signal in such a manner that some nodes would work properly, while others work slowly because of excessive retries or not at all. See [[standing wave]] for an explanation. These could be much more difficult to diagnose than a complete failure of the segment.</ref>\r
\r
Through the first half of the 1980s, Ethernet\'s [[10BASE5]] implementation used a coaxial cable {{convert|0.375|in}} in diameter, later called \"thick Ethernet\" or \"thicknet\". Its successor, [[10BASE2]], called \"thin Ethernet\" or \"thinnet\", used a cable similar to cable television cable of the era. The emphasis was on making installation of the cable easier and less costly.\r
\r
Since all communications happen on the same wire, any information sent by one computer is received by all, even if that information is intended for just one destination.<ref group=note>This \"one speaks, all listen\" property is a security weakness of shared-medium Ethernet, since a node on an Ethernet network can eavesdrop on all traffic on the wire if it so chooses.</ref> The network interface card interrupts the [[central processing unit|CPU]] only when applicable packets are received: The card ignores information not addressed to it.<ref group=note>Unless it is put into [[promiscuous mode]].</ref> Use of a single cable also means that the bandwidth is shared, such that, for example, available bandwidth to each device is halved when two stations are simultaneously active.\r
\r
Collisions corrupt transmitted data and require stations to retransmit. The lost data and retransmissions reduce throughput. In the worst case where multiple active hosts connected with maximum allowed cable length attempt to transmit many short frames, excessive collisions can reduce throughput dramatically. However, a [[Xerox]] report in 1980 studied performance of an existing Ethernet installation under both normal and artificially generated heavy load. The report claims that 98% throughput on the LAN was observed.<ref>{{cite journal\r
  | author=Shoch, John F. and Hupp, Jon A.\r
  | title = Measured performance of an Ethernet local network\r
  | journal=Communications of the ACM\r
  | volume = 23\r
  | issue = 12\r
  | pages = 711â721\r
  | publisher=ACM Press\r
  | year = 1980\r
  | month = December\r
  | url = http://portal.acm.org/citation.cfm?doid=359038.359044#abstract\r
  | issn = 0001-0782\r
  | doi = 10.1145/359038.359044\r
  }}</ref> This is in contrast with [[token passing]] LANs (token ring, token bus), all of which suffer throughput degradation as each new node comes into the LAN, due to token waits. This report was controversial, as modeling showed that collision-based networks theoretically became unstable under loads as low as 37% of nominal capacity. Many early researchers failed to understand these results. Performance on real networks is significantly better.<ref>{{cite journal\r
  | author=Boggs, D.R., Mogul, J.C., and Kent, C.A.\r
  | title = Measured capacity of an Ethernet: myths and reality\r
  | year = 1988\r
  | month = September\r
  | publisher=DEC WRL\r
  | url = http://www.hpl.hp.com/techreports/Compaq-DEC/WRL-88-4.pdf\r
  }}</ref>\r
The [[10BASE-T]] standard introduced a collision-free [[full duplex]] mode of operation that eliminated collisions. Modern Ethernets are entirely collision-free.\r
\r
===Repeaters and hubs===\r
[[Image:Network card.jpg|thumb|A 1990s [[network card|network interface card]] supporting both [[coaxial cable]]-based [[10BASE2]] ([[BNC connector]], left) and twisted pair-based [[Ethernet over twisted pair|10BASE-T]] ([[8P8C]] connector, right)]]{{Main|Ethernet hub}}\r
For signal degradation and timing reasons, coaxial [[Ethernet segment]]s had a restricted size. Somewhat larger networks could be built by using an [[Ethernet repeater]]. Early repeaters had only two ports, allowing, at most, a doubling of network size. Once repeaters with more than two ports became available, it was possible to wire the network in a [[star network|star topology]]. Early experiments with star topologies (called \"Fibernet\") using [[optical fiber]] were published by 1978.<ref>{{cite journal |title= Fibemet: Multimode Optical Fibers for Local Computer Networks |author1= Eric G. Rawson |author2= Robert M. Metcalfe |journal=IEEE transactions on communications |date= July 1978 |volume=26 |issue=7 |pages= 983â990 |url= http://ethernethistory.typepad.com/papers/Fibernet.pdf |doi= 10.1109/TCOM.1978.1094189 |accessdate= June 11, 2011 }}</ref>\r
\r
Shared cable Ethernet was always hard to install in offices because its bus topology was in conflict with the star topology cable plans designed into buildings for telephony. Modifying Ethernet to conform to [[twisted pair]] telephone wiring already installed in commercial buildings provided another opportunity to lower costs, expand the installed base, and leverage building design, and, thus, twisted-pair Ethernet was the next logical development in the mid-1980s.\r
\r
Ethernet on unshielded twisted-pair cables (UTP) began with [[StarLAN]] at 1&nbsp;Mbit/s in the mid-1980s.  In 1987 [[SynOptics]] introduced the first twisted-pair Ethernet at 10&nbsp;Mbit/s in a star-wired cabling topology with a central hub, later called [[LattisNet]].<ref>\r
   {{cite book\r
   |title = Ethernet; The Definitive Guide\r
   |publisher=O\'Reilly\r
   |author=Spurgeon, Charles E.\r
   |year = 2000\r
   |isbn = 1-56592-660-9\r
   |series = Nutshell Handbook\r
   |page = 29\r
   |url = http://books.google.com/?id=MRChaUQr0Q0C&pg=PA20&lpg=PA20&dq=synoptics+unshielded+twisted+pair#v=onepage&q=synoptics&f=false\r
   }}\r
</ref><ref>\r
   {{cite book\r
   | title = The Triumph of Ethernet: technological communities and the battle for the LAN standard\r
   | author=Urs von Burg\r
   | publisher=Stanford University Press |year= 2001\r
   |url= http://books.google.com/books?id=ooBqdIXIqbwC&pg=PA175\r
   | isbn = 0-8047-4094-1\r
   | page = 175\r
   }}\r
</ref><ref name=VonBurg2003/>\r
These evolved into 10BASE-T, which was designed for point-to-point links only, and all termination was built into the device. This changed repeaters from a specialist device used at the center of large networks to a device that every twisted pair-based network with more than two machines had to use. The tree structure that resulted from this made Ethernet networks easier to maintain by preventing most faults with one peer or its associated cable from affecting other devices on the network.\r
\r
Despite the physical star topology and the presence of separate transmit and receive channels in the twisted pair and fiber media, repeater based Ethernet networks still use half-duplex and CSMA/CD, with only minimal activity by the repeater, primarily the Collision Enforcement signal, in dealing with packet collisions. Every packet is sent to every port on the repeater, so bandwidth and security problems are not addressed. The total throughput of the repeater is limited to that of a single link, and all links must operate at the same speed.\r
\r
===Bridging and switching===<!--[[Full-duplex Ethernet]] redirects here-->\r
[[File:Network switches.jpg|thumb|[[Patch cable]]s with [[patch field]]s of two Ethernet switches]]\r
{{Main|Ethernet switch|Bridging (networking)|}}\r
While repeaters could isolate some aspects of [[Ethernet segment]]s, such as cable breakages, they still forwarded all traffic to all Ethernet devices. This created practical limits on how many machines could communicate on an Ethernet network. The entire network was one [[collision domain]], and all hosts had to be able to detect collisions anywhere on the network. This limited the number of repeaters between the farthest nodes. Segments joined by repeaters had to all operate at the same speed, making phased-in upgrades impossible.\r
\r
To alleviate these problems, bridging was created to communicate at the data link layer while isolating the physical layer. With bridging, only well-formed Ethernet packets are forwarded from one Ethernet segment to another; collisions and packet errors are isolated. Prior to learning of network devices on the different segments, Ethernet bridges (and switches) work somewhat like Ethernet repeaters, passing all traffic between segments. After the bridge learns the addresses associated with each port, it forwards network traffic only to the necessary segments, improving overall performance. [[broadcasting (networking)|Broadcast]] traffic is still forwarded to all network segments. Bridges also overcame the limits on total segments between two hosts and allowed the mixing of speeds, both of which are critical to deployment of [[Fast Ethernet]].\r
\r
In 1989, the networking company [[Kalpana (company)|Kalpana]] introduced their EtherSwitch, the first Ethernet switch.<ref group=note>The term \'\'switch\'\' was invented by device manufacturers and does not appear in the 802.3 standard.</ref> This worked somewhat differently from an Ethernet bridge, where only the header of the incoming packet would be examined before it was either dropped or forwarded to another segment.  This greatly reduced the forwarding latency and the processing load on the network device.   One drawback of this [[Cut-through switching|cut-through]] switching method was that packets that had been corrupted would still be propagated through the network, so a jabbering station could continue to disrupt the entire network.  The eventual remedy for this was a return to the original [[store and forward]] approach of bridging, where the packet would be read into a buffer on the switch in its entirety, verified against its checksum and then forwarded, but using more powerful [[application-specific integrated circuit]]s. Hence, the bridging is then done in hardware, allowing packets to be forwarded at full wire speed.\r
\r
When a twisted pair or fiber link segment is used and neither end is connected to a repeater, [[full-duplex]] Ethernet becomes possible over that segment.  In full-duplex mode, both devices can transmit and receive to and from each other at the same time, and there is no collision domain.  This doubles the aggregate bandwidth of the link and is sometimes advertised as double the link speed (e.g., 200&nbsp;Mbit/s).<ref group=note>This is misleading, as performance will double only if traffic patterns are symmetrical.</ref> The elimination of the collision domain for these connections also means that all the link\'s bandwidth can be used by the two devices on that segment and that segment length is not limited by the need for correct collision detection.\r
\r
Since packets are typically delivered only to the port they are intended for, traffic on a switched Ethernet is less public than on shared-medium Ethernet. <span id=\"switch_vulnerabilities\">Despite this, switched Ethernet should still be regarded as an insecure network technology, because it is easy to subvert switched Ethernet systems by means such as [[ARP spoofing]] and [[MAC flooding]].</span>\r
\r
The bandwidth advantages, the improved isolation of devices from each other, the ability to easily mix different speeds of devices and the elimination of the chaining limits inherent in non-switched Ethernet have made switched Ethernet the dominant network technology.<ref>{{cite web |url=http://www.cisco.com/en/US/solutions/collateral/ns340/ns394/ns74/ns149/net_business_benefit09186a00800c92b9_ps6600_Products_White_Paper.html |quote=Respondents were first asked about their current and planned desktop LAN attachment standards. The results were clearâswitched Fast Ethernet is the dominant choice for desktop connectivity to the network |title=Token Ring-to-Ethernet Migration |publisher=Cisco |accessdate=October 22, 2010}}</ref>\r
\r
===Advanced networking===\r
[[File:Coreswitch (2634205113).jpg|thumb|A core Ethernet switch]]\r
Simple switched Ethernet networks, while a great improvement over repeater-based Ethernet, suffer from single points of failure, attacks that trick switches or hosts into sending data to a machine even if it is not intended for it, scalability and security issues with regard to [[broadcast radiation]] and [[multicast]] traffic, and bandwidth choke points where a lot of traffic is forced down a single link.{{Citation needed|date=October 2010}}\r
\r
Advanced networking features in switches and routers combat these issues through means including [[spanning-tree protocol]] to maintain the active links of the network as a tree while allowing physical loops for redundancy, port security and protection features such as [[Media_access_control|MAC]] lock down and broadcast radiation filtering, [[virtual LAN]]s to keep different classes of users separate while using the same physical infrastructure, [[multilayer switch]]ing to route between different classes and [[link aggregation]] to add bandwidth to overloaded links and to provide some measure of redundancy.\r
\r
[[IEEE 802.1aq]] ([[shortest path bridging]]) includes the use of the [[link-state routing protocol]] [[IS-IS]] to allow larger networks with shortest path routes between devices.  In 2012 it was stated by David Allan and Nigel Bragg, in \'\'802.1aq Shortest Path Bridging Design and Evolution: The Architect\'s Perspective\'\' that shortest path bridging is one of the most significant enhancements in Ethernet\'s history.<ref>[http://www.eabooks.com.au/epages/eab.sf/en_au/?ObjectPath=/Shops/eabooks/Products/9781118148662 802.1aq Shortest Path Bridging Design and Evolution: The Architect\'s Perspective]</ref>\r
\r
==Varieties of Ethernet==\r
{{Main|Ethernet physical layer}}\r
\r
The Ethernet physical layer evolved over a considerable time span and encompasses coaxial, twisted pair and fiber optic physical media interfaces and speeds from 10 Mbit to 100 Gbit. The most common forms used are [[Ethernet over twisted pair|10BASE-T, 100BASE-TX, and 1000BASE-T]]. All three utilize twisted pair cables and 8P8C modular connectors. They run at {{nowrap|10 Mbit/s}}, {{nowrap|100 Mbit/s}}, and {{nowrap|1 Gbit/s}}, respectively. [[Optical fiber|Fiber optic]] variants of Ethernet offer high performance, electrical isolation and distance (tens of kilometers with some versions). In general, network [[protocol stack]] software will work similarly on all varieties.\r
\r
==Ethernet frames==\r
{{main|Ethernet frame}}\r
\r
A data packet on the wire is called a frame. A frame begins with [[preamble (communication)|preamble]] and [[start frame delimiter]], followed by an Ethernet header featuring source and destination MAC addresses. The middle section of the frame consists of payload data including any headers for other protocols (e.g., [[Internet Protocol]]) carried in the frame. The frame ends with a 32-bit [[cyclic redundancy check]], which is used to detect corruption of data in transit.\r
\r
==Autonegotiation==\r
{{Main|Autonegotiation}}\r
Autonegotiation is the procedure by which two connected devices choose common transmission parameters, e.g. speed and duplex mode. Autonegotiation was an optional feature on first introduction of 100BASE-TX, while it is also backward compatible with 10BASE-T. Autonegotiation is mandatory for 1000BASE-T.\r
\r
==See also==\r
{{Portal|Computer networking|Computer Science}}\r
*[[ARCNET]]\r
*[[Chaosnet]]\r
*[[Ethernet crossover cable]]\r
*[[Fiber media converter]]\r
*[[Gigabit Ethernet]]\r
*[[Gigabit interface converter]] \r
*[[Industrial Ethernet]]\r
*[[List of device bit rates]]\r
*[[LocalTalk]]\r
*[[Metro Ethernet]]\r
*[[Media Independent Interface]] \r
*[[PHY (chip)]]\r
*[[Power over Ethernet]]\r
*[[Point-to-Point Protocol over Ethernet]]\r
*[[Small form-factor pluggable transceiver]] \r
*[[Terabit Ethernet]]\r
*[[Wake-on-LAN]]\r
*[[10 Gigabit Ethernet]]\r
*[[100 Gigabit Ethernet]]\r
*[[5-4-3 rule]]\r
\r
==Notes==\r
{{reflist|group=\"note\"|colwidth=30em}}\r
\r
==References==\r
{{reflist|colwidth=30em}}\r
\r
==Further reading==\r
*{{cite journal\r
 | author=Digital Equipment Corporation, Intel Corporation, Xerox Corporation\r
 | date = September, 1980\r
 | title = The Ethernet: A Local Area Network\r
 | url = http://portal.acm.org/citation.cfm?id=1015591.1015594\r
 | doi=10.1145/1015591.1015594\r
 | journal=ACM SIGCOMM Computer Communication Review\r
 | volume=11\r
 | issue=3\r
 | pages=20\r
 }}&nbsp;â Version 1.0 of the DIX specification.\r
* {{Cite web |title=Internetworking Technology Handbook |chapter=Ethernet |url=http://docwiki.cisco.com/wiki/Ethernet_Technologies |publisher=Cisco Systems |accessdate= April 11, 2011 }}\r
\r
== External links ==\r
{{Commons category}}\r
*[http://www.ieee802.org/3/ IEEE 802.3 Ethernet working group]\r
*[http://standards.ieee.org/getieee802/802.3.html IEEE 802.3-2008 standard]\r
\r
{{Ethernet}}\r
{{Basic computer components}}\r
\r
[[Category:Ethernet| ]]\r
[[Category:American inventions]]\r
[[Category:IEEE standards]]\r
\r
{{Link GA|de}}\r
'''),
        NVPair('wpSummary', ''),
        NVPair('wpSave', 'Save page'),
        NVPair('wpEditToken', '+\\'), ),
      ( NVPair('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php?title=Ethernet&action=edit'),
        NVPair('Content-Type', 'multipart/form-data; boundary=---------------------------190513402010395305381584506687'), ),
      True)

    return result

  def page15(self):
    """GET Main_Page (request 1501)."""
    result = request1501.GET('/index.php/Main_Page', None,
      ( NVPair('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php?title=Ethernet&action=submit'), ))

    return result

  def page21(self):
    """GET index.php (request 2101)."""
    self.token_fulltext = \
      'Search'
    self.token_title = \
      'Special:Search'
    result = request2101.GET('/index.php' +
      '?search=' +
      self.token_search +
      '&fulltext=' +
      self.token_fulltext +
      '&title=' +
      self.token_title, None,
      ( NVPair('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php/Main_Page'), ))

    return result

  def page22(self):
    """GET load.php (request 2201)."""
    self.token_modules = \
      'mediawiki.legacy.commonPrint,shared|mediawiki.special|skins.vector'
    self.token_only = \
      'styles'
    result = request2201.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&only=' +
      self.token_only +
      '&skin=' +
      self.token_skin +
      '&*', None,
      ( NVPair('Accept', 'text/css,*/*;q=0.1'),
        NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php?search=collision&fulltext=Search&title=Special%3ASearch'), ))

    return result

  def page23(self):
    """GET load.php (request 2301)."""
    self.token_modules = \
      'jquery.autoEllipsis,checkboxShiftClick,highlightText,makeCollapsible,mw-jump,placeholder,suggestions|mediawiki.api,searchSuggest,user|mediawiki.page.ready|mediawiki.special.search'
    self.token_version = \
      '20130422T023354Z'
    result = request2301.GET('/load.php' +
      '?debug=' +
      self.token_debug +
      '&lang=' +
      self.token_lang +
      '&modules=' +
      self.token_modules +
      '&skin=' +
      self.token_skin +
      '&version=' +
      self.token_version +
      '&*', None,
      ( NVPair('Accept', '*/*'),
        NVPair('Referer', 'http://sdcranch10.ecn.purdue.edu/index.php?search=collision&fulltext=Search&title=Special%3ASearch'), ))
    self.token_fulltext = \
      httpUtilities.valueFromHiddenInput('fulltext') # '1'

    return result

  def __call__(self):
    """Called for every run performed by the worker thread."""
    self.page1()      # GET Ethernet (request 101)

    grinder.sleep(69)
    self.page2()      # GET load.php (request 201)
    self.page3()      # GET load.php (request 301)
    self.page4()      # GET load.php (request 401)
    self.page5()      # GET load.php (request 501)
    self.page6()      # GET load.php (request 601)

    grinder.sleep(24)
    self.page7()      # GET load.php (request 701)

    grinder.sleep(144)
    self.page8()      # GET load.php (request 801)

    grinder.sleep(74)
    self.page9()      # GET load.php (request 901)

    grinder.sleep(13566)
    self.page10()     # GET index.php (request 1001)

    grinder.sleep(89)
    self.page11()     # GET load.php (request 1101)

    grinder.sleep(79)
    self.page12()     # GET index.php (requests 1201-1209)

    grinder.sleep(31210)
    self.page13()     # POST index.php (request 1301)
    self.page14()     # GET ping (request 1401)

    grinder.sleep(5666)
    self.page15()     # GET Main_Page (request 1501)

    grinder.sleep(2803)
    self.page16()     # GET api.php (request 1601)

    grinder.sleep(64)
    self.page17()     # GET api.php (request 1701)
    self.page18()     # GET api.php (request 1801)
    self.page19()     # GET api.php (request 1901)

    grinder.sleep(359)
    self.page20()     # GET api.php (request 2001)

    grinder.sleep(2000)
    self.page21()     # GET index.php (request 2101)

    grinder.sleep(34)
    self.page22()     # GET load.php (request 2201)

    grinder.sleep(127)
    self.page23()     # GET load.php (request 2301)


# Instrument page methods.
Test(100, 'Page 1').record(TestRunner.page1)
Test(200, 'Page 2').record(TestRunner.page2)
Test(300, 'Page 3').record(TestRunner.page3)
Test(400, 'Page 4').record(TestRunner.page4)
Test(500, 'Page 5').record(TestRunner.page5)
Test(600, 'Page 6').record(TestRunner.page6)
Test(700, 'Page 7').record(TestRunner.page7)
Test(800, 'Page 8').record(TestRunner.page8)
Test(900, 'Page 9').record(TestRunner.page9)
Test(1000, 'Page 10').record(TestRunner.page10)
Test(1100, 'Page 11').record(TestRunner.page11)
Test(1200, 'Page 12').record(TestRunner.page12)
Test(1300, 'Page 13').record(TestRunner.page13)
Test(1400, 'Page 14').record(TestRunner.page14)
Test(1500, 'Page 15').record(TestRunner.page15)
Test(1600, 'Page 16').record(TestRunner.page16)
Test(1700, 'Page 17').record(TestRunner.page17)
Test(1800, 'Page 18').record(TestRunner.page18)
Test(1900, 'Page 19').record(TestRunner.page19)
Test(2000, 'Page 20').record(TestRunner.page20)
Test(2100, 'Page 21').record(TestRunner.page21)
Test(2200, 'Page 22').record(TestRunner.page22)
Test(2300, 'Page 23').record(TestRunner.page23)
