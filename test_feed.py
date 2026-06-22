# test_feed.py
# RSSを取得して表示

import feedparser

url = "https://zenn.dev/topics/nlp/feed" # RSSのURL
parsed = feedparser.parse(url) # RSSを解析

print("フィード名：", parsed.feed.get("title", "タイトルなし")) # フィードのタイトルを表示
for entry in parsed.entries[:3]: # 最初の3件を表示
    print("-", entry.title)
    print("  URL:", entry.link)