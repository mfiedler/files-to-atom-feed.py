#!/usr/bin/env python
'''
Create an Atom feed from a list of files.


Copyright 2013 by Michael Fiedler <michael.fiedler87@gmx.de>

Based on an answer by user 'codeape'[1] to a question by user 'Recursion'[2] on
stackoverflow.com, see [3].

  [1] http://stackoverflow.com/users/106534/recursion
  [2] http://stackoverflow.com/users/3571/codeape
  [3] http://stackoverflow.com/questions/2099666/tips-on-creating-rss-xml-easily-in-python

This file may be distributed and/or modified under the terms of the Creative
Commons Attribution-ShareAlike 3.0 Unported license[4].

  [4] http://creativecommons.org/licenses/by-sa/3.0/
'''

import jinja2
import os.path
import sys
import time

if len(sys.argv) < 4:
    print >> sys.stderr, 'Usage: %s <base URL> <feed title> <file>...' % sys.argv[0]
    sys.exit(2)

URLBase = sys.argv[1]
feedTitle = sys.argv[2]
files = sys.argv[3:]

feedItems = [(os.path.basename(x),
            URLBase + x,
            time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.path.getmtime(x))),
            feedTitle)
        for x in files]

templateKey = 'template'
templateValue = r'''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">''' + \
    '    <title>%s</title>' % feedTitle + \
r'''    {%for item in items %}
    <entry>
        <title>{{item[0]}}</title>
        <link href="{{item[1]}}"/>
        <content type="html">{{item[0]}}</content>
        <updated>{{item[2]}}</updated>
    </entry>
    {%endfor%}
</feed>
'''
templatesDict = {templateKey: templateValue}


env = jinja2.Environment(loader=jinja2.DictLoader(templatesDict))
print env.get_template(templateKey).render(items=feedItems)
