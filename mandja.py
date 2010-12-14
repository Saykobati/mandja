#!/usr/bin/env python

import httplib
import urllib2
from restkit import request
import urlparse

import os
import sys
import re
import argparse


def argparseUrlCheck(url):
    
    msg_scheme_error = "Missing scheme in '{url}'".format(url = url)
    msg_netloc_error = "Missing network location in {url}".format(url = url)
    
    url = urlparse.urlparse(url)
    
    if(not url.scheme):
        raise argparse.ArgumentTypeError(msg_scheme_error)
    elif(not url.netloc):
        raise argparse.ArgumentTypeError(msg_netloc_error)
    
    return url


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

def getURIsFromData(data):
    pass


def main():
    program_description = "Just a begininig"
    program_epilog = "Author: Mr.Gray"
    url_help = "The URL you want to parse"
    
    parser = argparse.ArgumentParser(description = program_description, epilog = program_epilog)
    
    parser.add_argument("url", type = argparseUrlCheck, help = url_help)
    
    arguments = parser.parse_args()
    
    main_url = arguments.url
    
    a = "\x05\x00"
    s = "Bizarre socks5 response: {resp}".format(resp = repr(a))
    print s
    
    
    #rsp = headPing(main_url)
    #print rsp.status, rsp.reason
    
    #rsp = getUrl(main_url)
    #print rsp.body


if(__name__ == "__main__"):
    main()
