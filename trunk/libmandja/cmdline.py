from urlparse import urlparse
from urlparse import ParseResult
import argparse


class CmdlineParser(object):
    _scheme_error = "Missing scheme in '{url}'"
    _netloc_error = "Missing network location in {url}"
    
    @classmethod
    def _argparseUrlCheck(cls, url):
        url = urlparse(url)
        if(not url.scheme):
            raise argparse.ArgumentTypeError(cls._scheme_error.format(url = url))
        elif(not url.netloc):
            raise argparse.ArgumentTypeError(cls._netloc_error.format(url = url))
        
        return url