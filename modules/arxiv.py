import requests

def download_pdf(url, filename):
    headers = { 'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0' }
    pdf = requests.get(url.replace('/abs/', '/pdf/'), headers=headers).content
    with open(filename, 'wb') as f:
        f.write(pdf)
    return True

import base
base.register_module('http://arxiv.org/abs/.*',
                     {'name': 'arXiv',
                      'download_pdf': download_pdf,
                      })
