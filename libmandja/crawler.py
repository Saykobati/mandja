import socket
import httplib2
import urllib2
from restkit import request

from urlparse import urlparse
from urlparse import ParseResult

from libmandja.exception import mandjaCrawlerError
from libmandja.exception import mandjaCrawlerURLError
from libmandja.exception import mandjaCrawlerContentError

from libmandja.common import md5bin
from libmandja.common import removeWWW

from libmandja.parser import getURLs
from libmandja.parser import isContentTypeText

class URLEntity(object):
    __slots__ = ('url', 'hash', 'status')
    
    def __init__(self, url, hash_string = None, status = None):
        self.url = url
        self.hash = hash_string
        self.status = status

class Crawl(object):
    __default_user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; '\
                           'Windows NT 6.0; SU 3.1; SLCC1; .NET '\
                           'CLR 2.0.50727; .NET CLR 3.0.04506; '\
                           '.NET CLR 1.1.4322; .NET CLR 3.5.21022)'
    
    __default_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
                         'User-Agent': __default_user_agent,\
                         'Accept-Language': 'en-us,en;q=0.5',\
                         'Accept-Encoding': 'gzip,deflate',\
                         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}
    
    __text_content_type = []
    
    __start_url = None
    
    __start_scheme = None
    
    __start_netlocs = set()
    
    __checked_url_pool = set()
    __not_checked_url_pool = set()
    
    @classmethod
    def headPing(cls, url):
        if(not isinstance(url, ParseResult)):
            url = urlparse(url)
        
        conn = httplib2.Http()
        conn.follow_redirects = False
        (headers, body) = conn.request(url.geturl(), 'HEAD', None, cls.__default_headers)
        
        return headers
    
    @classmethod
    def getContent(cls, url, follow_redirect = False):
        if(not isinstance(url, ParseResult)):
            url = urlparse(url)
        
        response = request(url.geturl(), headers = cls.__default_headers)
        response = request(url.geturl(), headers = cls.__default_headers, follow_redirect = follow_redirect)
        
        return response
    
    def __init__(self, start_url):
        if(not isinstance(start_url, ParseResult)):
            start_url = urlparse(start_url)
            if(not start_url.scheme):
                raise mandjaCrawlerURLError
            elif(not start_url.netloc):
                raise mandjaCrawlerURLError
        
        self.__start_url = start_url.geturl()
        
        self.__start_scheme = start_url.scheme
        
        self.__start_netlocs.add(start_url.netloc)
        self.__start_netlocs.add(removeWWW(start_url.netloc))
    
    def __prepareURL(self, url_str, default_netloc):
        url = urlparse(url_str, self.__start_scheme)
        
        if not url.netloc:
            netloc = default_netloc
        else:
            netloc = url.netloc
        
        return ParseResult(url.scheme, netloc, url.path, url.params, url.query, url.fragment).geturl()
    
    def __proceedTraverse(self, url_str):
        url = urlparse(url_str, self.__start_scheme)
        if url.netloc in self.__start_netlocs:
            return True
        else:
            return False
    
    def startCrawling(self):
        start_page = self.getContent(self.__start_url, True)
        
        start_page_final_netloc = urlparse(start_page.final_url).netloc
        
        self.__start_netlocs.add(start_page_final_netloc)
        self.__start_netlocs.add(removeWWW(start_page_final_netloc))
        
        if 'content-type' in start_page.headers and isContentTypeText(start_page.headers['content-type']):
            page = start_page
            
            while True:
                if page and 'content-type' in page.headers and isContentTypeText(page.headers['content-type']):
                    page_urls = getURLs(page.body)
                    page_netloc = urlparse(page.final_url).netloc
                    for i in page_urls:
                        next_url = self.__prepareURL(i, page_netloc)
                        if not next_url in self.__checked_url_pool:
                            self.__not_checked_url_pool.add( next_url )
                
                if self.__not_checked_url_pool:
                    next_to_visit = self.__not_checked_url_pool.pop()
                    failed = False
                    if self.__proceedTraverse(next_to_visit):
                        try:
                            page = self.getContent(next_to_visit)
                        except:
                            page = None
                            failed = True
                        status = page.status_int if not failed else 'Invalid URL'
                    else:
                        page = None
                        try:
                            head = self.headPing(next_to_visit)
                        except:
                            failed = True
                        status = head.status if not failed else 'Invalid URL'
                    
                    print next_to_visit + '    ' + str(status)
                    
                    self.__checked_url_pool.add(next_to_visit)
                else:
                    break
            
        else:
            raise mandjaCrawlerContentError('The content-type of this page doesn\'t seem to be readable text')
        
        
        