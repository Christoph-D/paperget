#!/usr/bin/python

from modules import *
import os, sys, urllib, re, codecs

base_path = os.environ['HOME'] + '/papers'

def word_ok(word):
    for c in word:
        if ord(c) >= 128:
            return False
    return word != ''

def prepare_query(q):
    '''Strips punctuation and single letter words.'''
    q = re.sub('[.,:/]', '', q)
    q = re.sub('(^| )[a-zA-Z](\.| )', ' ', q)
    q = q.lower()
    q_clean = []
    for word in q.split(' '):
        if word_ok(word):
            q_clean.append('%s*' % word)
    return ' '.join(q_clean)

def get_query():
    q = ' '.join(sys.argv[1:])
    q = prepare_query(q)
    return q

def yes_no(prompt):
    a = raw_input(prompt + ' [Yn]')
    if a == 'Y' or a == 'y' or a == '':
        return True
    if a == 'N' or a == 'n':
        return False
    return yes_no(prompt)

def make_bibkey(result):
    if type(result['authors']) is list:
        first_author = result['authors'][0]
    else:
        first_author = result['authors']
    names = first_author.split(' ')
    last_name = names[-1].lower()
    key = "%s%d" % (last_name, result['year'])
    key = key.encode('ascii', errors='ignore')
    return key

def add_bibkey(result):
    result['key'] = make_bibkey(result)
    if not yes_no("Use the bibtex key '%s'?" % result['key']):
        result['key'] = raw_input('New bibtex key: ')

def add_acceptable_url(result):
    '''Adds the field 'acceptable_url' to the dictionary.  This
    operation is fairly expensive because it needs to resolve multiple
    HTTP redirects, so only call if necessary.'''
    result['acceptable_url'] = base.find_acceptable_url(result['doi'])

def find(query):
    r = dblp.find(query)
    if r is None:
        return None
    for key, value in sorted(r.iteritems()):
        if type(value) is list:
            print "%15s: %s" % (key, ', '.join(value))
        else:
            print "%15s: %s" % (key, value)
    if yes_no("Is this the paper you are looking for?"):
        return r
    return None

def download_pdf(result, path):
    if not base.dispatch_download_pdf(result['acceptable_url'], path):
        print 'Asking google...'
        if not google.download_pdf(result, path):
            print 'Could not download pdf!'
            return
    print 'Successfully downloaded %s' % path
    base.open_pdf(path)

def fix_bibtex(code, bibtex_key):
    '''Basic clean-up of bibtex code. Also sets the proper bibtex key.'''
    # Remove byte order mark because it confuses bibtex.
    if code[:1] == u'\uFEFF':
        code = code[1:]
    code = code.replace(u'\r\n', u'\n')
    # Add empty line at the end if it is missing.
    if code != u'' and code[-1] != u'\n':
        code += u'\n'
    # Fix bibtex key.
    code = re.sub(u'^(@[^ ]*) *\{.*', u'\\1{%s,' % bibtex_key, code)
    return code

def download_bib(result, path, bibtex_key):
    if not base.dispatch_download_bib(result['acceptable_url'], path):
        print 'Falling back to DBLP bibtex information.'
        if not dblp.download_bib(result, path):
            print 'Could not download citation!'
            return
    print 'Successfully downloaded %s' % path
    with codecs.open(path, encoding='utf-8') as f:
        citation = f.read()
    citation = fix_bibtex(citation, bibtex_key)
    with codecs.open(path, encoding='utf-8', mode='w') as f:
        f.write(citation)

query = get_query()
if query == '':
    print "Please provide a non-empty query on the command line."
    sys.exit()
result = find(query)
if result is None:
    print "Could not find the paper. Sorry about that."
    sys.exit()

add_bibkey(result)

pdf_path = '%s/%s.pdf' % (base_path, result['key'])
bib_path = '%s/%s.bib' % (base_path, result['key'])

skip_pdf = os.path.exists(pdf_path)
skip_bib = os.path.exists(bib_path)

if skip_pdf and skip_bib:
    print 'Nothing to do.\n  %s\nand \n  %s\nalready exist.' % (pdf_path, bib_path)
    sys.exit()

add_acceptable_url(result)

if not skip_pdf:
    download_pdf(result, pdf_path)
else:
    print "  %s already exists, skipping." % pdf_path

if not skip_bib:
    download_bib(result, bib_path, result['key'])
else:
    print "  %s already exists, skipping." % bib_path
