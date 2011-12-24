#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2011 diSabler <dsy@dsy.name>                               #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

import urllib2,re
import time,math,sys,cgi,cgitb,socket,chardet

html_head = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href=".css/isida.css" rel="stylesheet" type="text/css" />
<link rel="shortcut icon" href="/icon.ico">
<title>Site feed search</title></head>
<body>
<div class="main"><div class="top"><div class="heart">
<a href="http://isida-bot.com">http://isida-bot.com</a></div>
<div class="conference">Site feed search</div></div><div class="container">
<p><span class="paste">'''

html_end = '''
</span></p></div></div><br>
<p align="right"><font color="#0000aa">(c)&nbsp;2oo9-2o11&nbsp;Disabler&nbsp;Production&nbsp;Lab</font><font color="#ff0000">A</font><font color="#0000aa">ratory&nbsp;&nbsp;&nbsp;&nbsp;</font>
</p></body></html>
'''

CONFIG = {'rss_get_timeout':15,
		  'user_agent':'Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4',
		  'size_overflow':4096}

def GT(var): return CONFIG[var] 

def get_opener(page_name, parameters=None):
	socket.setdefaulttimeout(GT('rss_get_timeout'))
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	opener.addheaders = [('User-agent', GT('user_agent'))]
	if parameters: page_name += urllib.urlencode(parameters)
	try: data, result = opener.open(page_name), True
	except Exception, SM:
		try: SM = str(SM)
		except: SM = unicode(SM)
		data, result = 'Error! %s' % SM.replace('>','').replace('<','').capitalize(), False
	return data, result

def load_page(page_name, parameters=None):
	data, result = get_opener(page_name, parameters)
	if result: return data.read(GT('size_overflow'))
	else: return data

def smart_encode(text,enc):
	tx,splitter = '','|'
	while splitter in text: splitter += '|'
	ttext = text.replace('</','<%s/' % splitter).split(splitter)
	for tmp in ttext:
		try: tx += unicode(tmp,enc)
		except: pass
	return tx
	
def html_encode(body):
	encidx = re.findall('encoding=["\'&]*(.*?)["\'& ]{1}',body[:1024])
	if encidx: enc = encidx[0]
	else:
		encidx = re.findall('charset=["\'&]*(.*?)["\'& ]{1}',body[:1024])
		if encidx: enc = encidx[0]
		else: enc = chardet.detect(body)['encoding']
	if body == None: body = ''
	if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
	if enc == 'ISO-8859-2':
		tx,splitter = '','|'
		while splitter in body: splitter += '|'
		tbody = body.replace('</','<'+splitter+'/').split(splitter)
		cntr = 0
		for tmp in tbody:
			try:
				enc = chardet.detect(tmp)['encoding']
				if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
				tx += unicode(tmp,enc)
			except:
				ttext = ''
				for tmp2 in tmp:
					if (tmp2<='~'): ttext+=tmp2
					else: ttext+='?'
				tx += ttext
			cntr += 1
		return tx
	else:
		try: return smart_encode(body,enc)
		except: return 'Encoding error!'

	
# ------------ Let's begin -----------
	
form = cgi.FieldStorage() 
url = form.getvalue('url')
if not url: url = ''
fk = form.keys()
if 'url' in fk and len(fk) > 1:
	fk.remove('url')
	url = '%s&%s' % (url,'&'.join(['%s=%s' % (t,form.getvalue(t)) for t in fk]))

print html_head

print '<form name="myform" method="post" class="paste" action="search_feed.py"><br>'
print '&nbsp;URL: <input type="text" name="url" value="%s" size=100 maxlength="256"/> ' % url
print '<input type="submit" value=" Get feed links "/><td>'
print '</form><br/>'
print '<p><span class="paste">'

if url:
	if url.startswith('http://'): url = url.replace('http://','',1)
	#print '<a href="http://%s">http://%s</a><br>' % (url,url)
	body = html_encode(load_page('http://%s' % url))
	if body.startswith('Error!') or body == 'Encoding error!': print body
	else:
		lnk = re.findall('<link.*?rel="alternate".*?title="(.*?)".*?href="(.*?)"',body,re.S+re.I+re.U)
		if lnk:
			print 'Found feed(s):<br>'
			print '<br>\n'.join(['%s - <a href="%s" title="%s">%s</a>' % tuple(list(t)+list(t)) for t in lnk])
		else: print 'Feed at %s not found!' % url
print '</span></p>'
print '<br>'
print html_end