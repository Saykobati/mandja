#!/usr/bin/env python
#-*- coding: utf-8 -*-


__all__ = ["Session"]


import sys
import re
import os
import json


class Session(object):
    def __init__(self, session_file=None, visit_regex=None):
        self.session_file = session_file
        self._create_session(session_file=session_file, visit_regex=visit_regex)

    def _init(self, **kw):
        self.__setattr__("visit_regex_pattern", kw.get("visit_regex", "^.+$"))
        self.__setattr__("visit_regex", re.compile(self.visit_regex_pattern))

        self.__setattr__("start_domains", kw.get("start_domains", []))
        self.__setattr__("last_visited", kw.get("last_visited", None))
        self.__setattr__("url_pool", kw.get("url_pool", {}))

    def __del__(self):
        self._store_session()

    def _create_session(self, **kw):
        if kw.get("session_file", None) and os.path.isfile(kw["session_file"]):
            try:
                session_dict = json.load(open(self.session_file, 'r'))
                self._init(**session_dict)
            except Exception, e:
                print >> sys.stderr, "Warning: Discarding session file %s: %s" % (self.session_file, str(e))
                visit_regex = kw.get("visit_regex", "^.+$")
                self._init(visit_regex=visit_regex)
        else:
            visit_regex = kw.get("visit_regex", "^.+$")
            self._init(visit_regex=visit_regex)

    def _store_session(self):
        if(self.session_file):
            try:
                session_dict = {}
                session_dict["visit_regex"] = self.visit_regex_pattern
                session_dict["last_visited"] = self.last_visited
                session_dict["start_domains"] = self.start_domains
                session_dict["url_pool"] = self.url_pool

                json.dump(session_dict, open(self.session_file, 'w'))
            except Exception, e:
                print >> sys.stderr, "Warning: Could not write to session file - %s" % str(e)

    def _visit_strip_url(self, url):
        if(self.visit_regex):
            r = self.visit_regex.search(url)
            if(r):
                return r.group()
            else:
                return url
        else:
            return url

    def add_start_domain(self, domain):
        if(domain not in self.start_domains):
            self.start_domains.append(domain)

    def add_url(self, url):
        if(self._visit_strip_url(url) not in self.url_pool):
            self.url_pool[self._visit_strip_url(url)] = [url, 0]

    def next_url(self):
        for i in self.url_pool:
            if(self.url_pool[i][1] == 0):
                return self.url_pool[i][0]

    def add_visited_url(self, url):
        self.url_pool[self._visit_strip_url(url)] = [url, 1]

    def set_restore_url(self, url):
        self.last_visited = url

    def get_restore_url(self):
        return self.last_visited
