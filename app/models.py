from sqlalchemy import Column, String, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from .database import Base

# ตารางเก็บข้อมูลกระทง
class Kratong(Base):
    __tablename__ = "kratongs"

    id = Column(String, primary_key=True, index=True)       # เราจะส่งเป็น string จาก frontend (Date.now().toString())
    owner_name = Column(String(100), nullable=False)        # ชื่อคนลอย
    wish_text = Column(Text, nullable=False)                # คำอวยพร
    shape_img = Column(String(255), nullable=False)         # path รูปกระทง เช่น "/kratong1.png"
    created_at = Column(BigInteger, nullable=False)         # timestamp ms จาก frontend
    server_time = Column(DateTime(timezone=True), server_default=func.now())  # timestamp ฝั่งเซิร์ฟเวอร์ (optional debug)
