import pymysql
from sqlalchemy import create_engine
from models.user import User
from database import Base
from sqlalchemy.orm import sessionmaker, declarative_base
from auth import hash_password
# 修改为你的数据库信息
DB_HOST = '192.168.50.234'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'Yagami'
DB_NAME = 'company_management'

# 1. 连接 MySQL 创建数据库（如果不存在）
connection = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = connection.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
connection.commit()
cursor.close()
connection.close()

# 2. 使用 SQLAlchemy 初始化表结构
DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

# Step 3: 创建默认 admin 用户（如果不存在）
ADMIN_USERNAME='admin'
ADMIN_PASSWORD='admin'
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()
admin_user = db.query(User).filter(User.username == ADMIN_USERNAME).first()
if not admin_user:
    user = User(
        username=ADMIN_USERNAME,
        password=hash_password(ADMIN_PASSWORD),
        role='admin'
    )
    db.add(user)
    db.commit()
    print(f'✅ 已创建默认 admin 用户：用户名 {ADMIN_USERNAME}，密码 {ADMIN_PASSWORD}')
else:
    print(f'ℹ️ 默认 admin 用户已存在：{ADMIN_USERNAME}')
db.close()

print("✅ 数据库和用户表已初始化完成")
