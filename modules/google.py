import urllib, json, re
from BeautifulSoup import BeautifulSoup

class FakeUseragentURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:9.0.1) Gecko/20100101 Firefox/9.0.1"
urllib._urlopener = FakeUseragentURLopener()

base_url = 'http://www.google.com/search?q="%s"+filetype:pdf+|+filetype:ps&filter=0'

def find(query):
    '''Returns the URL to a pdf or ps file, if successful.'''
    url = base_url % urllib.quote_plus(query)
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    results = []
    for link in soup.findAll('h3', { 'class' : 'r' }):
        link = link.a
        title = ''.join([ t.string for t in link ])
        target = link['href']
        results.append({'title': title, 'url': target})
    choice = ask_which_result(results)
    if choice is None:
        return None
    return results[choice-1]['url']

def ask_which_result(results):
    if len(results) == 0:
        print 'No results from Google.'
        return None
    for i in range(len(results)):
        print '%2d. %s\n    %s' % (i+1, results[i]['title'], results[i]['url'])
    choice = raw_input('Please enter a number: [1]')
    if choice == '':
        return 1
    try:
        return int(choice)
    except:
        return None

def download_pdf(result, filename):
    url = find(result['title'])
    if url is None:
        return False
    return urllib.urlretrieve(url, filename) is not None
