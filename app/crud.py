from sqlalchemy.orm import Session
from . import models, schemas

def create_kratong(db: Session, kratong_in: schemas.KratongCreate):
    # Check if kratong with same ID already exists
    existing = db.query(models.Kratong).filter(models.Kratong.id == kratong_in.id).first()
    if existing:
        print(f"⚠️  Kratong with ID {kratong_in.id} already exists, skipping duplicate")
        return existing
    
    db_item = models.Kratong(
        id=kratong_in.id,
        owner_name=kratong_in.ownerName,
        wish_text=kratong_in.wishText,
        shape_img=kratong_in.shapeImg,
        created_at=kratong_in.createdAt,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    print(f"✓ Saved kratong to database: ID={db_item.id}")
    return db_item

def list_kratongs(db: Session):
    # ดึงทั้งหมด เรียงจากใหม่ไปเก่า (created_at ใหญ่สุดก่อน)
    return (
        db.query(models.Kratong)
        .order_by(models.Kratong.created_at.desc())
        .all()
    )
