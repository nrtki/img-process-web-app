## 📦 Usage (使い方)


### Prerequisites (事前準備)
- Python 3.8 以上
- Git

### 1. Clone & Setup (環境構築)
リポジトリをクローンし、プロジェクトディレクトリへ移動します。

```bash
git clone https://github.com/nrtki/image-processing-app.git
cd image-processing-app
```
### 2. 仮想環境の作成と有効化 (Optional)
```bash
python -m venv .venv
```
#### Windows (PowerShell) の場合:
```bash
.venv\Scripts\activate
```
#### Mac/Linux の場合:
```bash
source .venv/bin/activate
```
### 3. ライブラリのインストール
```bash
pip install -r requirement.txt
```
### 4. backendサーバ起動
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```
### 5.frontend用のサーバーを起動
```bash
python -m http.server :5500
```
