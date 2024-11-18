import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from util.environment import Environment
from util.error_reporter import ErrorReporter

# ログ
logging.basicConfig(level=logging.INFO)
if Environment.is_dev():
    logging.basicConfig(level=logging.DEBUG)

# アプリ設定
app = FastAPI(
    title="Scraping API",
    version="0.0.1",
)

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)


handler = Mangum(app, lifespan="off")


# ミドルウェア
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):  # noqa: ANN001, ANN201
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = int((time.time() - start_time) * 1000)  # 整数値のミリ秒
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    except:
        ErrorReporter().execute()
        raise
