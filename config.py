# config.py
# 接続先とRSSの設定

# RSS
# feeds.py が存在しない場合はサンプルにフォールバック
try:
    from feeds import FEED_URLS, LIMIT  # 実際のフィード一覧（非公開）
except ImportError:
    from feeds_sample import FEED_URLS, LIMIT  # サンプルで代替
    print("[警告] feeds.py が見つかりません。feeds_sample.py で動作しています。")

# A: Ollama
BASE_URL = "http://localhost:11434/v1" # Ollama の OpenAI 互換エンドポイント
API_KEY = "hoge" # ローカルはダミーで OK（中身は無視される）
MODEL = "qwen2.5-coder:7b"


# B: LM Studio
# BASE_URL = "http://localhost:1234/v1" # LM Studio サーバのデフォルト
# API_KEY = "hoge" # ローカルはダミーで OK
# MODEL = "" # LM Studio で読み込んだモデルの ID
