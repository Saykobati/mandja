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


class MandjaCmdlineParser(CmdlineParser):
    _program_description = ('A little recursive python crawler. '
                            'It is able to list all URLs it has visited. '
                            'There are options to crawl anonimously via proxy, '
                            'or to reuse connections when you traversing a specified '
                            'domain.')
    _program_epilog = 'Author: mrgray'
    
    _url_help = 'The URL you want mandja to start with'
    
    _arguments = None
    
    def __new__(cls):
        if(cls._arguments is None):
            parser = argparse.ArgumentParser(description = cls._program_description, epilog = cls._program_epilog)
            parser.add_argument("url", type = cls._argparseUrlCheck, help = cls._url_help)
            cls._arguments = parser.parse_args()
            
            return cls._arguments
        else:
            return cls._arguments
