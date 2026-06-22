# rss_summarizer.py
# RSS ニュースを取得して、ローカル LLM（Ollama / LM Studio）で要約するツール。

import feedparser
from openai import OpenAI

import config

def fetch_articles(feed_url, limit):
    # RSS フィードを取得して記事を返す
    parsed = feedparser.parse(feed_url)
    articles = []
    for entry in parsed.entries[:limit]:
        title = entry.get("title", "タイトルなし")
        link = entry.get("link", "リンクなし")
        summary = entry.get("summary", "要約なし")
        articles.append({"title": title, "summary": summary, "link": link})
    return articles

def make_client():
    # config.py の設定から OpenAI 互換クライアントを作って返す
    return OpenAI( 
        base_url=config.BASE_URL,
        api_key=config.API_KEY, 
        )

def summarize(client, text):
    # LLM に要約を依頼して返す
    if not text.strip():
        return "要約するテキストがありません。"
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=[
            {"role": "system", "content": "あなたは優秀な編集者です。日本語で簡潔に要約します。"},
            {"role": "user", "content": f"次のニュースを要約して要約してください:\n{text}"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content

def main():
    # プログラムの入り口。全体の流れをここで組み立てる
    client = make_client() # 1) LLM クライアントを用意
    for feed_url in config.FEED_URLS: # フィードを1つずつ処理
        print(f"\n=== フィード: {feed_url} ===")
        articles = fetch_articles(feed_url, config.LIMIT) # RSS から記事を取得
        if not articles:
            print("記事が取得できませんでした。スキップします。")
            continue
        for i, article in enumerate(articles, start=1):
            print(f"\n[{i}] {article['title']}")
            print(f" URL: {article['link']}")
            result = summarize(client, article["summary"])
            print(f" 要約: {result}")

if __name__ == "__main__": 
    main() 