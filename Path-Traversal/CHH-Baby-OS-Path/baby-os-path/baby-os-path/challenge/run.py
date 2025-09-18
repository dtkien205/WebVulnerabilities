import sys
import os

from fastapi.responses import JSONResponse, FileResponse
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

from settings import DEBUG, LOG_LEVEL, VERSION


# Setup logger
logger.remove()
logger.add(sys.stdout, level=LOG_LEVEL)

app = FastAPI(
    debug=DEBUG,
    version=VERSION,
    title="Content Creator - API",
    description="Content Creator - API",
    contact={"name": "Creator", "email": "creator@cookiearena.org"},
)


# Index
@app.get("/")
async def root():
    return {
        "title": "Content Creator - API",
        "files": {
            "post-20221123-1800": "post-20221123-1800.txt",
            "post-20221123-1500": "post-20221123-1500.txt",
            "robot": "robots.txt",
            "index": "index.html",
        }}


# Healthcheck endpoint
@ app.get("/health")
def health():
    return "OK"


# Serve static files
@ app.get("/{px:path}")
def serve_frontend(px: str):
    root_dir = "statics"
    file_path = os.path.join(root_dir, px)

    if "etc" in file_path:
        return "Deny"

    if (os.path.exists(file_path)) and os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse(os.path.join(root_dir, "index.html"))


# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
