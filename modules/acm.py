import requests, re

download_pdf_regex = re.compile('\s*<a name="FullTextPDF" title="FullText PDF" href="([^"]*).*')

def download_pdf(url, filename):
    headers = { 'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0' }
    landingpage = requests.get(url, headers=headers)
    result = download_pdf_regex.search(landingpage.text)
    if result is None:
        return False
    fulltext_url = 'http://dl.acm.org/' + result.group(1)
    # ACM requires cookies for pdf downloads.
    pdf = requests.get(fulltext_url, cookies=landingpage.cookies, headers=headers).content
    with open(filename, 'wb') as f:
        f.write(pdf)
    return True

import base
base.register_module('http://dl\.acm\.org/citation\.cfm.*',
                     {'name': 'ACM',
                      'download_pdf': download_pdf,
                      })
