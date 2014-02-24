import urllib2, re, subprocess, os

class FoundURL:
    def __init__(self, url):
        self.url = url
class PreventRedirectsHandler(urllib2.HTTPRedirectHandler):
    '''Instead of redirecting, raise an exception to tell the caller
    the new url.'''
    def redirect_request(self, req, fp, code, msg, hdrs, newurl):
        raise FoundURL(newurl)

opener = urllib2.build_opener(PreventRedirectsHandler())
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:9.0.1) Gecko/20100101 Firefox/9.0.1')]

def find_acceptable_url(url):
    '''Follow redirects until some module claims it supports the URL
    or we exhausted the redirects.'''
    if url == '':
        return ''
    updated_url = True
    while updated_url:
        updated_url = False
        try:
            print 'Following %s' % url
            opener.open(url)
        except FoundURL as f:
            url = f.url
            updated_url = True
        except urllib2.HTTPError as e:
            print e
            return '(%s)' % e
        if someone_accepts_url(url):
            print 'Found acceptable destination: %s' % url
            return url
    print 'No more redirects: %s' % url
    return url

modules = []
def register_module(url_regex, module):
    modules.append((re.compile(url_regex), module))

def dispatch_download_pdf(url, filename):
    for url_regex, module in modules:
        if url_regex.match(url):
            if 'download_pdf' in module:
                print 'Using module %s to download pdf...' % module['name']
                return module['download_pdf'](url, filename)
    print 'No suitable pdf module for: %s' % url
    return False

def dispatch_download_bib(url, filename):
    for url_regex, module in modules:
        if url_regex.match(url):
            if 'download_bib' in module:
                print 'Using module %s to download citation...' % module['name']
                return module['download_bib'](url, filename)
    print 'No suitable bib module for: %s' % url
    return False

def someone_accepts_url(url):
    for url_regex, module in modules:
        if url_regex.match(url):
            return True
    return False

def shrink_pdf(path):
    if subprocess.call(['gs', '-sDEVICE=pdfwrite', '-o', path + '~', path]) == 0:
        os.rename(path + '~', path)

def open_pdf(path):
    '''Opens the given file in evince.'''
    if os.fork() == 0:
        # Eat stdout/stderr of evince
        os.dup2(os.open('/dev/null', os.O_WRONLY), 1)
        os.dup2(1, 2)
        os.execvp('evince', ['evince', path])
