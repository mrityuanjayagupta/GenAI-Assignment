from docx import Document
from fastapi import FastAPI, HTTPException, UploadFile
import io

from main import run_code_generator

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    if file.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        raise HTTPException(400, detail="Invalid document type")
    contents = await file.read()

    doc = Document(io.BytesIO(contents))
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    text = "\n".join(full_text)
    run_code_generator(text)
    return {"zip_path": "./final_project"}