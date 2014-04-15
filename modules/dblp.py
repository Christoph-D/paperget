import urllib, json, re

def find(query):
    url = "http://www.dblp.org/search/api/?q=%s&h=5&c=4&f=0&format=json" % urllib.quote_plus(query)
    json_code = urllib.urlopen(url).read()
    r = json.loads(json_code)
    hits = r['result']['hits']
    if hits['@sent'] == '0':
        return None
    result = hits['hit']
    if isinstance(result, list):
        result = result[0]
    result = {
        'bibtex_url': result['url'],
        'title': result['info']['title']['text'],
        'authors': result['info']['authors']['author'],
        'doi': result['info']['title']['@ee'],
        'year': int(result['info']['year']),
        'venue': result['info']['venue']['text'],
        'venue_url': 'http://www.dblp.org/' + result['info']['venue']['@url'],
        }
    return result

def download_bib(result, filename):
    bib = urllib.urlopen(result['bibtex_url']).read()
    bib = bib.replace('<pre>', '')
    bib = bib.replace('</pre>', '')
    bib = bib.replace('\r', '')
    result = []
    for line in bib.split('\n'):
        if line != '' and line[0] != '<':
            line = re.sub('<[^>]*>', '', line)
            result.append(line)
    with open(filename, 'w') as f:
        f.write('\n'.join(result))
    return True
