from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

#static file server

@app.get("/static/{file_name}")
async def static_file(file_name: str):
    return FileResponse(f"./{file_name}")

#main page
@app.get("/")
async def root():
    return {"message": "linushorn.dev static file server"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7995)