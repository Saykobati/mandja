#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Plamen Valov

# This file is part of `mandja` program.
# `mandja` is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.

# Mandja is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.


import re
from logging import debug, info, warn, error, critical
from collections import namedtuple
from urlparse import urlparse, ParseResult
import requests

from .common import removeWWW
from .parser import is_content_type_text


HeadData = namedtuple("HeadData", ["code", "headers", "error", "error_msg"])
ContentData = namedtuple("ContentData", ["code", "headers", "error", "error_msg", "content", "final_url"])
URLInfoData = namedtuple("URLInfoData", ["url", "status", "from_domain"])


class CrawlerError(StandardError):
    pass


class CrawlerURLError(CrawlerError):
    pass


class CrawlerContentError(CrawlerError):
    pass


class Crawler(object):
    def __init__(self, start_url, url_parser, session_mng, go_regex, do_head_ping=False, httpauth_creds=None):
        self._url_parser = url_parser
        self._session = session_mng

        self.httpauth_creds = httpauth_creds

        start_url = start_url if not self._session.get_restore_url() else self._session.get_restore_url()

        if(not isinstance(start_url, ParseResult)):
            start_url = urlparse(start_url)
            if(not start_url.scheme):
                raise CrawlerURLError
            elif(not start_url.netloc):
                raise CrawlerURLError

        self._default_user_agent = ('Mozilla/4.0 (compatible; MSIE 7.0; '
                                    'Windows NT 6.0; SU 3.1; SLCC1; .NET '
                                    'CLR 2.0.50727; .NET CLR 3.0.04506; '
                                    '.NET CLR 1.1.4322; .NET CLR 3.5.21022)')
        self._default_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                 'User-Agent': self._default_user_agent,
                                 'Accept-Language': 'en-us,en;q=0.5',
                                 'Accept-Encoding': 'gzip,deflate',
                                 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}
        self._proxy_keep_alive_headers = {'Keep-Alive': '115',
                                          'Proxy-Connection': 'keep-alive'}
        self._keep_alive_headers = {'Keep-Alive': '115',
                                    'Connection': 'keep-alive'}

        self._start_url = start_url.geturl()
        self._start_scheme = start_url.scheme

        self._request = requests.Session()

        self._checked_url_pool = set()
        self._not_checked_url_pool = set()

        self.go_regex_pattern = go_regex
        self.go_regex = re.compile(go_regex)

        self.do_head_ping = do_head_ping

    def _get_htauth_creds(self, netloc):
        try:
            c = self.httpauth_creds.get(netloc, {})
            u = c.get("username", None)
            p = c.get("password", None)
            return (u, p) if u and p else None
        except Exception, err:
            warn("Could not retreive credentials - probably bad httpauth_creds format: %s" % str(err))
            return None

    def _url_to_abs_url(self, url_str, default_netloc):
        us = url_str.replace("&amp;", "&")
        url = urlparse(us, self._start_scheme)

        if not url.netloc and url.scheme in ("http", "https"):
            netloc = default_netloc
        else:
            netloc = url.netloc

        return ParseResult(url.scheme, netloc, url.path, url.params, url.query, url.fragment).geturl()

    def _do_proceed_traverse(self, url_str):
        url = urlparse(url_str, self._start_scheme)
        if url.netloc in self._session.start_domains and self.go_regex.match(url.geturl()):
            return True
        else:
            return False

    def head_ping(self, url):
        if(not isinstance(url, ParseResult)):
            url = urlparse(url)

        error = False
        err_msg = None

        creds = self._get_htauth_creds(url.netloc)

        try:
            resp = self._request.head(url.geturl(), headers=self._default_headers, verify=False, auth=creds)
            code = resp.status_code
            headers = resp.headers
        except Exception, e:
            code = None
            headers = None
            error = True
            err_msg = str(e)

        return HeadData(code=code, headers=headers, error=error, error_msg=err_msg)

    def get_content(self, url, follow_redirect=False):
        # import pudb;pudb.set_trace()
        if(not isinstance(url, ParseResult)):
            url = urlparse(url)

        error = False
        err_msg = None

        creds = self._get_htauth_creds(url.netloc)

        try:
            resp = self._request.get(url.geturl(), allow_redirects=follow_redirect, verify=False, auth=creds)

            final_url = resp.url
            headers = resp.headers
            code = resp.status_code
            content = resp.text
        except Exception, e:
            final_url = None
            headers = None
            code = None
            content = None

            error = True
            err_msg = str(e)

        return ContentData(final_url=final_url,
                           headers=headers,
                           code=code,
                           content=content,
                           error=error,
                           error_msg=err_msg)

    def start_crawl(self):
        start_page = self.get_content(self._start_url, follow_redirect=True)

        if(start_page.error):
            raise CrawlerError("Could not get initial start page: %s" % start_page.error_msg)

        start_page_final_netloc = urlparse(start_page.final_url).netloc

        self._session.add_start_domain(start_page_final_netloc)
        self._session.add_start_domain(removeWWW(start_page_final_netloc))

        if 'content-type' in start_page.headers and is_content_type_text(start_page.headers['content-type']):
            page = start_page

            while True:
                if page and not page.error and ('content-type' in page.headers) and is_content_type_text(page.headers['content-type']):
                    page_netloc = urlparse(page.final_url).netloc

                    for i in self._url_parser.url_gen(page.content):
                        next_url = self._url_to_abs_url(i, page_netloc)

                        self._session.add_url(next_url)

                next_to_visit = self._session.next_url()

                if next_to_visit:
                    if self._do_proceed_traverse(next_to_visit):
                        page = self.get_content(next_to_visit)
                        status = page.code if not page.error else None
                        from_domain = True
                        self._session.set_restore_url(next_to_visit)
                    else:
                        from_domain = False
                        page = None
                        if self.do_head_ping:
                            head = self.head_ping(next_to_visit)
                            status = head.code if not head.error else None
                        else:
                            status = None

                    url_data = URLInfoData(url=next_to_visit, status=status, from_domain=from_domain)

                    yield url_data

                    self._session.add_visited_url(url_data.url)
                else:
                    break

        else:
            raise CrawlerContentError('The content-type of this page doesn\'t seem to be readable text')
