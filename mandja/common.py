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
import hashlib


def isInt(value):
    result = True
    try:
        num = int(value)
    except (ValueError, TypeError):
        result = False
        
    return result


def isIp4Addr(ip_addr):
    ip_addr_pattern = (r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
                      r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
                      r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
                      r"\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    
    if not isinstance(ip_addr, str):
        return False
    
    if re.match(ip_addr_pattern, ip_addr):
        return True
    else:
        return False


def removeWWW(data):
    return re.sub('^([\s]*?)www\.', '', data)


def md5bin(data):
    return hashlib.md5().update(data).digest()


def md5str(data):
    return hashlib.md5().update(data).hexdigest()