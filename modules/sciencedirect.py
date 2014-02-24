import urllib2, cookielib
from BeautifulSoup import BeautifulSoup

# Sciencedirect requires cookies for pdf downloads.
cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:9.0.1) Gecko/20100101 Firefox/9.0.1')]

def download_pdf(url, filename):
    html = opener.open(url).read()
    soup = BeautifulSoup(html)
    pdflink = soup.find('a', { 'id' : 'pdfLink' })
    if pdflink is None:
        print 'Could not find PDF link on ScienceDirect page.'
        return False
    pdf = opener.open(pdflink['href']).read()
    if pdf[:4] != '%PDF':
        print 'You do not seem to have the permission to view this pdf.'
        return False
    with open(filename, 'wb') as f:
        f.write(pdf)
    return True

import base
base.register_module('http://www\.sciencedirect\.com/science/article/.*',
                     {'name': 'sciencedirect',
                      'download_pdf': download_pdf,
                      })
