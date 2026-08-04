import os
from collections.abc import Generator
from pathlib import Path


from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,Session, sessionmaker


# backend目录的绝对路径
BASE_DIR = Path(__file__).resolve().parent

# 明确加载backend/.env文件
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. "
        "Please check backend/.env."
    )

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# 创建数据库会话工厂
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


# 所有 SQLAlchemy ORM 模型的基类
class Base(DeclarativeBase):
    pass

# 为每次 FastAPI 请求提供独立的数据库会话
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()