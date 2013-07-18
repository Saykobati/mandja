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


import re


_url_patterns = ['(?:(?:href|src)\=)(?P<quotes>"|\')(?P<urlString>[^\s]*?)(?P=quotes)',\
                  '(?:url\()(?P<urlString>[^\s]*?)(?:\))']

_text_content_type_patterns = ['text|javascript|css|html|xhtml|xml']


def getURLs(data):
    
    url_regex_chain =  [itr for itr in\
                                (re.finditer(ptr, data, re.MULTILINE | re.DOTALL | re.IGNORECASE)\
                                    for ptr in _url_patterns) ]
    all_urls = set()
    
    for i in url_regex_chain:
        for j in i:
            all_urls.add(j.group('urlString').strip())
    
    return all_urls


def parseHeaders(headers):
    headers_dict = {}
    h_lines = [i.strip() for i in re.split("\n",headers)]
    http_greet = h_lines.pop(0)
    status_regex = re.search("HTTP/[\d]?\.[\d]?[\s]+([\d]+)", http_greet)
    status = status_regex.group(1) if status_regex.group(1) else None
    
    headers_dict['status'] = status
    for l in h_lines:
        line = [q for q in re.split(":", l)]
        if(len(line) == 2):
            headers_dict[line[0].strip().lower()] = line[1].strip()
    
    return headers_dict


def extractHtmlEncoding(html):
    meta_tag_pattern = '\<meta[\s]+http\-equiv\=(?P<quotes1>"|\')Content\-Type(?P=quotes1)'\
                       '[\s]+content\=(?P<quotes2>"|\')(?P<contentString>.*)(?P=quotes2)'
    content_pattern = '(?:charset\=)([^\s]+)'
    
    for i in re.finditer(meta_tag_pattern, html, re.IGNORECASE):
        content = i.group('contentString')
        match_charset = re.search(content_pattern, content, re.IGNORECASE)
        if(match_charset.group(1)):
            return match_charset.group(1).lower()
    
    return None


def isContentTypeText(content_type_data):
    for txt_ptr in _text_content_type_patterns:
        if re.search(txt_ptr, content_type_data):
            return True
    return False