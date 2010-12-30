import re

__url_patterns = ['(?:(?:href|src)\=)(?P<quotes>"|\')(?P<urlString>[^\s]*?)(?P=quotes)',\
                  '(?:url\()(?P<urlString>[^\s]*?)(?:\))']

__text_content_type_patterns = ['text|javascript|css|html|xhtml|xml']

def getURLs(data):
    
    url_regex_chain =  [itr for itr in\
                                (re.finditer(ptr, data, re.MULTILINE | re.DOTALL | re.IGNORECASE)\
                                    for ptr in __url_patterns) ]
    all_urls = set()
    
    for i in url_regex_chain:
        for j in i:
            all_urls.add(j.group('urlString').strip())
    
    return all_urls

def isContentTypeText(content_type_data):
    for txt_ptr in __text_content_type_patterns:
        if re.search(txt_ptr, content_type_data):
            return True
    return False