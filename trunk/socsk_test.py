#!/usr/bin/env python

from libmandja import socks
from libmandja import common

#res = common.isipaddr('255.122.3.1')
#print repr(res)

prx = socks.Proxy()
name = prx.getHostByName('abv.bg')

print name