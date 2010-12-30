#!/usr/bin/env python

from libmandja.cmdline import cmdlineParse
from libmandja.crawler import Crawl

def main():
    arguments = cmdlineParse()
    main_url = arguments.url
    
    cr_ob = Crawl(main_url)
    cr_ob.startCrawling()
    
    #cr = Crawl()
    #print repr(Crawl.headPing(main_url))
    
    #v1 = 'binary/html'
    #v2 = 'binary/application'
    #print repr(isContentTypeText(v1))
    #print repr(isContentTypeText(v2))


if(__name__ == "__main__"):
    main()
