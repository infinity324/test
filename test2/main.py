# main.py
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.orm import Session
from models import User, UserCreate, UserUpdate, Base, engine
from typing import List
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库会话依赖


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


# 创建表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="用户管理API", version="1.0.0")

# 自定义CRUD路由


class UserCRUDRouter(SQLAlchemyCRUDRouter):
    def _get_all(self, *args, **kwargs):
        """重写获取所有数据方法，增加分页"""
        db = kwargs.get("db")
        skip = kwargs.get("skip", 0)
        limit = kwargs.get("limit", 100)
        return db.query(self.db_model).offset(skip).limit(limit).all()


router = UserCRUDRouter(
    schema=User,
    db_model=User,
    db=get_db,
    create_schema=UserCreate,
    update_schema=UserUpdate,
    prefix="users",
    tags=["Users"]
)

# 添加自定义路由


@router.get("/search/", response_model=List[User])
def search_users(
    name: str = Query(None, min_length=2),
    email: str = Query(None),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """用户搜索接口"""
    query = db.query(User)
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()


app.include_router(router)

# 健康检查端点


@app.get("/health")
def health_check():
    return {"status": "healthy"}
