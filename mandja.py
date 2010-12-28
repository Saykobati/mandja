#!/usr/bin/env python

import httplib
import urllib2
from restkit import request
import urlparse

import os
import sys
import re

from libmandja.cmdline import cmdlineParse

def headPing(url):
    if(not isinstance(url, urlparse.ParseResult)):
        url = urlparse.urlparse(url)
    
    conn = httplib.HTTPConnection(url.netloc)
    conn.request("HEAD",url.path)
    response = conn.getresponse()
    
    return response

def getUrl(url):
    if(not isinstance(url, urlparse.ParseResult)):
        url = urlparse.urlparse(url)
    
    response = request(url.geturl())
    
    return response

def parseForURLs(data):
    pass


def main():
    arguments = cmdlineParse()
    main_url = arguments.url
    
    
    #rsp = headPing(main_url)
    #print rsp.status, rsp.reason
    
    rsp = getUrl(main_url)
    print rsp.body


if(__name__ == "__main__"):
    main()
