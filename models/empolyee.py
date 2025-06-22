from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum
import time
import enum
from database import Base

class GenderEnum(enum.Enum):
    MALE = '男'
    FEMALE = '女'
    OTHER = '其他'

class EducationEnum(enum.Enum):
    PRIMARY = '小学'
    MIDDLE = '初中'
    HIGH = '高中'
    BACHELOR = '本科'
    MASTER = '硕士'
    DOCTOR = '博士'
    OTHER = '其他'

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    name = Column(String(100), nullable=False, comment='姓名')
    gender = Column(String(10), comment='性别')
    age = Column(Integer, comment='年龄')
    department = Column(String(100), comment='部门')
    position = Column(String(100), comment='职位')
    salary = Column(Float, comment='薪资')
    hire_date = Column(Date, comment='入职日期')
    email = Column(String(100), unique=True, comment='邮箱')
    phone = Column(String(20), comment='联系电话')
    address = Column(String(255), comment='家庭住址')
    education = Column(String(50), comment='学历')
    performance_rating = Column(Float, comment='绩效评分')
    created_at = Column(DateTime, default=time.time(), comment='创建时间')
    