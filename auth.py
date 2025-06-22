import jwt
import time
from models.user import User
from database import SessionLocal
from hashlib import sha256

SECRET_KEY = 'mysecretkey'
ALGORITHM = 'HS256'
EXPIRE_SECONDS = 3600

def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()

def create_jwt_token(user_id: int, role: str):
    payload = {
        'sub': str(user_id),
        'role': role,
        'exp': time.time() + EXPIRE_SECONDS
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str):
    print(token)
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as e:
        print(e)
        return None
    except jwt.InvalidTokenError as e2:
        print(e2)
        return None

def verify_user(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and user.password == hash_password(password):
        return user
    return None

def register_user(username: str, password: str) -> bool:
    db = SessionLocal()
    if db.query(User).filter(User.username == username).first():
        db.close()
        return False
    user = User(username=username, password=hash_password(password), role='viewer')
    db.add(user)
    db.commit()
    db.close()
    return True
