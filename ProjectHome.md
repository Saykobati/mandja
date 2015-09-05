# Mandja #

## Usage ##

```
usage: mandja-crawl [-h] [-a HTTPAUTH_CREDS] [-s SESSION_FILE] [-g GO_REGEX]
                    [-u VISIT_REGEX]
                    [-e {a-href,link-href,script-src,form-action,sick-match}]
                    [-o {url,status,from_main_domain}] [-f OUTPUT_FILTER]
                    url

A little recursive crawler. It is able to list all URLs it has visited. You
reuse the connection via Keep-Connection when crawling on the set domain and
use different connections for the head ping of URLs on different domains.

positional arguments:
  url                   URL to crawl

optional arguments:
  -h, --help            show this help message and exit
  -a HTTPAUTH_CREDS, --httpauth-creds HTTPAUTH_CREDS
                        HTTP authentication credentials passed as a json
                        string: -a '{"<netloc>": {"username": "<user>",
                        "password": "<password>"}}'
  -s SESSION_FILE, --session-file SESSION_FILE
                        If a session file is used - all the data from URL
                        processing is saved including the current state. If
                        the crawling is interrupted you can continue later
                        using the session file. When crawleing has finished,
                        this state is marked also. By using the file you can
                        filter/parse/extract data related to the crawled URL
                        offline.
  -g GO_REGEX, --go-regex GO_REGEX
                        Pre-visit regex filter to determine if an URL is
                        permitted to be crawled
  -u VISIT_REGEX, --visit-regex VISIT_REGEX
                        A regex which is used over extracted URLs to determine
                        if it has been visited. This way a 'visited' mask is
                        formed
  -e {a-href,link-href,script-src,form-action,sick-match}, --extract-option {a-href,link-href,script-src,form-action,sick-match}
                        These options present the type of extraction filter
                        used to determine which URLs should be extracted. This
                        is used on the crawling phase - if you miss an option
                        you would not visit the kind of URLs. The default is:
                        ['a-href']. The meaning of options is: 'a-href' -
                        visit URLs gathered from <a href=".."> tags, 'link-
                        href' - URLs from <link src="..">, 'form-action' -
                        URLs from <form action="..">, 'sick-match' - using a
                        sick general regex to finde anything looking like an
                        URL
  -o {url,status,from_main_domain}, --output-fields {url,status,from_main_domain}
                        This presents the information that is outputed on the
                        screen. Default is: ['url', 'status']

Copyright (C) 2011 MrGray
```

## Requires ##

  * Python 2.6 >
  * requests


## Description ##

> A little recursive crawler.
> It tries to visit every URL of the same domain and parse it for URLs.
> Mandja looks in css, js, txt's and everything which looks like plain text.
> You reuse the connection via Keep-Connection when crawling on the set domain and use
> different connections for the head ping of URLs on different domains.
> For now it just prints out the visited URLs with the status code.
> I plan to add more features in future.