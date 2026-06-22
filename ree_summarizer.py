# rss_summarizer.py
# RSS ニュースを取得して、ローカル LLM（Ollama / LM Studio）で要約するツール。

import feedparser
from openai import OpenAI
import os
import datetime

import config

def fetch_articles(feed_url, limit, days):
    # days 日分の記事を RSS から取得して返す
    parsed = feedparser.parse(feed_url)
    articles = []
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    for entry in parsed.entries[:limit]:
        # 日付情報があれば期間フィルタ、なければそのまま含める
        pub = entry.get("published_parsed") or entry.get("updated_parsed")
        if pub:
            pub_dt = datetime.datetime(*pub[:6], tzinfo=datetime.timezone.utc)
            if pub_dt < cutoff:
                continue  # 古い記事はスキップ
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

def summarize_all(client, articles, days):
    # 全記事をまとめて1つに要約する
    if not articles:
        return "記事が収集できませんでした。"

    # 各記事を「タイトル + RSS本文200文字」に整形してまとめる
    # （ローカルLLMのコンテキスト制限対策）
    lines = []
    for i, a in enumerate(articles, start=1):
        short_summary = a["summary"][:200].replace("\n", " ")  # 200文字に切り詰め
        lines.append(f"{i}. 【{a['title']}】{short_summary}")

    combined_text = "\n".join(lines)

    response = client.chat.completions.create(
        model=config.MODEL,
        messages=[
            {"role": "system", "content": "あなたは優秀な編集者です。日本語で簡潔にまとめます。"},
            {"role": "user", "content": (
                f"以下は過去{days}日分のRSS記事{len(articles)}件です。\n"
                "主要トピックをカテゴリ別にまとめた日報として日本語で要約してください。\n\n"
                f"{combined_text}"
            )},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content

# 変更後
def main():
    client = make_client()
    all_articles = []  # 全フィードの記事をここにまとめる

    # 全フィードから記事を収集
    for feed_url in config.FEED_URLS:
        print(f"取得中: {feed_url}")
        articles = fetch_articles(feed_url, config.LIMIT, config.DAYS)
        all_articles.extend(articles)

    print(f"\n収集記事数: {len(all_articles)} 件（過去{config.DAYS}日分）")

    if not all_articles:
        print("記事が見つかりませんでした。")
        return

    # LLMで全体まとめを生成
    print("\nまとめを生成中...")
    summary = summarize_all(client, all_articles, config.DAYS)

    # ターミナルに表示
    today = datetime.date.today().isoformat()
    print(f"\n========== RSS まとめ ({today}) ==========")
    print(summary)

    # Markdownファイルに保存
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(config.OUTPUT_DIR, f"{today}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"# RSS まとめ ({today})\n\n")
        f.write(f"期間: 過去{config.DAYS}日 / 収集記事数: {len(all_articles)}件\n\n")
        f.write("## 全体まとめ\n\n")
        f.write(summary + "\n\n")
        f.write("---\n")
        f.write(f"*生成日時: {now_str}*\n")

    print(f"\n保存先: {output_path}")

if __name__ == "__main__": 
    main() 