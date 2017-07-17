import feedparser
from urllib.request import urlopen
from ics import Calendar

class FeedValidator(object):
	checked_feeds = {}
	def validate(self, feeds):
		for feed in feeds:
			self.validate_single(feed)
			if self.checked_feeds[feed]: break
			else: print("Not a valid URL: " + feed)
		return [ feed for feed, validated in self.checked_feeds.items() if validated ]

	def validate_page(self, url):
		self.page = url

	def execute(self):
		print("Executing link validator strategy")
		if self.page not in self.checked_feeds:
			self.checked_feeds[self.page] = self.validate_single(self.page)
		return [ feed for feed, validated in self.checked_feeds.items() if validated ]

class RssValidator(FeedValidator):
	def validate_single(self, feed):
		if feed not in self.checked_feeds:
			self.checked_feeds[feed] = len(feedparser.parse(feed).entries) > 0
		return self.checked_feeds[feed]

class IcsValidator(FeedValidator):
	def validate_single(self, feed):
		if feed not in self.checked_feeds:
			self.checked_feeds[feed] = bool(Calendar(urlopen(feed).read().decode('iso-8859-1')))
		return self.checked_feeds[feed]