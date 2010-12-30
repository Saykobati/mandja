#!/usr/bin/env python

from libmandja.cmdline import cmdlineParse
from libmandja.crawler import Crawl

def main():
    arguments = cmdlineParse()
    main_url = arguments.url
    
    cr_ob = Crawl(main_url)
    cr_ob.startCrawling()

if(__name__ == "__main__"):
    main()
