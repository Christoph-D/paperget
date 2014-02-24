import urllib2, cookielib, re

# ACM requires cookies for pdf downloads.
cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:9.0.1) Gecko/20100101 Firefox/9.0.1')]

download_pdf_regex = re.compile('\s*<a name="FullTextPDF" title="FullText PDF" href="([^"]*).*')

def download_pdf(url, filename):
    page = opener.open(url).read()
    result = download_pdf_regex.search(page)
    if result is None:
        return False
    fulltext_url = 'http://dl.acm.org/' + result.group(1)
    pdf = opener.open(fulltext_url).read()
    with open(filename, 'wb') as f:
        f.write(pdf)
    return True

import base
base.register_module('http://dl\.acm\.org/citation\.cfm.*',
                     {'name': 'ACM',
                      'download_pdf': download_pdf,
                      })
