import requests
from bs4 import BeautifulSoup as bs4
from .RssStrategies import *
from .IcsStrategies import *
from .validators import *

class FeedFinder(object):
	def __init__(self, root_url):
		self.urls = { "/": { "url": root_url } }
		self.possible_feeds = { "rss_feeds": set(), "ics_feeds": set() }
		self.feeds = { "rss_feeds": set(), "ics_feeds": set() }

	def get_rss_feed(self):
		rss_validator = RssValidator()
		return self.find_feed(
			key='/', 
			feed_type="rss_feeds", 
			validator=rss_validator,
			strategies=[
				DefaultRssStrategy(site=self.urls['/']['url']),
				LinkRelRssStrategy(feedfinder=self, key='/'), 
				HyperlinkRssStrategy(feedfinder=self, key='/'),
				ChildPageRssStrategy(feedfinder=self, key='/', validator=rss_validator),
		])

	def get_ics_feed(self):
		ics_validator = IcsValidator()
		return self.find_feed(
			key='/', 
			feed_type="ics_feeds", 
			validator=ics_validator,
			strategies=[
				#DefaultIcsStrategy(site=self.urls['/']['url']),
				EmbeddedIcsStrategy(feedfinder=self, key='/'),
				LinkRelIcsStrategy(feedfinder=self, key='/'), 
				HyperlinkIcsStrategy(feedfinder=self, key='/'),
				ChildPageIcsStrategy(feedfinder=self, key='/', validator=ics_validator),
		])

	def find_feed(self, strategies, feed_type, key, validator):
		for strategy in strategies:
			self.possible_feeds[feed_type] = self.possible_feeds[feed_type].union(strategy.execute())
			self.feeds[feed_type] = self.feeds[feed_type].union(validator.validate(self.possible_feeds[feed_type]))
			if self.feeds[feed_type]: return self.feeds[feed_type].pop()
		return None

	def get_page_content(self, key):
		if key not in self.urls: self.urls[key] = {
				"content": bs4(requests.get(key).text, "html5lib"),
				"url": key
			}
		elif "content" not in self.urls[key]: self.urls[key]["content"] = bs4(requests.get(self.urls[key]["url"]).text, "html5lib")
		return self.urls[key]["content"]