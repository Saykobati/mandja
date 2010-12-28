#!/usr/bin/env python

import httplib2
import urllib2
from restkit import request
import urlparse

import os
import sys

from libmandja.cmdline import cmdlineParse
from libmandja.parser import getURLs

__default_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
                     'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; '\
                                   'Windows NT 6.0; SU 3.1; SLCC1; .NET '\
                                   'CLR 2.0.50727; .NET CLR 3.0.04506; '\
                                   '.NET CLR 1.1.4322; .NET CLR 3.5.21022)',\
                     'Accept-Language': 'en-us,en;q=0.5',\
                     'Accept-Encoding': 'gzip,deflate',\
                     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}

def headPing(url):
    if(not isinstance(url, urlparse.ParseResult)):
        url = urlparse.urlparse(url)
    
    conn = httplib2.Http()
    conn.follow_redirects = False
    (headers, body) = conn.request(url.geturl(), 'HEAD', None, None)
    
    return headers

def getContent(url):
    if(not isinstance(url, urlparse.ParseResult)):
        url = urlparse.urlparse(url)
    
    req = urllib2.Request(url.geturl(), None, __default_headers)
    resp = urllib2.urlopen(req)
    
    return resp

def getContent2(url):
    if(not isinstance(url, urlparse.ParseResult)):
        url = urlparse.urlparse(url)
    
    response = request(url.geturl(), headers = __default_headers)
    
    return response


def main():
    arguments = cmdlineParse()
    main_url = arguments.url
    
    
    #rsp = headPing(main_url)
    #print repr(rsp)
    
    #rsp = getContent(main_url)
    #print repr(rsp.info().headers)
    #print "\n"
    #print rsp.read()
    
    rsp2 = getContent2(main_url)
    all = getURLs(rsp2.body)
    for i in all:
        print i
    #print "\n\n".join(all)


if(__name__ == "__main__"):
    main()
