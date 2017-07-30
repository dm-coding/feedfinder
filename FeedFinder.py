from .RssStrategies import *
from .IcsStrategies import *
from .validators import *

class FeedFinder(object):
	def __init__(self, root_url):
	 	''' Initalize the object's shared memory cache. '''
	 	self.cache = CacheManager(root_url)

	def get_rss_feed(self, url):
		''' RSS feeds use the default strategry, the link rel strategry, the hyperlink strategy, and a child page strategy.
		Since the child page strategy requires use of the validator, initialize it first. Then return the first feed found by any of the strategies.
		Start on the first page passed to the constructor, and label that with the cache key `/`. '''

		rss_validator = RssValidator(cache=self.cache)
		rss_feeds = self.find_feed(
			feed_type="rss_feeds",
			validator=rss_validator,
			url=url,
			cache=self.cache,
			strategies=[
				DefaultRssStrategy,
				LinkRelRssStrategy,
				HyperlinkRssStrategy,
				ChildPageRssStrategy,
		])
		return rss_feeds.pop() if rss_feeds else None

	def get_ics_feed(self, url):
		''' ICS feeds use the embedded iframe strategry, the link rel strategry, the hyperlink strategy, and a child page strategy.
		Since the child page strategy requires use of the validator, initialize it first. Then return the first feed found by any of the strategies.
		Start on the first page passed to the constructor, and label that with the cache key `/`. '''
		ics_validator = IcsValidator(cache=self.cache)
		ics_feeds = self.find_feed(
			feed_type="ics_feeds",
			validator=ics_validator,
			url=url,
			cache=self.cache,
			strategies=[
				#DefaultIcsStrategy(site=self.urls['/']['url']),
				EmbeddedIcsStrategy,
				LinkRelIcsStrategy,
				HyperlinkIcsStrategy,
				ChildPageIcsStrategy,
		])
		return ics_feeds.pop() if ics_feeds else None

	def find_feed(self, strategies, feed_type, validator, cache, url):
		''' Execute all strategies in the provided list. Each strategy will provide a list of possible feeds, so
		merge that list with the existing list of possible feeds and then validate each item in the list.
		(The validator takes care of caching the result of each URL validation for speed, not us.)
		Return the first found valid feed or none. '''
		for strategy in strategies:
			#self.possible_feeds[feed_type] |= strategy.execute()
			#print(" Possible feeds after execution of strategy: ")
			#print("\n".join(self.possible_feeds[feed_type]))
			#self.feeds[feed_type] |= validator.validate(self.possible_feeds[feed_type])
			#print(" Found feeds after execution of strategy: ")
			#print("\n".join(self.feeds[feed_type]))
			#if self.feeds[feed_type]: return self.feeds[feed_type].pop()
			feeds = strategy(cache=cache, url=url)
			print("Possible feeds after strategy:")
			print("\n".join(feeds))
			feeds = validator.validate(feeds)
			print("Found feeds after execution of strategy:")
			print("\n".join(feeds))
			if feeds: return feeds
		return set()