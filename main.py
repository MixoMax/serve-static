from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import uvicorn
import hashlib
import json
import datetime

app = FastAPI()

#static file server

def verify_password(p: str) -> bool:
    with open("./password.token", "r") as f:
        token = f.read()
    
    p_hash = hashlib.sha256(p.encode()).hexdigest()
    
    if p_hash == token:
        return True
    else:
        return False

@app.get("/static/{file_name}")
async def static_file(file_name: str):
    if file_name.endswith(".token"):
        return JSONResponse(content={"status": "no access"}, status_code=403)
    return FileResponse(f"./{file_name}")

@app.get("/quellen/{json_name}")
async def quellen(json_name: str):
    with open("./quellen_json.html", "r") as f:
        html = f.read()
    
    html = html.replace("json_url_placeholder", f"/static/{json_name}")
    
    return HTMLResponse(content=html, status_code=200)

@app.get("/quellen_ui/add_form")
async def quellen_add_form(p:str):
    #p: password
    if verify_password(p) == False:
        return JSONResponse(content={"status": "wrong password"}, status_code=403)
    
    with open("./quellen_add_form.html", "r") as f:
        html = f.read()
    
    return HTMLResponse(content=html, status_code=200)

@app.post("/quellen_api/add")
async def quellen_add(request: Request) -> JSONResponse:
    #request: {p, json_fp, tag, name, link, *author, *date, *description}
    
    print(request.query_params)
    
    if verify_password(request.query_params["p"]) == False:
        return JSONResponse(content={"status": "wrong password"}, status_code=403)
    
    json_fp = request.query_params["json_fp"]

    necessary = ["tag", "name", "link"]
    optional = ["author", "date", "description"]
    
    for n in necessary:
        if n not in request.query_params:
            return JSONResponse(content={"status": f"missing {n}"}, status_code=400)
    
    for o in optional:
        if o not in request.query_params or o == "":
            
            if o == "date":
                request.query_params[o] = datetime.datetime.now().strftime("YYYY-MM-DD")
            else:
                request.query_params[o] = ""
    
    with open(json_fp, "r") as f:
        data = json.load(f)
    
    data.append({
        "tag": request.query_params["tag"],
        "name": request.query_params["name"],
        "link": request.query_params["link"],
        "author": request.query_params["author"],
        "date": request.query_params["date"],
        "description": request.query_params["description"]
    })
    
    with open(json_fp, "w") as f:
        json.dump(data, f, indent=4)
    
    return JSONResponse(content={"status": "success"}, status_code=200)
    


#main page
@app.get("/")
async def root():
    return {"message": "linushorn.dev static file server"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7995)