#!/usr/bin/env python

import argparse

from libmandja.cmdline import CmdlineParser
from libmandja.crawler import Crawl

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

def main():
    arguments = MandjaCmdlineParser()
    main_url = arguments.url
    
    cr_ob = Crawl(main_url)
    cr_ob.startCrawling()

if(__name__ == "__main__"):
    main()
