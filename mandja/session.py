#!/usr/bin/env python
#-*- coding: utf-8 -*-


__all__ = ["Session"]


class Session(object):
    def __init__(self, session_file=None, visit_regex=None):
        self.session_file = session_file
        self.visit_regex = visit_regex
        self._start_domains = set()
        self._last_visited = None

        self._url_pool = {}

    def _visit_strip_url(self, url):
        if(self.visit_regex):
            r = self.visit_regex.search(url)
            if(r):
                return r.group()
            else:
                return url
        else:
            return url

    @property
    def start_domains(self):
        return self._start_domains

    def add_start_domain(self, domain):
        self._start_domains.add(domain)

    def add_url(self, url):
        if(self._visit_strip_url(url) not in self._url_pool):
            self._url_pool[self._visit_strip_url(url)] = (url, 0)

    def next_url(self):
        for i in self._url_pool:
            if(self._url_pool[i][1] == 0):
                return self._url_pool[i][0]

    def add_visited_url(self, url):
        self._last_visited = url

        self._url_pool[self._visit_strip_url(url)] = (url, 1)
