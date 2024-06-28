from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
import uvicorn

import os

os.chdir("..")

print(os.getcwd())


port = 1950
address = "0.0.0.0"
domain_prefix = "https://static.linus-minus-sinus.org/"

app = FastAPI()

_all_f = os.listdir(".")

banned_dirs = ["tokens", "serve-static"]

dirs = [f for f in _all_f if os.path.isdir(f) and not f.startswith(".") and not f in banned_dirs]

print(dirs)

def is_valid_file(file_path: str) -> bool:
    is_in_dir = False
    for d in dirs:
        if file_path.startswith(d):
            is_in_dir = True
            break
    
    if ".." in file_path or not is_in_dir:
        return False
    elif not os.path.exists(file_path):
        return False
    
    return True

@app.get("/get_files.json")
async def get_files() -> JSONResponse:
    file_urls = []
    for root, dirs, files in os.walk("."):
        for f in files:
            fp = os.path.join(root, f).replace("\\", "/")

            if fp.startswith("./"):
                fp = fp[2:]

            url = f"{domain_prefix}{fp}"

            if is_valid_file(fp):
                file_urls.append(url)
    
    return JSONResponse(content={"files": file_urls})

@app.get("sitemap.xml")
async def get_sitemap() -> FileResponse:
    file_urls = []
    for root, dirs, files in os.walk("."):
        for f in files:
            fp = os.path.join(root, f).replace("\\", "/")

            if fp.startswith("./"):
                fp = fp[2:]

            url = f"{domain_prefix}{fp}"

            if is_valid_file(fp):
                file_urls.append(url)
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {'\n'.join([f'<url><loc>{url}</loc></url>' for url in file_urls])}
    </urlset>"""

    return HTMLResponse(content=sitemap)

@app.get("/")
async def read_root() -> FileResponse:
    return FileResponse("./serve-static/index.html")

@app.get("/robots.txt")
async def read_robots() -> FileResponse:
    return FileResponse("./serve-static/robots.txt")





@app.get("/{file_path:path}")
async def read_file(file_path: str) -> FileResponse:
    if not is_valid_file(file_path):
        return JSONResponse(content={"error": "Invalid file path"}, status_code=400)
    
    media_types = {
        # text formats
        "txt": "text/plain",
        "html": "text/html",
        "css": "text/css",
        "js": "text/javascript",
        "json": "application/json",
        "md": "text/markdown",
        "xml": "application/xml",

        # image formats
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "bmp": "image/bmp",
        "webp": "image/webp",
        "ico": "image/x-icon",
        "svg": "image/svg+xml",

        # audio formats
        "mp3": "audio/mpeg",
        "wav": "audio/wav",
        "ogg": "audio/ogg",
        "flac": "audio/flac",

        # video formats
        "mp4": "video/mp4",
        "webm": "video/webm",
        "ogg": "video/ogg",
        "mkv": "video/x-matroska",
        "avi": "video/x-msvideo",
        "mov": "video/quicktime",

        # document formats
        "pdf": "application/pdf",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "ppt": "application/vnd.ms-powerpoint",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "csv": "text/csv",
        "rtf": "application/rtf",
        "odt": "application/vnd.oasis.opendocument.text",
        "ods": "application/vnd.oasis.opendocument.spreadsheet",
        "odp": "application/vnd.oasis.opendocument.presentation",
        
        # archive formats
        "zip": "application/zip",
        "rar": "application/x-rar-compressed",
        "7z": "application/x-7z-compressed",
        "tar": "application/x-tar",
        "gz": "application/gzip",
        "bz2": "application/x-bzip2",
    }

    file_ext = file_path.split(".")[-1]

    if file_ext in media_types:
        media_type = media_types[file_ext]
    else:
        media_type = "application/octet-stream"


    return FileResponse(file_path, media_type=media_type)

if __name__ == "__main__":
    uvicorn.run(app, host=address, port=port)