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
try:
    models.Base.metadata.create_all(bind=database.engine)
    print("✓ Database tables created/verified successfully")
except Exception as e:
    print(f"✗ Error creating database tables: {e}")

# Test database connection on startup
@app.on_event("startup")
async def startup_event():
    try:
        from .database import SessionLocal
        db = SessionLocal()
        try:
            # Test query to verify database connection
            from . import crud
            kratong_count = len(crud.list_kratongs(db))
            print(f"✓ Database connected successfully. Found {kratong_count} kratongs in database.")
        finally:
            db.close()
    except Exception as e:
        print(f"✗ Database connection error: {e}")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/debug/db-info")
def debug_db_info(db: Session = Depends(database.get_db)):
    """Debug endpoint to check database connection and data"""
    try:
        from . import crud
        kratongs = crud.list_kratongs(db)
        import os
        db_url = os.environ.get("DATABASE_URL", "NOT SET")
        # Mask password
        if "@" in db_url:
            parts = db_url.split("@")
            if len(parts) == 2 and ":" in parts[0]:
                user = parts[0].split("://")[-1].split(":")[0]
                host_db = parts[1]
                db_url = db_url.split("://")[0] + "://" + user + ":***@" + host_db
        
        return {
            "status": "connected",
            "database_url_masked": db_url,
            "total_kratongs": len(kratongs),
            "kratongs": [
                {
                    "id": k.id,
                    "ownerName": k.owner_name,
                    "wishText": k.wish_text[:50] + "..." if len(k.wish_text) > 50 else k.wish_text,
                    "createdAt": k.created_at
                }
                for k in kratongs[:10]  # Show first 10
            ]
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/kratong", response_model=schemas.KratongList)
def get_all_kratongs(db: Session = Depends(database.get_db)):
    try:
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
        print(f"✓ Retrieved {len(result)} kratongs from database")
        return {"kratongs": result}
    except Exception as e:
        print(f"✗ Error retrieving kratongs: {e}")
        raise


@app.post("/kratong", response_model=schemas.KratongOut)
def create_kratong(kratong_in: schemas.KratongCreate, db: Session = Depends(database.get_db)):
    try:
        saved = crud.create_kratong(db, kratong_in)
        print(f"✓ Created new kratong: ID={saved.id}, Owner={saved.owner_name}")
        return schemas.KratongOut(
            id=saved.id,
            ownerName=saved.owner_name,
            wishText=saved.wish_text,
            shapeImg=saved.shape_img,
            createdAt=saved.created_at,
        )
    except Exception as e:
        print(f"✗ Error creating kratong: {e}")
        raise

@app.delete("/kratong/{kratong_id}")
def delete_kratong(kratong_id: str, db: Session = Depends(database.get_db)):
    """Delete a kratong by ID"""
    try:
        deleted = crud.delete_kratong(db, kratong_id)
        if deleted:
            return {"message": f"Kratong {kratong_id} deleted successfully", "success": True}
        else:
            return {"message": f"Kratong {kratong_id} not found", "success": False}
    except Exception as e:
        print(f"✗ Error deleting kratong: {e}")
        raise