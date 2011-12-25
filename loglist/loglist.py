#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida Jabber Bot logs list for lighttpd                                  #
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

import os,time,sys,cgi,cgitb

html_head = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<title>%s</title>
<style type="text/css">
a, a:active, a:visited {text-decoration: none; color: #787878;}
a:hover, a:focus {text-decoration: underline; color: black;}
body {background-color: #e0e0e0;}
h2 {margin-bottom: 12px; font-family: consolas}
table {margin-left: 12px;}
th, td { font: 90%% monospace; text-align: left; font-family: consolas}
th { font-weight: bold; padding-right: 14px; padding-bottom: 3px; font-family: consolas}
td {padding-right: 14px;}
td.s, th.s {text-align: right;}
div.list { background-color: white; border-top: 1px solid #646464; border-bottom: 1px solid #646464; padding-top: 10px; padding-bottom: 14px;}
div.foot { font: 90%% monospace; color: #787878; padding-top: 4px;}
</style>
<link rel="shortcut icon" href="/icon.ico">
</head>
<body>

<div class="foot">
<table width="98%%" cellpadding="0" cellspacing="0" border="0">
<td valign="center"><h2><i>%s</i></h2></td>
<td valign="center" width="10%%" ><p align="right"><a href="/"><img src="/images/home.gif" title="Home" align="middle" alt="Home" border="0" /></a></p></td>
</table>
</div>

<div class="list">
<table summary="Directory Listing" cellpadding="0" cellspacing="0">
<thead><tr><th class="n">Name</th><th class="m">Last Modified</th><th class="s">Size</th><th class="t">Type</th></tr></thead>
<tbody>
<tr><td class="n">%s<a href="../"><b>..</b></a></td><td class="m">&nbsp;</td><td class="s">- &nbsp;</td><td class="t">directory</td></tr>
'''

html_end = '''
</tbody>
</table>
</div>
<div class="foot">
<p align="right"><a href="http://dsy.name"><img src="/images/long_logo.png" title="Disabler Production Lab." align="middle" alt="Disabler Production Lab." border="0" /></a>&nbsp;&nbsp;&nbsp;&nbsp;</p>
</div>
</body>
</html>
'''

#<br><p align="right">
#<font color="#0000aa">(c)&nbsp;2oo9-2o11&nbsp;Disabler&nbsp;Production&nbsp;Lab</font><font color="#ff0000">A</font><font color="#0000aa">ratory&nbsp;&nbsp;&nbsp;&nbsp;</font>
#</p>

mask = '<tr><td class="n">%s<a href="%s"><font color=black>%s</font></a></td><td class="m">%s</td><td class="s">%s</td><td class="t">%s</td></tr>'

mimetype = {'pdf':'application/pdf',
			'sig':'application/pgp-signature',
			'spl':'application/futuresplash',
			'class':'application/octet-stream',
			'ps':'application/postscript',
			'torrent':'application/x-bittorrent',
			'dvi':'application/x-dvi',
			'gz':'application/x-gzip',
			'pac':'application/x-ns-proxy-autoconfig',
			'swf':'application/x-shockwave-flash',
			'tar':'application/x-tgz',
			'tgz':'application/x-tgz',
			'tar':'application/x-tar',
			'zip':'application/zip',
			'mp3':'audio/mpeg',
			'm3u':'audio/x-mpegurl',
			'wma':'audio/x-ms-wma',
			'wax':'audio/x-ms-wax',
			'ogg':'application/ogg',
			'wav':'audio/x-wav',
			'gif':'image/gif',
			'jar':'application/x-java-archive',
			'jpg':'image/jpeg',
			'jpeg':'image/jpeg',
			'png':'image/png',
			'xbm':'image/x-xbitmap',
			'xpm':'image/x-xpixmap',
			'xwd':'image/x-xwindowdump',
			'css':'text/css',
			'html':'text/html',
			'htm':'text/html',
			'js':'text/javascript',
			'py':'text/python',
			'asc':'text/plain',
			'c':'text/plain',
			'cpp':'text/plain',
			'log':'text/plain',
			'conf':'text/plain',
			'text':'text/plain',
			'txt':'text/plain',
			'dtd':'text/xml',
			'xml':'text/xml',
			'mpeg':'video/mpeg',
			'mpg':'video/mpeg',
			'mov':'video/quicktime',
			'qt':'video/quicktime',
			'avi':'video/x-msvideo',
			'asf':'video/x-ms-asf',
			'asx':'video/x-ms-asf',
			'wmv':'video/x-ms-wmv',
			'bz2':'application/x-bzip',
			'tbz':'application/x-bzip-compressed-tar',
			'tar':'application/x-bzip-compressed-tar',
			'.':'application/octet-stream'}

#form = cgi.FieldStorage() 
#print form.getvalue()
#print sys.argv
#print cgi.FormContentDict()

#print wsgiref.util.request_uri('PATH_INFO')

img = '<img src="%s"/>'
img_folder = img % '/images/dirlist-folder.png'
img_file = img % '/images/dirlist-file.png'
img_back = img % '/images/dirlist-back.png'

dir_name = os.environ['REQUEST_URI'][:-1]
'''
log_dir = '.log'

log_file_name = time.strftime('%Y%m%d.txt',time.localtime())

log_time  = time.strftime('%H:%M:%S',time.localtime())
log_ip    = unicode(os.environ['REMOTE_ADDR'])
try: log_ref   = unicode(os.environ['HTTP_REFERER'])
except: log_ref   = 'Direct connect'
log_agent = unicode(os.environ['HTTP_USER_AGENT'])

lrec = '%s [%s] %s (%s -> %s)\n' % (log_time,log_ip,log_agent,log_ref,dir_name)

if not os.path.exists(log_dir): os.mkdir(log_dir)

fl = open('%s/%s' % (log_dir,log_file_name), 'a')
fl.write(lrec.encode('utf-8'))
fl.close()
'''
#for i in os.environ.keys():
#	print '%s - %s<br>' % (i,os.environ[i])

def error_handler(error):
	print error
	sys.exit()

HOST_DIR = '/var/www/html/'
if os.environ['DOCUMENT_ROOT'] != HOST_DIR: error_handler('Incorrect root!')

ALLOWED_DIRS = ['/syslogs','/chatlogs']
correct = False
for t in ALLOWED_DIRS:
	if dir_name.startswith(t):
		correct = True
		break
if not correct: error_handler('Incorrect path: %s' % dir_name)
	

dir_name2 = '%s' % dir_name[1:].capitalize()

dnn = dir_name2.replace('/',': ',1).replace('/',' - ',1)
dnnurl = '/'
cmp = '/'
for t in dir_name2.split('/')[:-1]:
	cmp += '%s/' % t.lower()
	dnnurl += '<a href="%s">%s</a>/' % (cmp,t)
dnnurl += dir_name2.split('/')[-1]
dnnurl = dnnurl[1:].replace('</a>/','</a>: ',1).replace('</a>/','</a> - ',1)

print html_head % (dnn,dnnurl,img_back)

content = os.listdir('../%s' % dir_name)
content.sort()
dirs,files = [],[]
for t in content:
	if os.path.isdir('../%s/%s' % (dir_name,t)): dirs.append(t)
	else: files.append(t)

for t in dirs+files:
	if not t.startswith('.') and t != 'index.py':
		tm = time.strftime('%H:%M:%S %d.%m\'%Y',time.localtime(os.path.getmtime('../%s/%s' % (dir_name,t))))
		if os.path.isdir('../%s/%s' % (dir_name,t)):
			timg = img_folder
			isd = 'directory'
			sz = '- &nbsp;'
			fn = '<b>%s</b>' % t
		else:
			timg = img_file
			tt = t.split('.')[-1]
			if mimetype.has_key(tt): isd = mimetype[tt]
			else: isd = mimetype['.']
			sz = os.path.getsize('../%s/%s' % (dir_name,t))
			fn = t
		print mask % (timg,t,fn,tm,sz,isd)
		

		
print html_end
