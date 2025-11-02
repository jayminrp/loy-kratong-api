from sqlalchemy.orm import Session
from . import models, schemas

def create_kratong(db: Session, kratong_in: schemas.KratongCreate):
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
    return db_item

def list_kratongs(db: Session):
    # ดึงทั้งหมด เรียงจากใหม่ไปเก่า (created_at ใหญ่สุดก่อน)
    return (
        db.query(models.Kratong)
        .order_by(models.Kratong.created_at.desc())
        .all()
    )
