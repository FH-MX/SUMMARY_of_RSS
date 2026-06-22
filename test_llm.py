# test_llm.py
# LLMの呼ぶためのテスト
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",  # LLMのエンドポイント
    api_key="hoge"  # API Key(ローカルの場合はダミー)
)

response = client.chat.completions.create(
    model = "qwen2.5-coder:7b",  # 使用するモデル
    messages = [
        {"role": "system", "content": "日本語で簡潔に要約します"},
        {"role": "user", "content": "現在の私の身体的状態を総合的に観察した結果として、特に胃部周辺において継続的かつ無視しがたい空腹感が発生しており、このことは直近の食事から相応の時間が経過したことを示唆している。そのため、今この時点において、何らかの食品を摂取することが望ましいのではないかと強く感じているところである。"},
    ],
)
print(response.choices[0].message.content)