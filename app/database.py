import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# โหลด .env แล้วบังคับให้ทับทุกค่าเก่า
load_dotenv(override=True)

raw_url = os.environ.get("DATABASE_URL")
if not raw_url:
    raise RuntimeError("DATABASE_URL is not set. Please configure environment variable.")

DATABASE_URL = raw_url.strip().strip('"').strip("'")

# แสดง DATABASE_URL ที่ได้มา (ซ่อน password)
masked_url = DATABASE_URL
if "@" in masked_url:
    parts = masked_url.split("@")
    if len(parts) == 2:
        user_pass = parts[0].split("://")[-1]
        if ":" in user_pass:
            user = user_pass.split(":")[0]
            masked_url = masked_url.split("://")[0] + "://" + user + ":***@" + parts[1]
print(">>> DATABASE_URL (masked):", masked_url)

# force postgres:// -> postgresql+psycopg:// (for psycopg3)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    # If already postgresql://, replace with postgresql+psycopg:// for psycopg3
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# เช็คว่าเป็น internal หรือ external URL
if "@dpg-" in DATABASE_URL and ".render.com" not in DATABASE_URL:
    print("⚠️  WARNING: Using INTERNAL database URL. Make sure API and DB are in same Render network.")
    print("   If you need external access, use EXTERNAL_DATABASE_URL or add .render.com to hostname")
elif ".render.com" in DATABASE_URL:
    print("✓ Using EXTERNAL database URL (accessible from anywhere)")
else:
    print("ℹ️  Using custom database URL")

# 🔥 DEBUG PRINT - เช็คว่าเราใช้ URL อะไรจริงตอน runtime (masked version)
print(">>> Final DATABASE_URL format: postgresql+psycopg://***@[host]/[database]")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
