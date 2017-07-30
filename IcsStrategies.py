import requests
from .Strategies import *
from .validators import *
from urllib.parse import urlparse, parse_qs

def EmbeddedIcsStrategy(cache, url):
	possible_feeds = set()
	content = cache.get(key=url, itemName="page_content")
	print("Executing embeded iframe ICS strategy on page %s" % url)
	for iframe in content.findAll("iframe"):
		if "calendar.google.com" in iframe.get("src") or "@gmail.com" in iframe.get("src"):
			iframe_src = urlparse(iframe.get("src"))
			params = parse_qs(iframe_src.query)
			for thing in params['src']:
				if "@" in thing:
					possible_feeds.add("https://calendar.google.com/calendar/ical/%s/public/basic.ics" % thing.replace("@", "%40"))
				elif "%40" in thing:
					possible_feeds.add("https://calendar.google.com/calendar/ical/%s/public/basic.ics" % thing)
	return possible_feeds

def LinkRelIcsStrategy(cache, url):
	possible_feeds = set()
	content = cache.get(key=url, itemName="page_content")
	print("Executing ICS link rel strategy on page %s" % url)
	for f in content.findAll("link", rel="alternate"):
		found_feed = check_attribs(node=f, check="type", check_contains=["calendar", "ics"], return_attrb="href")
		if found_feed: possible_feeds.add(found_feed)
	return possible_feeds

def HyperlinkIcsStrategy(cache, url):
	content = cache.get(key=url, itemName="page_content")
	print("Executing ICS hyperlink strategy on page %s" % url)
	possible_feeds = set()
	for a in content.findAll("a", href=True):
		found_feed = check_attribs(node=a, check="href", check_contains=["calendar", ".ics"], return_attrb="href")
		if found_feed:
			if "://" in a['href']: possible_feeds.add(found_feed)
			else: possible_feeds.add(self.base_url + found_feed)
	return possible_feeds

def ChildPageIcsStrategy(cache, url):
	print("Executing ICS child page strategy on page %s" % url)
	validator = IcsValidator(cache=cache)
	for page in find_child_pages(
			pages=[ "event", "calendar", "ics", "ical" ],
			url=url,
			cache=cache
		):
		print("Found child page: %s" % page)
		for strategy in [
			EmbeddedIcsStrategy,
			#self.validator,
			#DefaultIcsStrategy(site=page),
			LinkRelIcsStrategy,
			HyperlinkIcsStrategy,
		]:
			possible_feeds = strategy(url=page, cache=cache)
			feeds = validator.validate(possible_feeds)
			if feeds: return feeds
	return set()

# class DefaultIcsStrategy(FeedFindStrategy):
# 	def __init__(self, site):
# 		self.site = site
# 	def execute(self):
# 		print("Executing RSS default feed location strategy")
# 		r = requests.get(self.site + "/events")
# 		if r.status_code == requests.codes.ok: self.possible_feeds.add(r.url) 
# 		return self.possible_feeds