#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import with_statement
import urllib
import lxml
from lxml import etree, html
import sys
import re
import MySQLdb as mdb
import os
import lxml.html as lh
import logging


i=0

specjalizacja = 'hematolog'


#con = mdb.connect(host='127.0.0.1', user='root', passwd='weHu8aza', db='spislekarzy', port=3307, charset='utf8')
con = mdb.connect(host='127.0.0.1', user='root', passwd='', db='spislekarzy', port=3306, charset='utf8')

def ile_stron():
	
	Link = "http://spislekarzy.pl/"+specjalizacja+"/p,1"
	sock = urllib.urlopen(Link)
	tree = lh.parse(Link)
	print Link 
	htmlsource = sock.read()
	sock.close()
	root = etree.HTML(htmlsource)
	i = 1

	max = ''.join(tree.xpath("/html/body/div[2]/div/div[2]/div/p/a[11]/@href")).strip().split(',')
	max = int(max[1])
	return max
	
	
def dane_pattern(count):
	print count
	Link = "http://spislekarzy.pl/"+specjalizacja+"/p,"+str(count)
	sock = urllib.urlopen(Link)
	tree = lh.parse(Link)
	print Link 
	htmlsource = sock.read()
	sock.close()
	root = etree.HTML(htmlsource)
	i = 1

	
	sublink = ''.join(tree.xpath("/html/body/div[2]/div/div[2]/div/ol/li[1]/h3/a/@href")).strip().encode('utf-8')
	print 'http://spislekarzy.pl/' + sublink
	sock2 = urllib.urlopen('http://spislekarzy.pl/' + sublink)
	tree2 = lh.parse('http://spislekarzy.pl/' + sublink)
	print i, sublink 
	htmlsource2 = sock2.read()
	sock2.close()
	root = etree.HTML(htmlsource2)
	
	nazwa = ''.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/h1/text()")).strip()
	spec = ' | '.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul[1]/*/text()")).strip()
	web = ''.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul[2]/li[1]/ul/li[@class='web']/a/@href")).strip()
	
	phone = ''.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul[2]/li[1]/ul/li[@class='phone']/text()")).strip()
	phone = phone.replace(' ','').replace('-','')
	
	
	email = ''.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul[2]/li[1]/ul/li[@class='email']/a/@href")).strip()
	email = email[7:]
	
	adres = ' '.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul[2]/li[3]/p/text()")).strip()
	adres = adres.split(',')
	
	print i
	print 'nazwa: ' , nazwa.encode('utf-8')
	print 'spec: ', spec.encode('utf-8')
	print 'phone: ', phone.encode('utf-8')
	print 'web: ', web.encode('utf-8')
	print 'email: ', email.encode('utf-8')
	
	with con:
		if nazwa is not '':
			cur = con.cursor()
			cur.execute("SELECT `imie` FROM lekarze WHERE `imie` = %s AND email = %s", (nazwa.encode('utf-8'), email.encode('utf-8')))
			dupl = cur.fetchone()
			if dupl is None:
				cur.execute("INSERT INTO lekarze (`imie`, `specjalizacja`, telefon, email, www, adres, miasto) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nazwa.encode('utf-8'), spec.encode('utf-8'), phone.encode('utf-8'), email.encode('utf-8'), web.encode('utf-8'), adres[0].encode('utf-8'), adres[1].encode('utf-8')))
			else:
				print 'juz bylo'

	
	for k in range (0,56):
		i=i+1
		try:
										   
			sublink = ''.join(tree.xpath("/html/body/div[2]/div/div[2]/div/ol/li["+str(i)+"]/h3/a/@href")).strip().encode('utf-8')
			sock2 = urllib.urlopen('http://spislekarzy.pl/' + sublink)
			tree2 = lh.parse('http://spislekarzy.pl/' + sublink)
			htmlsource2 = sock2.read()
			sock2.close()
			root = etree.HTML(htmlsource2)
			
			nazwa = ''.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/h1/text()")).strip()
			spec = ' | '.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul[1]/*/text()")).strip()
			web = ''.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul[2]/li[1]/ul/li[@class='web']/a/@href")).strip()
			
			phone = ''.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul[2]/li[1]/ul/li[@class='phone']/text()")).strip()
			phone = phone.replace(' ','').replace('-','')
			
			email = ''.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul[2]/li[1]/ul/li[@class='email']/a/@href")).strip()
			email = email[7:]
			
			adres = ' '.join(tree2.xpath("/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/ul[2]/li[3]/p/text()")).strip()
			adres = adres.split(',')
			
			print i
			print 'nazwa: ' , nazwa.encode('utf-8')
			print 'spec: ', spec.encode('utf-8')
			print 'phone: ', phone.encode('utf-8')
			print 'web: ', web.encode('utf-8')
			print 'email: ', email.encode('utf-8')
			
			with con:
				if nazwa is not '':
					cur = con.cursor()
					cur.execute("SELECT `imie` FROM lekarze WHERE `imie` = %s AND email = %s", (nazwa.encode('utf-8'), email.encode('utf-8')))
					duppl = cur.fetchone()
					if dupl is None:
						cur.execute("INSERT INTO lekarze (`imie`, `specjalizacja`, telefon, email, www, adres, miasto) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nazwa.encode('utf-8'), spec.encode('utf-8'), phone.encode('utf-8'), email.encode('utf-8'), web.encode('utf-8'), adres[0].encode('utf-8'), adres[1].encode('utf-8')))
					else:
						print 'juz bylo'
		except:
			nazwa = ''


n = ile_stron();
print n
for i in range (1,n+2):
	try:
		r = dane_pattern(i)
	except Exception, e:
		logging.exception(e)

		

