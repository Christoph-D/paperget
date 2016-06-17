import urllib, json, re

def find_electronic_edition(bibtex):
    m = re.search('^ *url += +\\{([^}]*)\\}', bibtex, re.MULTILINE)
    if m is None:
        return None
    return m.group(1)

def find(query):
    url = "http://www.dblp.org/search/publ/api/?q=%s&h=5&c=4&f=0&format=json" % urllib.quote_plus(query)
    json_code = urllib.urlopen(url).read()
    try:
        r = json.loads(json_code)
    except ValueError:
        print('Received:\n%s\n\nError: Could not decode JSON!' % json_code)
        return None
    hits = r['result']['hits']
    if hits['@sent'] == '0':
        return None
    result = hits['hit']
    if isinstance(result, list):
        result = result[0]
    bibtex_url = result['info']['url'].replace('/rec/', '/rec/bib2/', 1) + '.bib'
    bibtex = urllib.urlopen(bibtex_url).read()
    result = {
        'bibtex': bibtex,
        'title': result['info']['title'],
        'authors': result['info']['authors']['author'],
        'ee': find_electronic_edition(bibtex),
        'year': int(result['info']['year']),
        'venue': result['info']['venue'],
        }
    return result

def download_bib(result, filename):
    with open(filename, 'w') as f:
        f.write(result['bibtex'])
    return True
