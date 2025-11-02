from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import schemas

from . import database, models, crud

app = FastAPI(
    title="Loy Kratong API",
    description="API สำหรับลอยกระทงออนไลน์",
    version="1.0.0",
)

# เปิด CORS ให้ frontend เรียกได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://loy-kratong-tse.onrender.com", "http://localhost:5173", "http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# สร้างตารางใน DB ถ้ายังไม่มี
models.Base.metadata.create_all(bind=database.engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/kratong", response_model=schemas.KratongList)
def get_all_kratongs(db: Session = Depends(database.get_db)):
    items = crud.list_kratongs(db)
    # map field name ให้ตรงกับ schema KratongOut
    # (เพราะใน DB เราเก็บ owner_name ไม่ใช่ ownerName)
    result = [
        schemas.KratongOut(
            id=i.id,
            ownerName=i.owner_name,
            wishText=i.wish_text,
            shapeImg=i.shape_img,
            createdAt=i.created_at,
        )
        for i in items
    ]
    return {"kratongs": result}


@app.post("/kratong", response_model=schemas.KratongOut)
def create_kratong(kratong_in: schemas.KratongCreate, db: Session = Depends(database.get_db)):
    saved = crud.create_kratong(db, kratong_in)
    return schemas.KratongOut(
        id=saved.id,
        ownerName=saved.owner_name,
        wishText=saved.wish_text,
        shapeImg=saved.shape_img,
        createdAt=saved.created_at,
    )
