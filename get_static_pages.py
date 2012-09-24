#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: ts=2 sts=2 sw=2 noet

try:
    from configparser import ConfigParser
except ImportError: # Python <3
    from ConfigParser import ConfigParser

from lxml import html
from lxml import etree

from pprint import pprint
try:
    from urllib.parse import urlparse
except ImportError: # Python <3
    from urlparse import urlparse
try:
    from urllib import urlopen
except: # Python <3
    from urllib.request import urlopen
try:
    from urllib import urlretrieve
except: # Python <3
    from urllib.request import urlretrieve

import collections
import optparse
import os
import re
import sys

_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
_RESOURCE_DIRNAME = 'resources'
_RESOURCE_URLPREFIX = 'adhocracy.de/'

class PageDownloader(object):
    def __init__(self, base_url, target_dir, overwrite):
        self._base_url = base_url
        self._target_dir = target_dir
        self._resource_dir = os.path.join(self._target_dir, _RESOURCE_DIRNAME)
        self._resource_prefix = _RESOURCE_URLPREFIX + _RESOURCE_DIRNAME + '/'
        self._overwrite = overwrite

        self._pages_to_load = collections.deque()
        self._downloaded = set()

    def make_dirs(self):
        if not os.path.exists(self._target_dir):
            os.mkdir(self._target_dir)
        if not os.path.exists(self._resource_dir):
            os.mkdir(self._resource_dir)

    def _download_resource(self, url):
        filename = os.path.basename(url.split( "/" )[-1])
        fname_path = os.path.join(self._resource_dir, filename)

        if self._overwrite and not os.path.exists(fname_path):
            urlretrieve(url, fname_path)
        return filename

    def _write_html_file(self, fn, content):
        dirpath = os.path.dirname(fn)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)

        with open(fn, 'wb') as f:
            f.write(content)

    def _queue_page(self, path):
        self._pages_to_load.append(path)

    def _queued_pages(self):
        while True:
            if not self._pages_to_load:
                break
            path = self._pages_to_load.popleft()
            if path in self._downloaded:
                continue
            self._downloaded.add(path)
            yield path

    def _handle_page(self, document):
        for img in document.xpath( "//img" ):
            if img.get( 'alt' ) == 'captcha':
                img.set('src', 'about:blank?captcha')
                continue

            filename = self._download_resource(img.get('src'))
            img.set('src', self._resource_prefix + filename )

        for style in document.xpath( "//*[@rel='stylesheet']" ):
            filename = self._download_resource(style.get('href'))
            style.set('src', self._resource_prefix + filename)

        for script in document.xpath( "//script[@src]" ):
            filename = self._download_resource(script.get('src'))
            script.set('src', self._resource_prefix + filename)

        adhocracy_a = document.xpath( \
            "//div[contains( @class, 'menu' )]" \
            + "//a[contains( @href, 'adhocracy.de' )]" \
        )
        for a in adhocracy_a:
            href = urlparse(a.get('href'))
            self._queue_page(href.path)
            a.set('href', href.path)

    def get_page(self, start_path):
        assert not list(self._queued_pages())
        self._queue_page(start_path)

        for page_path in self._queued_pages():
            local_page = '/index' if page_path == '/' else page_path
            local_page = self._target_dir + local_page
            local_page = local_page.rstrip( '/' ) + '.html'

            if not self._overwrite and os.path.exists(local_page):
                continue

            print ("Getting {0}" . format( page_path ))

            url = 'http://' + self._base_url + page_path

            page = urlopen(url)
            e_document = etree.HTML( page.read() )
            page.close()

            self._handle_page(e_document)

            html_document = etree.Element( "html" )
            html_document.append( e_document.xpath( "//head" )[0] )
            html_document.append( e_document.xpath( "//body" )[0] )

            html = etree.tostring(
                html_document,
                pretty_print = True,
                method = "html"
            )
            self._write_html_file(local_page, html)

class DryRunDownloader(PageDownloader):
    def make_dirs(self):
        pass

    def _download_resource(self, fn, html):
        pass

    def _write_html_file(self, fn, html):
        pass


def main():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', help='Base URL to download from')
    parser.add_option('-c', '--config-file', help='Read URL from configuration file')
    parser.add_option('-t', '--target-dir', help='Directory that the static files get stored in')
    parser.add_option('-o', '--overwrite', action='store_true', help='Overwrite existing files')
    parser.add_option('-D', '--dry-run', action='store_true', help='Do not actually touch anything on disk, but test that downloading works')
    (opts, args) = parser.parse_args()

    if opts.url is None and opts.config_file is None:
        parser.error('Please specify a base URL, either with the -u or -c option')
    if opts.url is not None and opts.config_file is not None:
        parser.error('Please use EITHER -u or -c, not both')

    base_url = opts.url
    if not base_url:
        adhocracy_config = ConfigParser()
        adhocracy_config.read(opts.config_file)
        base_url = adhocracy_config.get('filter:theme', 'wordpress_backend')

    if opts.target_dir is None:
        opts.target_dir = os.path.join(_SCRIPT_DIR, 'static')

    dlClass = DryRunDownloader if opts.dry_run else PageDownloader
    dl = dlClass(base_url, opts.target_dir, opts.overwrite)
    dl.make_dirs()

    dl.get_page('/')

if __name__ == '__main__':
    main()

