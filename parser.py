import feedparser

d = feedparser.parse('http://www.20minutos.es/rss/')
print(d.feed.title)
