from urlparse import urlparse
from urlparse import ParseResult
import argparse

def __argparseUrlCheck(url):
    
    msg_scheme_error = "Missing scheme in '{url}'".format(url = url)
    msg_netloc_error = "Missing network location in {url}".format(url = url)
    
    url = urlparse(url)
    
    if(not url.scheme):
        raise argparse.ArgumentTypeError(msg_scheme_error)
    elif(not url.netloc):
        raise argparse.ArgumentTypeError(msg_netloc_error)
    
    return url

def cmdlineParse():
    program_description = 'A little recursive python crawler. '\
                          'It is able to list all URLs it has visited. '\
                          'There are options to crawl anonimously via proxy, '\
                          'or to reuse connections when you traversing a specified '\
                          'domain.'
    program_epilog = 'Author: Mr.Gray'
    url_help = 'The URL you want mandja to start with'
    
    parser = argparse.ArgumentParser(description = program_description, epilog = program_epilog)
    
    parser.add_argument("url", type = __argparseUrlCheck, help = url_help)
    
    arguments = parser.parse_args()
    
    return arguments