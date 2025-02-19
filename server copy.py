# server.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
