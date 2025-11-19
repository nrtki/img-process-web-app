## 📦 Usage (使い方)
このアプリケーションは、Python環境があれば以下の手順ですぐに動作確認が可能です。

### Prerequisites (事前準備)
- Python 3.8 以上
- Git

### 1. Clone & Setup (環境構築)
リポジトリをクローンし、プロジェクトディレクトリへ移動します。

```bash
git clone [https://github.com/あなたのユーザー名/image-processing-app.git](https://github.com/あなたのユーザー名/image-processing-app.git)
cd image-processing-app
# 仮想環境の作成と有効化 (Optional)
python -m venv .venv
# Windows (PowerShell) の場合:
.venv\Scripts\activate
# Mac/Linux の場合:
source .venv/bin/activate

# ライブラリのインストール
pip install -r requirements.txt

# backendサーバ起動
uvicorn main:app --reload --host 0.0.0.0 --port 8001
# frontend用のサーバーを起動
python -m http.server 5500
```
