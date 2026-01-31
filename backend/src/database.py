# backend/src/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 数据库连接URL
# 先用SQLite（本地文件，无需安装数据库服务器）
SQLALCHEMY_DATABASE_URL = "sqlite:///./tomato.db"
# 后期可轻松换为PostgreSQL：
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/tomato"

# 2. 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # 仅SQLite需要
)

# 3. 创建数据库会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 创建基类，用于定义数据模型
Base = declarative_base()

# 依赖项函数，用于在API路由中获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()