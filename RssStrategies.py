import requests
from .Strategies import *
from .validators import *

def LinkRelRssStrategy(cache, url):
	feeds = set()
	content = cache.get(key=url, itemName="page_content")

	print("Executing RSS link rel strategy on page %s" % url)
	for f in content.findAll("link", rel="alternate"):
		found_feed = check_attribs(node=f, check="type", check_contains=["rss", "xml"], return_attrb="href")
		if found_feed:
			feeds.add(found_feed)
	return feeds

def HyperlinkRssStrategy(url, cache):
	feeds = set()
	content = cache.get(key=url, itemName="page_content")

	print("Executing RSS hyperlink strategy on page %s" % url)
	for a in content.findAll("a", href=True):
		found_feed = check_attribs(node=a, check="href", check_contains=["rss", "xml"], return_attrb="href")
		if found_feed:
			if "://" in a['href']: feeds.add(found_feed)
			else: feeds.add(self.base_url + found_feed)
	return feeds

def ChildPageRssStrategy(url, cache):
	validator = RssValidator(cache=cache)
	print("Executing RSS child page strategy on page %s" % url)
	for page in find_child_pages(
			pages=[ "blog", "news", "rss", "feed" ],
			url=url,
			cache=cache,
		):
		print("Found child page: %s" % page)
		for strategy in [
			DefaultRssStrategy,
			LinkRelRssStrategy,
			HyperlinkRssStrategy,
		]:
			possible_feeds = strategy(cache=cache, url=page)
			feeds = validator.validate(possible_feeds)
			if feeds: return feeds
	return set()

def DefaultRssStrategy(cache, url):
	print("Executing RSS default feed location strategy")
	#r = requests.get(self.site + "/feed")
	r = cache.get(key=url + "/feed/", itemName="page_src")
	if r and r.status_code == requests.codes.ok:
		print("Found after "+ r.url + " after execution of default RSS strategy")
		return { r.url }
	return set()