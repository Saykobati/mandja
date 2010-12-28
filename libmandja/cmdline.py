import urlparse
import argparse

def _argparseUrlCheck(url):
    
    msg_scheme_error = "Missing scheme in '{url}'".format(url = url)
    msg_netloc_error = "Missing network location in {url}".format(url = url)
    
    url = urlparse.urlparse(url)
    
    if(not url.scheme):
        raise argparse.ArgumentTypeError(msg_scheme_error)
    elif(not url.netloc):
        raise argparse.ArgumentTypeError(msg_netloc_error)
    
    return url

def cmdlineParse():
    program_description = "Just a begininig"
    program_epilog = "Author: Mr.Gray"
    url_help = "The URL you want to parse"
    
    parser = argparse.ArgumentParser(description = program_description, epilog = program_epilog)
    
    parser.add_argument("url", type = _argparseUrlCheck, help = url_help)
    
    arguments = parser.parse_args()
    
    return arguments