from fastapi import FastAPI,File,UploadFile
from pydantic import BaseModel
from typing import Optional #patch
from typing import List
from fastapi.responses import FileResponse
from pathlib import Path
import os

app = FastAPI()

UPLOAD_DIR = Path.cwd() / "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload-multiple")
async def upload_files(files: list[UploadFile] = File(...)):
    contents = []
    for file in files:
        content = await file.read()
        contents.append({"filename": file.filename, "content_type": file.content_type, "content": content})
    return contents

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "filename": file.filename,
        "saved_path": file_path
    }

memo_db = [{"id":1, "title":"빅나티 변기에 넣고 내려", "content":"양홍원한테 손절당함"}]

class MemoUpdate(BaseModel): # patch
    title: Optional[str] = None
    content: Optional[str] = None

class Item(BaseModel):
    name: str
    grade: int

class Memo(BaseModel):
    title: str
    content: str

@app.get("/memos")
async def read_memos():
    return memo_db

@app.post("/memos")
async def create_memo(memo: Memo):
    new_id = len(memo_db) + 1
    new_memo = {"id": new_id, "title": memo.title, "content": memo.content}
    memo_db.append(new_memo)
    return {"new_memo": new_memo}


@app.put("/memos/{memo_id}")
async def update_memo(memo_id: int, memo: Memo):
    for item in memo_db:
        if item["id"] == memo_id:
            item["title"] = memo.title
            item["content"] = memo.content
            return {"updated_memo": item}
    return {"error": "Memo not found"}

@app.patch("/memos/{memo_id}")
async def patch_memo(memo_id: int, memo: MemoUpdate):
    for item in memo_db:
        if item["id"] == memo_id:
            if memo.title: item["title"] = memo.title
            if memo.content: item["content"] = memo.content
            return item
    return {"error": "메모를 찾을 수 없습니다."}


@app.delete("/memos/{memo_id}")
async def delete_memo(memo_id: int):
    global memo_db
    memo_db = [item for item in memo_db if item["id"] != memo_id]
    return {"message": f"{memo_id}번 삭제 완료"}


@app.get("/users/{user_id}")
async def test_path(user_id: int):
    return {"user_id": user_id}

@app.get("/users")
async def test_query(user_id: int, age: int):
    return {"user_id": user_id, "age": age}

@app.post("/post")
async def test_post(item: Item):
    return {"item_info": item.grade}

@app.get("/download/{filename}")
async def download_file(filename: str):

    file_path = UPLOAD_DIR / filename

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
