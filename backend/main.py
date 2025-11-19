from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5500",  # VSCode Live Serverのデフォルト
    "http://127.0.0.1:5500", # VSCode Live Serverの別のアドレス
    "null" # ローカルファイルを直接開いた場合（file://）
]

# CORS設定（フロントエンドとバックエンドの通信を許可する設定）
# 実務では特定のドメインのみ許可しますが、開発用なので全許可にしています
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "画像加工APIサーバーは正常に稼働しています！"}

@app.post("/process/")
async def process_image(file: UploadFile = File(...)):
    """
    アップロードされた画像をグレースケールに変換して返すAPI
    """
    # 1. アップロードされたファイルを読み込む
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))

    # 2. 画像処理（ここでOpenCVなどを使えば複雑な加工も可能）
    # 今回はシンプルに「白黒（グレースケール）」変換
    processed_image = image.convert("L")

    # 3. 加工した画像をメモリ上のバッファに保存（ディスクには保存しない）
    buf = io.BytesIO()
    processed_image.save(buf, format="PNG")
    buf.seek(0)

    # 4. 画像データとしてレスポンスを返す
    return StreamingResponse(buf, media_type="image/png")