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


__all__ = [
    "extract_html_encoding",
    "is_content_type_text",
    "UrlParser"
]


import re


def extract_html_encoding(html):
    meta_tag_pattern = '\<meta[\s]+http\-equiv\=(?P<quotes1>"|\')Content\-Type(?P=quotes1)'\
                       '[\s]+content\=(?P<quotes2>"|\')(?P<contentString>.*)(?P=quotes2)'
    content_pattern = '(?:charset\=)([^\s]+)'

    for i in re.finditer(meta_tag_pattern, html, re.IGNORECASE):
        content = i.group('contentString')
        match_charset = re.search(content_pattern, content, re.IGNORECASE)
        if(match_charset.group(1)):
            return match_charset.group(1).lower()

    return None


def is_content_type_text(content_type_data):
    text_content_type_patterns = ['text|javascript|css|html|xhtml|xml']

    for txt_ptr in text_content_type_patterns:
        if re.search(txt_ptr, content_type_data):
            return True

    return False


class UrlParser(object):
    patterns = {"a-href": re.compile(u'\<[\s]*a.*[\s]+href\=(?P<quotes>"|\')(?P<url_string>[^\s]*?)(?P=quotes)'),
                "link-href": re.compile(u'\<[\s]*link.*[\s]+href\=(?P<quotes>"|\')(?P<url_string>[^\s]*?)(?P=quotes)'),
                "script-src": re.compile(u'\<[\s]*script.*[\s]+src\=(?P<quotes>"|\')(?P<url_string>[^\s]*?)(?P=quotes)'),
                "img-src": re.compile(u'\<[\s]*img.*[\s]+src\=(?P<quotes>"|\')(?P<url_string>[^\s]*?)(?P=quotes)'),
                "form-action": re.compile(u'\<[\s]*form.*[\s]+action\=(?P<quotes>"|\')(?P<url_string>[^\s]*?)(?P=quotes)'),
                "css-url": re.compile(u'url\([\s"\']*(?P<url_string>[^\s"\']*)'),
                "sick-match": re.compile(u'(?P<url_string>http[^\s"\']*)'),
                }

    def __init__(self, extract_options):
        self.extract_options = extract_options

    def url_gen(self, data):
        parsed_urls = []
        for i in self.extract_options:
            if(i in self.patterns):
                for urlrex in self.patterns[i].finditer(data, re.MULTILINE | re.DOTALL | re.IGNORECASE):
                    if(urlrex):
                        url = urlrex.group('url_string')
                        if(url not in parsed_urls):
                            yield url
                            parsed_urls.append(url)
