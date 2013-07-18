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

import os

from urlparse import urlparse
from urlparse import ParseResult
import argparse


class CmdlineParser(object):
    _scheme_error = "Missing scheme in '{url}'"
    _netloc_error = "Missing network location in {url}"
    _not_directory_error = "The entered directory doesn't exists: '{dir}'"
    _no_write_priv_error = "You don't have write permissions: '{dir}'"
    
    @classmethod
    def _argparseUrlCheck(cls, url):
        url = urlparse(url)
        if(not url.scheme):
            raise argparse.ArgumentTypeError(cls._scheme_error.format(url = url))
        elif(not url.netloc):
            raise argparse.ArgumentTypeError(cls._netloc_error.format(url = url))
        
        return url
    
    @classmethod
    def _argparseDirectoryCheck(cls, directory):
        if(not os.path.isdir(directory)):
            raise argparse.ArgumentTypeError(cls._not_directory_error.format(dir = directory))
        
        if(not os.access(directory, os.W_OK | os.X_OK)):
            raise argparse.ArgumentTypeError(cls._no_write_priv_error.format(dir = directory))
        
        return directory