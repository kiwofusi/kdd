# -*- coding: utf-8 -*-

import feedparser

# 注目エントリーから記事を取得する
def get_hot():
	d = feedparser.parse("http://b.hatena.ne.jp/entrylist?mode=rss&sort=hot&threshold=3")
	items = []
	for e in d.entries[0:29]:
		items.append({'url':e.link, 'title':e.title})
	return items
	

import simplejson
import urllib
# 記事からユーザを取得する
def get_urlposts(url):
	url = 'http://b.hatena.ne.jp/entry/json/?url=' + url
	lines = urllib.urlopen(url)
	for line in lines:
		line = line.strip(')')
		line = line.strip('(')
	json = simplejson.loads(line)

	try:
		users = []
		for u in json['bookmarks']:
			users.append({'user':u['user']})
	except AttributeError:
		users = ''
	except TypeError:
		users = ''
	
	return users


# ユーザから記事を取得する
def get_userposts(user):
	url = 'http://b.hatena.ne.jp/' + user + '/atomfeed'
	page = 0
	limit = 2
	items = []
	while(page < limit):
		d = feedparser.parse(url + "?of=" + str(page*30))
		for e in d.entries:
			try:
				tags = []
				for t in e.tags:
					tags.append(t['term'])
			except AttributeError:
				tags = ''
			items.append({'url':e.links[0].href, 'title':e.title, 'tag':tags})
		page += 1
	return items


# 記事からタグを取得する
def get_itemtags(url):
	tags = []
	url = 'http://b.hatena.ne.jp/entry/json/?url=' + url
	lines = urllib.urlopen(url)
	for line in lines:
		line = line.strip(')')
		line = line.strip('(')
	try:
		json = simplejson.loads(line)
		for u in json['bookmarks']:
			tags.extend(u['tags'])
	except TypeError:
		tags = ''
	except AttributeError:
		tags = ''
	except ValueError:
		tags = ''
	
	return tags