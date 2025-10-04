# file_upload_endpoint.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os

app = FastAPI(title="File Upload API")

# Directory to save uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file to the server.
    
    Args:
        file (UploadFile): File to upload.
        
    Returns:
        JSONResponse: Success message with filename.
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(content={"message": f"File '{file.filename}' uploaded successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@app.get("/")
def read_root():
    return {"message": "Welcome to File Upload API"}
    

if __name__ == "__main__":
    import uvicorn
    # ⚠️ Bandit warning about binding to 0.0.0.0 is expected for dev purposes
    uvicorn.run(app, host="0.0.0.0", port=8000)

