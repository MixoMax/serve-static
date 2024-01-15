from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import uvicorn
import hashlib
import json
import datetime
import os

app = FastAPI()

#static file server

@app.get("/static/{file_name}")
async def static_file(file_name: str) -> FileResponse:
    file_path = f"./static/{file_name}"
    file_path = os.path.abspath(file_path)
    
    #check if file extension is allowed
    not_allowd = ["token"]
    if file_name.split(".")[-1] in not_allowd:
        return JSONResponse({"message": "file extension not allowed"}, status_code=403)
    
    #check if file exists
    if not os.path.exists(file_path):
        return JSONResponse({"message": "file not found"}, status_code=404)
    
    #return file
    return FileResponse(file_path)



# Sources UI for presentation and other source quoting
# sources are stored in a json file

class SourceEntry:
    tag: str
    name: str
    link: str
    date: str
    
    author: str | None
    author_link: str | None
    
    description: str | None
    
    def __init__(self):
        self.tag = ""
        self.name = ""
        self.link = ""
        self.date = ""
        
        self.author = None
        self.author_link = None
        
        self.description = None
    
    def from_json(self, data: dict):
        self.tag = data["tag"]
        self.name = data["name"]
        self.link = data["link"]
        self.date = data["date"]
        
        self.author = data.get("author", None)
        self.author_link = data.get("author_link", None)
        
        self.description = data.get("description", None)
        
    def to_json(self) -> dict:
        return {
            "tag": self.tag,
            "name": self.name,
            "link": self.link,
            "date": self.date,
            
            "author": self.author,
            "author_link": self.author_link,
            
            "description": self.description
        }
    
class Sources:
    entries: list[SourceEntry]
    last_update: str
    hashed_password: str
    project_name: str
    
    authors: list[str]
    
    def __init__(self):
        self.entries = []
        self.last_update = ""
        self.hashed_password = ""
        self.project_name = ""
        
        self.authors = []
    
    def from_json(self, data: dict):
        self.last_update = data["last_update"]
        self.hashed_password = data["hashed_password"]
        self.project_name = data["project_name"]
        
        self.authors = data["authors"]
        
        for entry in data["entries"]:
            source_entry = SourceEntry()
            source_entry.from_json(entry)
            self.entries.append(source_entry)
            
        
    def to_json(self) -> dict:
        entries = []
        for entry in self.entries:
            entries.append(entry.to_json())
        
        return {
            "last_update": self.last_update,
            "hashed_password": self.hashed_password,
            "project_name": self.project_name,
            
            "authors": self.authors,
            
            "entries": entries
        }
    

@app.get("/sources/json/{file_path}")
async def sources_json(file_path: str) -> JSONResponse:
    file_path = f"./sources/{file_path}"
    file_path = os.path.abspath(file_path)
    
    #check if file exists
    if not os.path.exists(file_path):
        return JSONResponse({"message": "file not found"}, status_code=404)
    
    #load file
    with open(file_path, "r") as file:
        data = json.load(file)
    
    #create sources object
    sources = Sources()
    sources.from_json(data)
    
    #return json
    return JSONResponse(sources.to_json())


@app.post("/sources/{file_path}/add")
async def add_source(file_path: str, request: Request) -> JSONResponse:
    file_path = f"./sources/{file_path}"
    file_path = os.path.abspath(file_path)
    
    #check if file exists
    if not os.path.exists(file_path):
        return JSONResponse({"message": "file not found"}, status_code=404)
    
    #load file
    with open(file_path, "r") as file:
        data = json.load(file)
    
    #create sources object
    sources = Sources()
    sources.from_json(data)
    
    #check if password is correct
    password = request.headers.get("password", "")
    if not hashlib.sha256(password.encode()).hexdigest() == sources.hashed_password:
        return JSONResponse({"message": "wrong password"}, status_code=403)
    
    #get data from request
    data = await request.json()
    
    #create new source entry
    source_entry = SourceEntry()
    source_entry.from_json(data)
    
    #add source entry to sources
    sources.entries.append(source_entry)
    
    #save sources
    with open(file_path, "w") as file:
        json.dump(sources.to_json(), file, indent=4)
    
    #return json
    return JSONResponse(sources.to_json())


@app.get("/sources/html/{file_path}")
async def sources_html(file_path: str) -> HTMLResponse:
    with open("./sources.html", "r") as file:
        html = file.read()
    
    json_file_path = f"/sources/json/{file_path}"
    
    html = html.replace("JSON_FILE_PATH_PLACEHOLDER", json_file_path)
    
    return HTMLResponse(html)



#main page
@app.get("/")
async def root():
    return {"message": "linushorn.dev static file server"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7995)