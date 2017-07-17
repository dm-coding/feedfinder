import requests
from .Strategies import *
from .validators import *

class LinkRelRssStrategy(PageContentStrategy):
	def execute(self):
		print("Executing RSS link rel strategy")
		for f in self.content.findAll("link", rel="alternate"):
			found_feed = FeedFindStrategy.check_attribs(node=f, check="type", check_contains=["rss", "xml"], return_attrb="href")
			if found_feed: self.possible_feeds.add(found_feed)
		return self.possible_feeds

class HyperlinkRssStrategy(HrefStrategy):
	def execute(self):
		print("Executing RSS hyperlink strategy")
		for a in self.content.findAll("a", href=True):
			found_feed = FeedFindStrategy.check_attribs(node=a, check="href", check_contains=["rss", "xml"], return_attrb="href")
			if found_feed:
				if "://" in href: self.possible_feeds.add(found_feed)
				else: self.possible_feeds.add(self.base_url + found_feed)
		return self.possible_feeds

class ChildPageRssStrategy(ChildPageStrategy):
	def execute(self):
		print("Executing RSS child page strategy")
		possible_pages = set()
		for a in self.content.findAll("a", href=True):
			for term in [ "blog", "news", "rss", "feed" ]:
				if term in a.text.lower():
					href = a.get("href")
					if "://" in href: possible_pages.add(href)
					else: possible_pages.add(self.base_url + href)

		for page in possible_pages:
			self.validator.validate_page(page)
			for strategy in [
				self.validator,
				DefaultRssStrategy(site=page),
				LinkRelRssStrategy(feedfinder=self.feedfinder, key=page), 
				HyperlinkRssStrategy(feedfinder=self.feedfinder, key=page),
			]:
				self.possible_feeds = self.possible_feeds.union(strategy.execute())

				self.feedfinder.feeds["rss_feeds"] = self.feedfinder.feeds["rss_feeds"].union(self.validator.validate(self.possible_feeds))
				if self.feedfinder.feeds["rss_feeds"]: break
		return self.feedfinder.feeds["rss_feeds"]

class DefaultRssStrategy(FeedFindStrategy):
	def __init__(self, site):
		self.site = site
	def execute(self):
		print("Executing RSS default feed location strategy")
		r = requests.get(self.site + "/feed")
		if r.status_code == requests.codes.ok: self.possible_feeds.add(r.url) 
		return self.possible_feeds