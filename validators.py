from .CacheManager import *
from ics import Calendar
import feedparser

class FeedValidator(object):
	def __init__(self, cache):
		self.checked_feeds = {}
		cache.addResolver(itemName="page_src", resolver=remote_content_resolver)
		self.cache = cache
		print(" New feed validator initalized (CacheManager="+cache.default_key+")")

	def validate(self, feeds):
		#print ("********* ATTEMPTING TO VALIDATE FEEDS : **************")
		for feed in feeds:
			print("-----------------> " + feed)
			self.validate_single(feed)
			if self.checked_feeds[feed]: break
			#else: print("Not a valid URL: " + feed)
		for f in self.checked_feeds:
			print("========== > Checked feeds: %s (%s)" % (f, self.checked_feeds[f]))
		return { feed for feed, validated in self.checked_feeds.items() if validated }

	def execute(self, cache, url):
		print("Executing link validator strategy: " + url)
		if self.page not in self.checked_feeds:
			self.checked_feeds[self.page] = self.validate_single(self.page)
		#return { feed for feed, validated in self.checked_feeds.items() if validated }
		return { self.page }

class RssValidator(FeedValidator):
	def validate_single(self, feed):
		print("Validating single RSS feed %s" % feed)
		if feed not in self.checked_feeds:
			try:
				self.checked_feeds[feed] = len(feedparser.parse(self.cache.get(feed, "page_src").text).entries) > 0
			except Exception:
				self.checked_feeds[feed] = False
		return self.checked_feeds[feed]

class IcsValidator(FeedValidator):
	def validate_single(self, feed):
		print("Validating single ICS feed %s" % feed)
		if feed not in self.checked_feeds: #urlopen(feed).read().decode('iso-8859-1')
			try:
				self.checked_feeds[feed] = bool(Calendar(self.cache.get(feed, "page_src").text))
			except Exception:
				self.checked_feeds[feed] = False
		return self.checked_feeds[feed]