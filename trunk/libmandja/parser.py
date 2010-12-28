import re

__url_patterns = ['(?:(?:href|src)\=)(?P<quotes>"|\')(?P<urlString>[^\s]*?)(?P=quotes)',\
                  '(?:url\()(?P<urlString>[^\s]*?)(?:\))']

def getURLs(data):
    
    url_regex_chain =  [itr for itr in\
                                (re.finditer(ptr, data, re.MULTILINE | re.DOTALL | re.IGNORECASE)\
                                    for ptr in __url_patterns) ]
    all_urls = set()
    
    for i in url_regex_chain:
        for j in i:
            all_urls.add(j.group('urlString').strip())
    
    return all_urls