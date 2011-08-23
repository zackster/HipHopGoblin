import os
import re
import sys
import urllib
import BeautifulSoup
import json
#import simplejson
from models import Song as AppSong
import random
from django.http import HttpResponse
import logging
from django.core import serializers

URLS_LIST = ['http://pigeonsandplanes.com/', 'http://www.2dopeboyz.com/', 'http://agrumpyoldmanwithabeard.blogspot.com/', 'http://www.cocaineblunts.com/blunts/?page_id=1074']

URLS_LIST2 = ['http://3hive.com']

URLS_LIST3 = ['http://fakeshoredrive.com/','http://earmilk.com','http://passionweiss.com','http://creamteam.tv',]

MAX_DEPTH = 6
LOG_FILENAME = '/home/hiphopgoblin/logs/user/debug.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

def song(url, text):
	if url[-4:] == '.mp3':
		try:
			s = AppSong(url=url, title=text, count=0)
			s.save()
			logging.debug('song saved')
		except:
			logging.debug('song found, could not be saved')
		return (url, text)

def site(url, text):
	if url[-4:] != '.mp3' and url[:7] == 'http://':
		logging.debug(url)
		return url

def strip_tags(string):
	tag = re.compile(r'<.*?>')
	return tag.sub(' ', string)

def separate(lst):
	songs = [song(x,y) for x,y in lst]
	sites = [site(x,y) for x,y in lst]
	return (sites, songs)

class Node(object):
	def __init__(self, url, depth, top):
		self.url = url
		self.children = []
		self.songs = []
		self.depth = depth
		self.topNode = top

	def openResources(self):
		try:
			f = urllib.urlopen(self.url)
			logging.debug('urllib worked')
			return BeautifulSoup.BeautifulSoup(f.read())
		except:
			logging.debug('rsrcs opening fail ')
			return False

	def getUrls(self):
		link_list = []
		soup = self.openResources()
		if soup:
			logging.debug('returned a soup obj')
			links = soup.findAll('a')
			for l in links:
				try:
					link_list.append((l['href'], strip_tags((' ').join(str(t) for t in l.contents))))
					logging.debug('appended' + l['href'])
				except:
					logging.debug('could not append')
		return link_list

	def visit(self, scraper):
		logging.debug('visited')
		if self.depth <= MAX_DEPTH:
			urls_list, self.songs = separate(self.getUrls())
			self.children = [UnderNode(parent=self, top=self.topNode, url=x) for x in urls_list]
			self.pushSongs(scraper)
			for x in self.children:
				x.visit(scraper)
		else:
			return

	def pushSongs(self, scraper):
		scraper.songs = [scraper.songs.append(s) for s in self.songs]

class TopNode(Node):
	def __init__(self, url):
		super(TopNode, self).__init__(url, 0, top=self)

class UnderNode(Node):
	def __init__(self, parent, top, url):
		super(UnderNode, self).__init__(url, parent.depth + 1, top)
		self.topNode = top

	def pushSongs(self, scraper):
		scraper.songs = [scraper.songs.append(s) for s in self.songs]

class Scraper:
	def __init__(self, urls):
		self.songs = []
		self.topNodes = [TopNode(x) for x in urls]

	def collectSongs(self):
		self.songs = [x.songs for x in self.topNodes]
		return self.songs

class Song:
	def __init__(self, url, text):
		self.url = url
		self.text = text

	def __unicode__(self):
		return self.url + " --- " + self.text

def scrape(songid=None):
	#scraper = Scraper(URLS_LIST)
	#for node in scraper.topNodes:
		#node.visit()
	#for song in scraper.collectSongs():
		#print song
		#print
	json_serializer = serializers.get_serializer("json")()
	if songid:
		s = AppSong.objects.get(id=songid)
	else:
		count = len(AppSong.objects.all())
		index = random.randint(1,count)
		s = AppSong.objects.all()[index-1]
	#json.write({"filename":s.url, "title":s.title, "count":s.count,"id":s.id,})
	return json.write({"filename":s.url, "title":s.title, "count":s.count,"id":s.id,})



def main():
	scraper = Scraper(URLS_LIST)
	for node in scraper.topNodes:
		node.visit(scraper)

def getsongs(request):
	logging.debug('called getsongs')
	scraper = Scraper(URLS_LIST3)
	for node in scraper.topNodes:
		node.visit(scraper)
	return HttpResponse()
