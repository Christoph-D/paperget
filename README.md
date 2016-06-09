Paperget
========

Ever tired of this?

1. Find some scientific article on [DBLP](http://dblp.org/).

2. Click "electronic edition", be forced to navigate some publisher's
   site while all you want is the pdf.

3. Finally find the pdf, with a publisher generated crazy filename.

4. Be forced to go back to DBLP to download the matching bibtex file.

5. Change the pdf/bib filenames to something reasonable.

Paperget automates all of this.

You give paperget fragments of a title, authors, etc., and it figures
out how to download the pdf and bib file and saves both with
reasonable filenames matching the bibtex key.

Example
-------

```
$ ./paperget.py reingold connectivity log space
        authors: Omer Reingold
             ee: http://doi.acm.org/10.1145/1391289.1391291
          title: Undirected connectivity in log-space.
          venue: J. ACM
           year: 2008
Is this the paper you are looking for? [Yn]
Use the bibtex key 'reingold2008'? [Yn]
Following http://doi.acm.org/10.1145/1391289.1391291
Found acceptable destination: http://dl.acm.org/citation.cfm?doid=1391289.1391291
Using module ACM to download pdf...
Successfully downloaded ~/papers/reingold2008.pdf
No suitable bib module for: http://dl.acm.org/citation.cfm?doid=1391289.1391291
Falling back to DBLP bibtex information.
Successfully downloaded ~/papers/reingold2008.bib
```

The path `~/papers/` and the bibtex key schema are hardcoded but can
easily be changed.  TODO: Make this configurable.

What it doesn't do
------------------

Paperget does not break paywalls.  Downloading pdfs from a paywalled
site only works if you have access, for example via your academic
institution.  Having said this, if paperget hits a paywall, it will
ask google for the title of a paper.  Often a paper turns out to be
available for free on the author's website.

Paperget does not support batched downloads.
