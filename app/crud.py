from sqlalchemy.orm import Session
from . import models, schemas

def create_kratong(db: Session, kratong_in: schemas.KratongCreate):
    # Check if kratong with same ID already exists
    existing = db.query(models.Kratong).filter(models.Kratong.id == kratong_in.id).first()
    if existing:
        print(f"⚠️  Kratong with ID {kratong_in.id} already exists, skipping duplicate")
        return existing
    
    # Check if we need to delete the oldest kratong (when count > 10)
    kratong_count = count_kratongs(db)
    if kratong_count >= 10:
        oldest_kratong = get_oldest_kratong(db)
        if oldest_kratong:
            delete_kratong(db, oldest_kratong.id)
            print(f"✓ Deleted oldest kratong (ID={oldest_kratong.id}) to maintain limit of 10")
    
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

def delete_kratong(db: Session, kratong_id: str):
    """Delete a kratong by ID"""
    kratong = db.query(models.Kratong).filter(models.Kratong.id == kratong_id).first()
    if kratong:
        db.delete(kratong)
        db.commit()
        print(f"✓ Deleted kratong: ID={kratong_id}")
        return True
    return False

def get_oldest_kratong(db: Session):
    """Get the oldest kratong (lowest created_at)"""
    return (
        db.query(models.Kratong)
        .order_by(models.Kratong.created_at.asc())
        .first()
    )

def count_kratongs(db: Session):
    """Count total number of kratongs"""
    return db.query(models.Kratong).count()