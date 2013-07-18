#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Plamen Valov
# 
# This file is part of `mandja` program.
# `mandja` is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.
# 
# Mandja is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.


import re
import gzip
import StringIO

from urlparse import urlparse
from urlparse import ParseResult
import pycurl

from .common import removeWWW
from .parser import getURLs
from .parser import isContentTypeText
from .parser import parseHeaders
from .parser import extractHtmlEncoding

from .exception import mandjaCrawlerError
from .exception import mandjaCrawlerURLError
from .exception import mandjaCrawlerContentError


class Buffer:
    _data = None
    
    def __init__(self):
        self._data = ''
    
    def addContent(self, content):
        self._data += content
    
    def dump(self):
        return self._data
    
    def clearContent(self):
        self._data = None


class Crawler(object):
    _default_user_agent = ('Mozilla/4.0 (compatible; MSIE 7.0; '
                           'Windows NT 6.0; SU 3.1; SLCC1; .NET '
                           'CLR 2.0.50727; .NET CLR 3.0.04506; '
                           '.NET CLR 1.1.4322; .NET CLR 3.5.21022)')
    _default_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'User-Agent': _default_user_agent,
                        'Accept-Language': 'en-us,en;q=0.5',
                        'Accept-Encoding': 'gzip,deflate',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}
    _proxy_keep_alive_headers = {'Keep-Alive': '115',
                                 'Proxy-Connection': 'keep-alive'}
    _keep_alive_headers = {'Keep-Alive': '115',
                           'Connection': 'keep-alive'}
    
    _curl_object = None
    _head_curl_object = None
    
    _text_content_type = []
    _start_url = None
    _start_scheme = None
    _start_netlocs = set()
    _checked_url_pool = set()
    _not_checked_url_pool = set()
    _http_proxy = 'http://127.0.0.1:8118'
    
    _option_use_proxy = False
    
    def __init__(self, start_url, options = {}):
        if(not isinstance(start_url, ParseResult)):
            start_url = urlparse(start_url)
            if(not start_url.scheme):
                raise mandjaCrawlerURLError
            elif(not start_url.netloc):
                raise mandjaCrawlerURLError
        
        self._curl_object = pycurl.Curl()
        self._head_curl_object = pycurl.Curl()
        self._start_url = start_url.geturl()
        self._start_scheme = start_url.scheme
        self._start_netlocs.add(start_url.netloc)
        self._start_netlocs.add(removeWWW(start_url.netloc))
    
    def _prepareURL(self, url_str, default_netloc):
        url = urlparse(url_str, self._start_scheme)
        
        if not url.netloc:
            netloc = default_netloc
        else:
            netloc = url.netloc
        
        return ParseResult(url.scheme, netloc, url.path, url.params, url.query, url.fragment).geturl()
    
    def _proceedTraverse(self, url_str):
        url = urlparse(url_str, self._start_scheme)
        if url.netloc in self._start_netlocs:
            return True
        else:
            return False
    
    def headPing(self, url):
        if(not isinstance(url, ParseResult)):
            url = urlparse(url)
        
        curlObj = self._head_curl_object
        error = False
        headers_buf = Buffer()
        
        try:
            curlObj.setopt(curlObj.URL, url.geturl())
            curlObj.setopt(curlObj.NOBODY, True)
            curlObj.setopt(curlObj.HEADERFUNCTION, headers_buf.addContent)
            curlObj.setopt(curlObj.FOLLOWLOCATION, 0)
            if(self._option_use_proxy):
                curlObj.setopt(curlObj.PROXY, self._http_proxy)
                curlObj.setopt(curlObj.HTTPHEADER, [k+': '+v for k,v in
                                                        dict(self._default_headers.items()).items()])
            else:
                curlObj.setopt(curlObj.HTTPHEADER, [k+': '+v for k,v in
                                                        dict(self._default_headers.items()).items()])
            curlObj.perform()
            
            headers = parseHeaders(headers_buf.dump())
            code = int(curlObj.getinfo(pycurl.HTTP_CODE))
        except:
            code = None
            headers = None
            error = True
        
        return {'code': code, 'headers': headers, 'error': error}
    
    def getContent(self, url, follow_redirect = False):
        if(not isinstance(url, ParseResult)):
            url = urlparse(url)
        
        curlObj = self._curl_object
        error = False
        content_buf = Buffer()
        headers_buf = Buffer()
        
        try:
            curlObj.setopt(curlObj.URL, url.geturl())
            curlObj.setopt(curlObj.WRITEFUNCTION, content_buf.addContent)
            curlObj.setopt(curlObj.HEADERFUNCTION, headers_buf.addContent)
            if(follow_redirect):
                curlObj.setopt(curlObj.FOLLOWLOCATION, 1)
            else:
                curlObj.setopt(curlObj.FOLLOWLOCATION, 0)
            if(self._option_use_proxy):
                curlObj.setopt(curlObj.PROXY, self._http_proxy)
                curlObj.setopt(curlObj.HTTPHEADER, [k+': '+v for k,v in
                                                        dict(self._default_headers.items() +
                                                        self._proxy_keep_alive_headers.items()).items()])
            else:
                curlObj.setopt(curlObj.HTTPHEADER, [k+': '+v for k,v in
                                                        dict(self._default_headers.items() +
                                                        self._keep_alive_headers.items()).items()])
            curlObj.perform()
            
            final_url = curlObj.getinfo(pycurl.EFFECTIVE_URL)
            headers = parseHeaders(headers_buf.dump())
            code = int(curlObj.getinfo(pycurl.HTTP_CODE))
            content = content_buf.dump()
            
            if('content-encoding' in headers and headers['content-encoding'] == 'gzip'):
                compressed_stream = StringIO.StringIO(content)
                gzipper = gzip.GzipFile(fileobj = compressed_stream)
                content = gzipper.read()
            
            encoding = extractHtmlEncoding(content)
            
        except:
            content = None
            final_url = None
            headers = None
            encoding = None
            error = True
            code = None
        
        headers_buf.clearContent()
        content_buf.clearContent()
        
        return {'code': code, 'final_url': final_url, 'headers': headers, 'error': error, 'content': content, 'encoding': encoding}
    
    def startCrawl(self):
        start_page = self.getContent(self._start_url, True)
        
        start_page_final_netloc = urlparse(start_page['final_url']).netloc
        
        self._start_netlocs.add(start_page_final_netloc)
        self._start_netlocs.add(removeWWW(start_page_final_netloc))
        
        if 'content-type' in start_page['headers'] and isContentTypeText(start_page['headers']['content-type']):
            page = start_page
            
            while True:
                if page and not page['error'] and ('content-type' in page['headers']) and isContentTypeText(page['headers']['content-type']):
                    page_urls = getURLs(page['content'])
                    page_netloc = urlparse(page['final_url']).netloc
                    for i in page_urls:
                        next_url = self._prepareURL(i, page_netloc)
                        if not next_url in self._checked_url_pool:
                            self._not_checked_url_pool.add( next_url )
                if self._not_checked_url_pool:
                    next_to_visit = self._not_checked_url_pool.pop()
                    failed = False
                    if self._proceedTraverse(next_to_visit):
                        page = self.getContent(next_to_visit)
                        failed = True if page['error'] else False
                        status = page['code'] if not failed else 'Invalid URL'
                    else:
                        page = None
                        head = self.headPing(next_to_visit)
                        status = head['code'] if not head['error'] else 'Invalid URL'
                    print next_to_visit + '    ' + str(status)
                    self._checked_url_pool.add(next_to_visit)
                else:
                    break
            
        else:
            raise mandjaCrawlerContentError('The content-type of this page doesn\'t seem to be readable text')