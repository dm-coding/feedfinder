Python FindFeed
==============

Utility suite optimized for fast-feed finding of embedded RSS and iCal feeds. Its job is **not** to find *all* feeds on a page, but only to find the first. It uses a smart cache handler and attempts to make the fewest outgoing requests possible. This makes it exceptionally fast, and good for web applications.

Strategies
----------
FindFeed executes various strategies to find a feed. After executing a strategy, FindFeed validates the suspected feeds and returns the first valid one. Despite the fact that the strategies differ depending on whether one is looking for RSS or iCal feeds, strategies are somewhat broadly similar:

* Embedded strategies search for <iframe> tags and parse them accordingly. The Embedded ICS strategy currently only finds iframe-embedded google calendars as these are the most common.
* LinkRel strategies search for <link rel=""> tags
* Hyperlink strategies search for hyperlinks (the <a> tag) and inspect the href attributes and text contents for likely matches.
* ChildPageStrategies, technically a kind of Hyperlink strategy, searches hyperlinks on a given page looking for links to other pages (e.g. "Blog page", "news page", "calendar page", "events page", etc.) On these other pages, ChildPageStrategies execute some further number of strategies such as an embedded stratgegy, a linkrel strategy, or a hyperlink strategy. ChildPageStrategies are not recursive.
* Default strategies search for the presence of a given URL, e.g. "/feed". (Given that 30%+ of all websites have RSS feeds at this location due to running Wordpress, this is a surprisingly simple, fast and effective mechanism).
* Validator strategies simply use a validator to check whether the suspected URL is, in fact, a feed.

Validators
----------
After a strategy has found a number of suspected feeds, FeedFinder attempts to validate these feeds and return the first one. Two validators are included:

* An ICS validator, which uses `ics.Calendar`
* An RSS validator, which uses `feedparser`.

You must have both of these libraries, along with `urlib` and `requests` to use this utility.

Requirements
-----
Along with ics.Calendar and feedparser, BeautifulSoup (bs4) is also required. A requirements.txt file is provided for you to pass to pip.

Usage
--------

CLI:

    python findfeed.py https://example.com

By default, CLI will fetch both kinds of feed. To fetch only one, try `--ics` or `--rss`.

FeedFinder:
    from .FeedFinder import FeedFinder
    feeds = FeedFinder(self.website)
    if not self.news_feed: self.news_feed = feeds.get_rss_feed()
    if not self.ical_feed: self.ical_feed = feeds.get_ics_feed()

You can also use the feed validators separately by calling their `validate_single` argument with the URL to check, for example:

    from .validators import RssValidator
    validator = RssValidator()
    return HttpResponse() if validator.validate_single(request.POST.get("feed_url")) else HttpResponse(status=504)

Like the FeedFinder object itself, Validators cache the results of their validation.

TODO
===
* A flag should control whether it returns all feeds or just some.
* A CLI utility suite would be very nice.