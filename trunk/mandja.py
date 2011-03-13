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


import argparse

from libmandja.cmdline import CmdlineParser
from libmandja.crawler import Crawler


class MandjaCmdlineParser(CmdlineParser):
    _program_description = ('A little recursive crawler. '
                            'It is able to list all URLs it has visited. '
                            'You reuse the connection via Keep-Connection when'
                            'crawling on the set domain and use different connections'
                            'for the head ping of URLs on different domains.')
    _program_epilog = 'Copyright (C) 2011 Plamen Valov'
    
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
    
    cr_ob = Crawler(main_url)
    cr_ob.startCrawl()


if(__name__ == "__main__"):
    main()
