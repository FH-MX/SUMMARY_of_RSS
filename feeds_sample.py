# feeds.example.py
# このファイルをコピーして feeds.py を作り、購読したい URL を記入してください
# このファイル自体は編集しないこと（GitHub に上げるサンプルです）

CATEGORIES = {
    # "カテゴリ名": ["https://example.com/feed", ...],
}

# FEED_URLS は CATEGORIES から自動生成
FEED_URLS = [url for urls in CATEGORIES.values() for url in urls]

LIMIT = 10  # 1フィードから取得する最大記事数