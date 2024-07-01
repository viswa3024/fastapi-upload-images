# server.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_location = UPLOAD_DIR / file.filename
    with file_location.open("wb") as f:
        f.write(await file.read())
    return {"url": f"/uploads/{file.filename}"}

@app.get("/uploads/{filename}")
async def get_image(filename: str):
    file_location = UPLOAD_DIR / filename
    if file_location.exists():
        return FileResponse(file_location)
    return {"error": "File not found"}

@app.get("/images")
async def list_images():
    images = [f"/uploads/{f.name}" for f in UPLOAD_DIR.iterdir() if f.is_file()]
    return {"images": images}

@app.delete("/delete/{filename}")
async def delete_image(filename: str):
    file_location = UPLOAD_DIR / filename
    if file_location.exists():
        os.remove(file_location)
        return {"message": f"{filename} has been deleted"}
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.delete("/delete-all")
async def delete_all_images():
    deleted_files = []
    for file in UPLOAD_DIR.iterdir():
        if file.is_file():
            os.remove(file)
            deleted_files.append(file.name)
    return {"message": "All files have been deleted", "deleted_files": deleted_files}


@app.delete("/delete-all-images")
async def delete_all_images():
    deleted_files = []
    for file in UPLOAD_DIR.iterdir():
        if file.is_file() and file.name != ".gitkeep":
            os.remove(file)
            deleted_files.append(file.name)
    return {"message": "All files have been deleted except .gitkeep", "deleted_files": deleted_files}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
