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

import time,math,sys,cgi,cgitb 

CYCLE_P = 23
CYCLE_E = 28
CYCLE_I = 33

X_SIZE = 128
Y_SIZE = 24

FROM = -X_SIZE/2
TO = X_SIZE/2

SPACE = ' '
X_LINE = '-'
Y_LINE = '|'

html_head = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href=".css/isida.css" rel="stylesheet" type="text/css" />
<title>Biorhytm calculator</title></head>
<body>
<div class="main"><div class="top"><div class="heart">
<a href="http://isida-bot.com">http://isida-bot.com</a></div>
<div class="conference">Biorhytm calculator</div></div><div class="container">
<p><span class="paste">'''
html_end = '''
</span></p></div></div><br>
<p align="right"><font color="#0000aa">(c)&nbsp;2oo9-2o11&nbsp;Disabler&nbsp;Production&nbsp;Lab</font><font color="#ff0000">A</font><font color="#0000aa">ratory&nbsp;&nbsp;&nbsp;&nbsp;</font>
</p></body></html>
'''

def timeadd(t): return '%02d.%02d.%02d' % (t[2],t[1],t[0])

def ins(t,a,p,m):
	p = int(math.sin(2*math.pi / float(p) * (a % p))*Y_SIZE/2) + int(Y_SIZE/2)
	return '%s%s%s' % (t[:p],m,t[p+1:])

# ------------ Let's begin -----------
	
form = cgi.FieldStorage() 
v1 = form.getvalue('bday')
v2 = form.getvalue('ctime')

BDAY = [18,6,1980]
if v1:
	try: BDAY = [int(t) for t in v1.split('.',2)]
	except: pass
BDAY = [BDAY[2],BDAY[1],BDAY[0],0,0,0,0,0,0]

lt = time.localtime()
CALC_TIME = [lt[2],lt[1],lt[0]]
if v2:
	try: CALC_TIME = [int(t) for t in v2.split('.',2)]
	except: pass
CALC_TIME = [CALC_TIME[2],CALC_TIME[1],CALC_TIME[0],0,0,0,0,0,0]


age_in_days = int(((time.mktime(CALC_TIME)-time.mktime(BDAY))/3600)/24)

	
print html_head

print 'Age is %s day(s)<br>' % age_in_days
print '<form name="myform" method="post" action="bio.py" class="paste">'
print '&nbsp;B-day is ............ <input type="text" name="bday" value="%s"/><br/>' % timeadd(BDAY)
print '&nbsp;Calculate date is ... <input type="text" name="ctime" value="%s"/><br/>' % timeadd(CALC_TIME)
print '<input type="submit" value=" Calculate "/></form><br/>'

print '<p><span class="paste">'

mz = []

for tmp in range(age_in_days+FROM,age_in_days+TO):
	if tmp == age_in_days: t = '%s%s%s' % (Y_LINE*int(Y_SIZE/2),X_LINE,Y_LINE*int(Y_SIZE/2))
	else: t = '%s%s%s' % (SPACE*int(Y_SIZE/2),X_LINE,SPACE*int(Y_SIZE/2))
	t = ins(t,tmp,CYCLE_P,'p')
	t = ins(t,tmp,CYCLE_E,'e')
	t = ins(t,tmp,CYCLE_I,'i')
	mz.append(t)

for t in range(0,len(mz[0])):
	t2 = ''
	for t1 in mz: t2+=t1[len(mz[0])-1-t]
	print '%s<br>' % t2.replace(' ','&nbsp;')

print '</span></p>'
print html_end