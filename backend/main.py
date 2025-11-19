from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageFilter
import io
from typing import Callable

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

router = APIRouter(prefix="/process")

async def process_image(file: UploadFile, process_func: Callable[[Image.Image], Image.Image]) -> StreamingResponse:
    """画像処理の共通ロジック"""
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    
    # RGBAやパレットモード(P)などの場合、フィルタ処理でエラーになることがあるためRGBに変換
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")
    
    # 画像処理を実行
    processed_image = process_func(image)
    
    buf = io.BytesIO()
    processed_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/")
def read_root():
    return {"message": "画像加工APIサーバーは正常に稼働しています！"}

@router.post("/gray")
async def create_gray_image(file: UploadFile = File(...)):
    """グレースケール画像を生成します"""
    return await process_image(file, lambda img: img.convert("L"))

@router.post("/edge")
async def create_edge_image(file: UploadFile = File(...)):
    """画像の輪郭を抽出します"""
    return await process_image(file, lambda img: img.filter(ImageFilter.FIND_EDGES))

@router.post("/blur")
async def create_blur_image(file: UploadFile = File(...)):
    """画像をぼかします"""
    return await process_image(file, lambda img: img.filter(ImageFilter.GaussianBlur(radius=5)))

app.include_router(router)
