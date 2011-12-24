#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Generate ip's for iptable                                                #
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

import socket

servers = ['nedbsd.nl','jabber.rtanet.ru','jabber.ufanet.ru','jabber.iptv.by','support-pc.ru','programist.ru','ubuntu-jabber.de',
		   'jabber.meta.net.nz','jabber.fr','default.co.yu','jabber.murom.net','ipse.zapto.org','jabber.second-home.de','xmpp.ir','debianforum.de',
		   'im.apinc.org','deshalbfrei.org','jabber.kh.ua','xmpp.web.id','jabber.belnet.be','hawkesnest.net','jabber.dk','nedbsd.eu','volity.net',
		   'ubuntu-jabber.net','jabster.pl','jabbim.com','bulmalug.net','jabber.cn','jabber.jp','jabber.3gnt.org','jabber.bsu.ru','jabber.sbin.org',
		   'jabber.bryansk.ru','main.gepro.cz','filip.eu.org','xabber.de','gabbler.net','jabber.at','verdammung.org','underley.eu.org','akl.lt',
		   'jabber.scunc.net','jabber.workaround.org','jabbernet.eu','braxis.org','tronet.ru','jabber.ionitcom.ru','tlug.up.ac.za',
		   'jabber.yeahnah.co.nz','roadrunner.proinet.pl','city.veganet.ru','jabber.chaotic.de','linuxlovers.at','jabbernet.dk','internet-exception.de',
		   'blessing.ru','jabber.ee','gabbler.org','vlink.ru','12jabber.net','xmppnet.de','jabber.web.id','jabber.elektron.com.pl','ojab.ru',
		   'jabber.chirt.ru','no-icq.org','netmindz.net','jabber.com.ua','maszyna.pl','jsmart.web.id','njs.netlab.cz','jabber.rdtc.ru',
		   'jabber.elcomnet.ru','jabber.postel.org','lugmen.org.ar','aster.pl','jabber.rootbash.com','jabber.cc','jabber.scha.de',
		   'jappix.com','jabber.wiretrip.org','gornyak.net','brauchen.info','911910.cn','igniterealtime.org','vayusphere.com','12jabber.com',
		   'codingteam.net','im.thiessen.it','jabber.earth.li','jabber.linux.it','jabberbr.com','jabber.ccc.de','portal-on.ru','jabbim.sk',
		   'ezvan.fr','draugr.de','nclug.ru','jabbrus.org.ua','jabbim.cz','jabber.sow.as','octoraul.com','jabber.systemli.org','gajim.org',
		   'swissjabber.ch','jabber.fsinf.at','wayround.org','aszlig.net','noicq.org','kofeina.net','jabber.zsmk.ru','jabber-hispano.org',
		   'aqq.eu','mailfr.com','bbs.docksud.com.ar','altbit.ru','jabber.iitsp.com','jabber.ch','headcounter.org','unstable.nl',
		   'jabber.rikt.ru','netcube.pl','darkdna.net','jabber.minus273.org','jabber.linuxfan.it','jabber.anywise.com','chatmask.com',
		   'sharmuta.us','swissjabber.li','jabber.al.com.ua','volgograd.ru','jabber.454.ru','limun.org','jabber.mobi','kanet.ru',
		   'isgeek.info','chel.lug.ru','jabba.mgw.pl','jabber.netrusk.net','jabber.zapsib.net','silper.cz','vzljot.ru','jabber.sk',
		   'jabber.tcweb.org','kdetalk.net','jabber.ua','jabber.icequake.net','binaryfreedom.info','web.id','macjabber.de','chrome.pl',
		   'jabber.zs1.wroc.pl','dhbit.ca','jabber.freenet.de','devzero.co.uk','jabber.kspu.kr.ua','jabbim.pl','jabber.org.ru',
		   'ggr.spb.ru','jabber.fds-net.ru','jabber.kiev.ua','jabber.ozerki.net','offlinemode.org','jabber.zp.ua','swissjabber.eu',
		   'bryansktel.ru','jid.pl','jabber80.com','jab.undernet.cz','jabber.tmkis.com','jabberes.org','jabber.psg.com','xmpp.us',
		   'default.rs','chote.net','shady.nl','jabber.lagaule.org','maszina.pl','jabber.syktsu.ru','jabber.mzk.rikt.ru','boese-ban.de',
		   'jabber.ulm.ccc.de','neko.im','gabbler.de','jabber.bol.ru','jabber.ukrwest.net','jabber.snc.ru','a-cube.vsi.ru','xmppnet.ru',
		   'jabberim.de','spbu.ru','jabber.kirovnet.ru','sameplace.cc','talk.mipt.ru','alpha-labs.net','jabber.ambrero.nl','xmpp.jp',
		   'dione.zcu.cz','highsecure.ru','jabber.od.ua','piastlan.net','jabber-br.org','jabber.hot-chilli.net','51102.ru','dominion.dn.ua',
		   'xdsl.by','pandion.im','letinet.ru','beercan.ru','jabber.justlan.ru','zlosnik.net','ims.kelkoo.net','bee.ru','jabber.produm.net',
		   'phcn.de','jabber.spbu.ru','ugatu.net','jwchat.org','jabber-fr.net','burtonini.com','jabber.mipt.ru','jabber.org.by','jabber.co.nz',
		   'jabber.cherkassy.net','thiessen.im','jabber.se','jabme.de','nedbsd.be','micro.net.ua','core.im','jabber.no','jabber.keinsinn.de',
		   'jabber4friends.de','jabber.pilgerer.de','4business.nl','jabber.me.uk','jabber.aston.ru','21region.org','jaim.at','thiessen.org',
		   'webii.ru','jabber.dn.u','jabber.tantel.ru']
		   
ip = ['46.4.163.99','46.43.34.31','62.231.161.5','62.75.218.162','62.75.218.204','64.76.18.116','65.38.17.158','69.164.216.139','77.120.80.9',
	  '77.221.155.138','78.36.196.92','80.239.54.119','80.51.20.6','81.175.86.202','82.207.68.199','83.142.206.171','83.163.63.162','83.223.73.61',
	  '85.11.66.61','85.214.136.81','85.214.93.191','85.234.2.161','85.25.137.23','85.26.173.170','86.57.151.12','86.59.34.124','87.237.201.132',
	  '88.149.132.6','88.190.17.126','88.190.23.192','88.190.239.13','88.198.198.218','88.198.198.220','88.198.198.221','88.198.204.200',
	  '88.198.216.91','88.198.6.247','88.83.200.37','88.83.236.21','90.184.12.24','91.102.11.143','91.149.162.230','91.190.93.130','91.194.60.3',
	  '91.202.24.5','92.39.64.230','93.89.215.12','94.142.245.74','95.142.163.45','97.107.128.233','128.9.112.9','131.203.119.149','140.186.70.41',
	  '176.9.17.157','178.130.18.9','178.216.101.4','188.40.80.245','193.138.244.40','193.200.42.57','194.116.252.6','194.84.141.2',
	  '194.85.80.94','194.87.5.86','195.19.225.242','195.20.118.4','195.4.20.18','195.4.20.26','195.62.15.242','212.0.66.38','212.6.7.10',
	  '213.218.118.122','213.254.12.149','213.80.130.180','216.187.72.182','217.10.10.194','217.130.250.228','217.24.113.52','217.29.21.23']

for t in servers:
	try:
		dns = socket.gethostbyname_ex(t)[2]
		print '%s [%s]' % (t,', '.join(dns))
		for d in dns:
			if d not in ip: ip.append(d)
	except: print 'Can\'t resolve %s' % t

print '-'*50
ip2 = []
for t in ip:
	if int(t.split('.')[0]) < 100: ip2.append('0%s' % t)
	else: ip2.append(t)
ip2.sort()
for t in ip2: print t if t[0] != '0' else t[1:]
print '-'*50
