from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn

app = FastAPI()

#static file server

@app.get("/static/{file_name}")
async def static_file(file_name: str):
    return FileResponse(f"./{file_name}")

@app.get("/quellen/{json_name}")
async def quellen(json_name: str):
    with open("./quellen_json.html", "r") as f:
        html = f.read()
    
    html = html.replace("json_url_placeholder", f"/static/{json_name}")
    
    return HTMLResponse(content=html, status_code=200)

#main page
@app.get("/")
async def root():
    return {"message": "linushorn.dev static file server"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7995)