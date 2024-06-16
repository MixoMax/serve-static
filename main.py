from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import uvicorn

import os

os.chdir("..")

print(os.getcwd())


port = 1950
address = "0.0.0.0"
domain_prefix = "https://static.linus-minus-sinus.org/"

app = FastAPI()

_all_f = os.listdir(".")
dirs = [f for f in _all_f if os.path.isdir(f) and not f.startswith(".") and not f.startswith("serve-")]

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

@app.get("/get_files")
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



@app.get("/{file_path:path}")
async def read_file(file_path: str) -> FileResponse:
    if not is_valid_file(file_path):
        return JSONResponse(content={"error": "Invalid file path"}, status_code=400)
    
    return FileResponse(file_path)

if __name__ == "__main__":
    uvicorn.run(app, host=address, port=port)