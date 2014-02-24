import urllib, re

class FakeUseragentURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:9.0.1) Gecko/20100101 Firefox/9.0.1"
urllib._urlopener = FakeUseragentURLopener()

download_pdf_regex = re.compile('.*<li class="pdf"><a class="sprite pdf-resource-sprite" href="([^"]*)" title="Download PDF.*')
viewstate_regex = re.compile('.*<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([^"]*)" />.*')
eventvalidation_regex = re.compile('.*<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="([^"]*)" />.*')

def download_pdf(url, filename):
    page = urllib.urlopen(url).read()
    result = download_pdf_regex.search(page)
    if result is None:
        return False
    fulltext_url = "http://www.springerlink.com" + result.group(1)
    return urllib.urlretrieve(fulltext_url, filename) is not None

def download_bib(url, filename):
    url += 'export-citation/'
    form = urllib.urlopen(url).read()
    viewstate = viewstate_regex.search(form)
    eventvalidation = eventvalidation_regex.search(form)
    if viewstate is None or eventvalidation is None:
        return False
    viewstate = viewstate.group(1)
    eventvalidation = eventvalidation.group(1)
    data = urllib.urlencode([
            ('__VIEWSTATE', viewstate),
            ('ctl00$ctl14$cultureList', 'en-us'),
            ('ctl00$ctl14$SearchControl$BasicSearchForTextBox', ''),
            ('ctl00$ctl14$SearchControl$BasicAuthorOrEditorTextBox', ''),
            ('ctl00$ctl14$SearchControl$BasicPublicationTextBox', ''),
            ('ctl00$ctl14$SearchControl$BasicVolumeTextBox', ''),
            ('ctl00$ctl14$SearchControl$BasicIssueTextBox', ''),
            ('ctl00$ctl14$SearchControl$BasicPageTextBox', ''),
            ('ctl00$ContentPrimary$ctl00$ctl00$Export', 'CitationOnlyRadioButton'),
            ('ctl00$ContentPrimary$ctl00$ctl00$CitationManagerDropDownList', 'BibTex'),
            ('ctl00$ContentPrimary$ctl00$ctl00$ExportCitationButton', 'Export+Citation'),
            ('__EVENTVALIDATION', eventvalidation)])
    return urllib.urlretrieve(url, filename, data=data) is not None

import base
base.register_module('http://www\.springerlink\.com/content/.*',
                     {'name': 'springerlink',
                      'download_pdf': download_pdf,
                      'download_bib': download_bib,
                      })
