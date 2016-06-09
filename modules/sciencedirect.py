import requests
from BeautifulSoup import BeautifulSoup

def download_pdf(url, filename):
    headers = { 'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0' }
    landingpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(landingpage.text)
    pdflink = soup.find('a', { 'id' : 'pdfLink' })
    if pdflink is not None:
        pdflink = pdflink['href']
    else:
        # Try something else.
        pdflink = soup.find('div', { 'id' : 'article-download' })
        if pdflink is None:
            print 'Could not find PDF link on ScienceDirect page.'
            return False
        pdflink = 'http:' + pdflink.a['href']
    # Sciencedirect requires cookies for pdf downloads.
    pdf = requests.get(pdflink, cookies=landingpage.cookies, headers=headers).content
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
