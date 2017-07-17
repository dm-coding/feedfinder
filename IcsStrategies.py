import requests
from .Strategies import *
from .validators import *
from urllib.parse import urlparse, parse_qs

class EmbeddedIcsStrategy(PageContentStrategy):
	def execute(self):
		print("Executing embeded iframe ICS strategy")
		for iframe in self.content.findAll("iframe"):
			if "calendar.google.com" in iframe.get("src") or "@gmail.com" in iframe.get("src"):
				iframe_src = urlparse(iframe.get("src"))
				params = parse_qs(iframe_src.query)
				for thing in params['src']:
					if "@" in thing:
						self.possible_feeds.add("https://calendar.google.com/calendar/ical/%s/public/basic.ics" % thing.replace("@", "%40"))
					elif "%40" in thing:
						self.possible_feeds.add("https://calendar.google.com/calendar/ical/%s/public/basic.ics" % thing)
		return self.possible_feeds

class LinkRelIcsStrategy(PageContentStrategy):
	def execute(self):
		print("Executing ICS link rel strategy")
		for f in self.content.findAll("link", rel="alternate"):
			found_feed = FeedFindStrategy.check_attribs(node=f, check="type", check_contains=["calendar", "ics"], return_attrb="href")
			if found_feed: self.possible_feeds.add(found_feed)
		return self.possible_feeds

class HyperlinkIcsStrategy(HrefStrategy):
	def execute(self):
		print("Executing ICS hyperlink strategy")
		for a in self.content.findAll("a", href=True):
			found_feed = FeedFindStrategy.check_attribs(node=a, check="href", check_contains=["calendar", ".ics"], return_attrb="href")
			if found_feed:
				if "://" in href: self.possible_feeds.add(found_feed)
				else: self.possible_feeds.add(self.base_url + found_feed)
		return self.possible_feeds

class ChildPageIcsStrategy(ChildPageStrategy):
	def execute(self):
		print("Executing ICS child page strategy")
		possible_pages = set()
		for a in self.content.findAll("a", href=True):
			href = a.get("href")
			for term in [ "event", "calendar", "ics", "ical" ]:
				if term in href or (a.text and term in a.text.lower()):
					if "://" in href: possible_pages.add(href)
					else: possible_pages.add(self.base_url + href)

		for page in possible_pages:
			self.validator.validate_page(page)
			for strategy in [
				EmbeddedIcsStrategy(feedfinder=self.feedfinder, key=page),
				self.validator,
				#DefaultIcsStrategy(site=page),
				LinkRelIcsStrategy(feedfinder=self.feedfinder, key=page), 
				HyperlinkIcsStrategy(feedfinder=self.feedfinder, key=page),
			]:
				self.possible_feeds = self.possible_feeds.union(strategy.execute())

				self.feedfinder.feeds["ics_feeds"] = self.feedfinder.feeds["ics_feeds"].union(self.validator.validate(self.possible_feeds))
				if self.feedfinder.feeds["ics_feeds"]: break
		return self.feedfinder.feeds["ics_feeds"]

# class DefaultIcsStrategy(FeedFindStrategy):
# 	def __init__(self, site):
# 		self.site = site
# 	def execute(self):
# 		print("Executing RSS default feed location strategy")
# 		r = requests.get(self.site + "/events")
# 		if r.status_code == requests.codes.ok: self.possible_feeds.add(r.url) 
# 		return self.possible_feeds