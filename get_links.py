#!/usr/bin/env python

"""
Extract all links from a web page
=================================
Author:  Laszlo Szathmary, 2011 (jabba.laci@gmail.com)
Website: https://pythonadventures.wordpress.com/2011/03/10/extract-all-links-from-a-web-page/
GitHub:  https://github.com/jabbalaci/Bash-Utils

Given a webpage, extract all links. Now groks gzip

Usage:
------
./get_links.py <URL>
"""

import sys
import urllib
import urlparse
import gzip
from StringIO import StringIO

from BeautifulSoup import BeautifulSoup


class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'


def process(url):
    myopener = MyOpener()

    try:
        response = myopener.open(url)
    except HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    else:
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            the_page = f.read()
        else:
            the_page = response.read()
        response.close()

    soup = BeautifulSoup(the_page)

    for tag in soup.findAll('a', href=True):
        tag['href'] = urlparse.urljoin(url, tag['href'])
        print tag['href']
# process(url)


def main():
    if len(sys.argv) == 1:
        print "Jabba's Link Extractor v0.1"
        print "Usage: %s URL [URL]..." % sys.argv[0]
        sys.exit(1)
    # else, if at least one parameter was passed
    for url in sys.argv[1:]:
        process(url)
# main()

#############################################################################

if __name__ == "__main__":
    main()

