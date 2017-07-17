import urllib.parse

class FeedFindStrategy(object):
	found_feeds = set()
	possible_feeds = set()
	def check_attribs(node, check, check_contains, return_attrb):
		c = node.get(check, None)
		if c:
			for needed_attrib in check_contains:
				if needed_attrib in c:
					return node.get(return_attrb, None)
		return None

class PageContentStrategy(FeedFindStrategy):
	def __init__(self, feedfinder, key):
		self.content = feedfinder.get_page_content(key=key)
		self.feedfinder = feedfinder

class HrefStrategy(PageContentStrategy):
	def __init__(self, feedfinder, key):
		parsed_url = urllib.parse.urlparse(feedfinder.urls[key]['url'])
		self.base_url = parsed_url.scheme + "://" + parsed_url.hostname
		PageContentStrategy.__init__(self, feedfinder, key)

class ChildPageStrategy(HrefStrategy):
	def __init__(self, feedfinder, validator, key):
		self.validator = validator
		HrefStrategy.__init__(self, feedfinder, key)