from fastapi import FastAPI, UploadFile, File,APIRouter
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageFilter
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
router = APIRouter(prefix="/process")
app.include_router(router)
@app.get("/")
def read_root():
    return {"message": "画像加工APIサーバーは正常に稼働しています！"}


@app.post("/process/gray")
async def create_gray_image(file: UploadFile = File(...)):
    """グレースケール画像を生成します"""
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    processed_image = image.convert("L")
    buf = io.BytesIO()
    processed_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/process/edge")
async def create_edge_image(file: UploadFile = File(...)):
    """画像の輪郭を抽出します"""
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    processed_image = image.filter(ImageFilter.FIND_EDGES)
    buf = io.BytesIO()
    processed_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/process/blur")
async def create_edge_image(file: UploadFile = File(...)):
    """画像の輪郭を抽出します"""
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    processed_image = image.filter(ImageFilter.GaussianBlur(radius=5))
    buf = io.BytesIO()
    processed_image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
