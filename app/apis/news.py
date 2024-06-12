import math
from logging import getLogger
from typing import Annotated

from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from schemas.news import NewsListResponseBody, NewsUpdateRequestBody, NewsUpdateResponseBody, \
                            NewsDetailResponseBody, NewsCreateRequestBody, NewsCreateResponseBody,\
                            NewsCategoryUpdateRequestBody, NewsCategoryUpdateResponseBody,\
                            NewsCategoryRequestBody, NewsCategoryResponseBody, NewsCategoryListResponseBody,\
                            PublishedNewsListResponseBody
from cruds import news as news_crud

logger = getLogger("uvicorn.app")

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/{news_id}/", response_model=NewsDetailResponseBody, status_code=status.HTTP_200_OK)
async def find_news_details(db: DbDependency, news_id: int = Path(gt=0)):
    """
    ニュース詳細取得

    Parameter
    -----------------------
    news_id: int
        取得するニュースのID

    Returns
    -----------------------
    dict
        id: int
            取得したニュースのID
        title: str
            ニュースのタイトル
        content: str
            ニュースの本文
        category: array
            categoey_id: int
                カテゴリのID
            category_name: str
                カテゴリのID
        published_at: str
            ニュースの公開日（ISO 8601形式）
    """

    news = news_crud.find_news_by_news_id(db, news_id)

    if not news:
        raise HTTPException(status_code=404, detail="The requested news article was not found.")

    news_category = news_crud.find_news_categories_by_category_id(db, news.news_category_id)
    di = {
        "category_id": news_category.id,
        "category_name": news_category.name
    }

    re_di = {
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "category": di,
        "published_at": news.published_at.isoformat()
    }

    return re_di

@router.get("", response_model=NewsListResponseBody, status_code=status.HTTP_200_OK)
async def find_news_list(db: DbDependency, page: int, limit: int):
    """
    ニュース一覧(管理者)取得

    Parameters
    -----------------------
    page: int
        表示するページ
    limit: int
        1ページに表示するニュース数

    Returns
    -----------------------
    news: array
        id: int
            取得したニュースのID
        title: str
            ニュースのタイトル
        category: array
            categoey_id: int
                カテゴリのID
            category_name: str
                カテゴリのID
        published_at: str
            ニュースの公開日（ISO 8601形式）
        is_published: bool
            ニュース公開状態
    """
    news = news_crud.find_news(db)

    li = []
    
    for data in news[(page-1)*limit : page*limit]:
        news_category = news_crud.find_news_categories_by_category_id(db, data.news_category_id)
        di = {
            "category_id": news_category.id,
            "category_name": news_category.name
        }

        re_di = {
            "id": data.id,
            "title": data.title,
            "category": di,
            "published_at": data.published_at.isoformat()
        }
        li.append(re_di)

    return {"news": li}

@router.patch("/{news_id}", response_model=NewsUpdateResponseBody, status_code=status.HTTP_200_OK)
async def update_news(db: DbDependency, news_id: int, param: NewsUpdateRequestBody):
    """
    ニュース更新

    Parameters
    -----------------------
    news_id: int
        編集したいニュースのid
    dict
        title: str
            更新するニュースのタイトル
        content: str
            更新するニュースの本文
        categoey_id: int
            カテゴリのID
        is_published: bool
            公開フラグ
        published_at: str
            公開日（ISO 8601形式）

    Returns
    -----------------------
    dict
        news_id: int
            更新されたニュースのID
        title: str
            更新されたニュースのタイトル
        content: str
            更新されたニュースの内容
        category: array
            category_id: int
                カテゴリのID
            category_name: str
                カテゴリの名前
        is_published: bool
            ニュースの公開フラグ
        published_at: str
            ニュースの公開日（ISO 8601形式）
        updated_at: str
            ニュースの更新日（ISO 8601形式）
    
    """
    logger.info(param)

    found_news = news_crud.find_news_by_news_id(db, news_id)

    if not found_news:
        raise HTTPException(status_code=404, detail="News not found.")

    try:
        news = news_crud.update_news_by_news_id(db, news_id, param.title, param.content, param.is_published, param.published_at)
        db.commit()

        news_category = news_crud.find_news_categories_by_category_id(db, news.news_category_id)
        di = {
            "category_id": news_category.id,
            "category_name": news_category.name
        }

        re_di = {
            "news_id": news.id,
            "title": news.title,
            "content": news.content,
            "category": di,
            "is_published": news.is_published,
            "published_at": news.published_at.isoformat(),
            "updated_at": news.updated_at.isoformat()
        }

        return re_di

    except Exception as e:
        logger.error(str(e)) 
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")  

@router.post("", response_model=NewsCreateResponseBody, status_code=status.HTTP_201_CREATED)
async def create_news(db: DbDependency, param: NewsCreateRequestBody):
    """
    ニュース作成
    Parameters
    -----------------------
    dict
        title: str
            作成するニュースのタイトル
        content: str
            作成するニュースの本文
        category_id: int
            カテゴリのID
        published_at: str
            公開日（ISO 8601形式）

    Returns
    -----------------------
    dict
        news_id: int
            ニュースのID
        title: str
            ニュースのタイトル
        content: str
            ニュースの本文
        category: array
            category_id: int
                カテゴリのID
            category_name: str
                カテゴリの名前
        is_published: bool
            ニュース公開状態
        published_at: str
            ニュースの公開日（ISO 8601形式）
        created_at: str
            ニュースの作成日（ISO 8601形式）
    """

    try:

        new_news = news_crud.create_news(db, param)
        db.commit()

        news_category = news_crud.find_news_categories_by_category_id(db, new_news.news_category_id)
        di = {
            "category_id": news_category.id,
            "category_name": news_category.name
        }

        re_di = {
            "id": new_news.id,
            "title": new_news.title,
            "content": new_news.content,
            "category": di,
            "is_published": new_news.is_published,
            "published_at": new_news.published_at.isoformat(),
            "created_at": new_news.created_at.isoformat()
        }

        return re_di
	
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")
    
@router.patch("/categories/{category_id}", response_model=NewsCategoryUpdateResponseBody, status_code=status.HTTP_200_OK)
async def update_news_category(db: DbDependency, category_id: int, param: NewsCategoryUpdateRequestBody):
    """
    ニュースカテゴリー更新
    Parameters
    -----------------------
    category_id: int
        更新するカテゴリのID
    dict
        name: str
            更新後のカテゴリ名
    Returns
    -----------------------
    message: str
        メッセージ
    category: array
        id: int
            カテゴリの一意識別子
        name: str
            カテゴリの名前
        created_at: str
            カテゴリの作成日
        updated_at: str
            カテゴリの更新日
    """

    try:
        news_category = news_crud.update_news_category_by_category_id(db, category_id, param)
        if not news_category:
            raise Exception("category not found.")
        db.commit()

        di = {
            "id": news_category.id,
            "name": news_category.name,
            "created_at": news_category.created_at.isoformat(),
            "updated_at": news_category.updated_at.isoformat(),
        }

        re_di = {
            "message": "Category updated successfully.",
            "category": di
        }

        return re_di

    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data or category not found.")

@router.post("/categories", response_model=NewsCategoryResponseBody, status_code=status.HTTP_201_CREATED)
async def create_news(db: DbDependency, param: NewsCategoryRequestBody):
    """
    ニュースカテゴリー作成
    Parameters
    -----------------------
    dict
        name: str
            ニュースカテゴリの名前
    Returns
    -----------------------
    message: str
        メッセージ
    category: array
        id: int
            カテゴリの一意識別子
        name: str
            カテゴリの名前
        created_at: str
            カテゴリの作成日
        updated_at: str
            カテゴリの更新日(初回作成時は作成日時と同じ）
    """

    try:
        created_news_category = news_crud.create_news_category(db, param)
        db.commit()
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data. 'name' field cannot be empty.")

    di = {
            "id": created_news_category.id,
            "name": created_news_category.name,
            "created_at": created_news_category.created_at.isoformat(),
            "updated_at": created_news_category.updated_at.isoformat(),
        }

    re_di = {
        "message": "Category created successfully.",
        "category": di
    }

    return re_di

@router.get("/categories/", response_model=NewsCategoryListResponseBody, status_code=status.HTTP_200_OK)
async def find_news_category_list(db: DbDependency):
    """
    ニュースカテゴリ一覧取得
    
    Parameters
    -----------------------
    なし

    Returns
    -----------------------
    categories: array
        id: int
            カテゴリの一意識別子
        name: str
            カテゴリの名前
        created_at: str
            カテゴリが作成された日時（ISO 8601形式）
        updated_at: str
            カテゴリが最後に更新された日時（ISO 8601形式）
    """

    news_categories = news_crud.find_news_categories(db)

    li = []
    for category in news_categories:
        di = {
            "id": category.id,
            "name": category.name,
            "created_at": category.created_at.isoformat(),
            "updated_at": category.updated_at.isoformat(),
        }
        li.append(di)

    return {"categories": li}

@router.get("/published", response_model=PublishedNewsListResponseBody, status_code=status.HTTP_200_OK)
async def find_news_list(db: DbDependency, page: int, limit: int):
    """
    ニュース一覧取得

    Parameters
    -----------------------
    page: int
        表示するページ
    limit: int
        1ページに表示するニュース数

    Returns
    -----------------------
    news: array
        id: int
            ニュースのID
        title: str
            ニュースのタイトル
        category: array
            category_id: int
                カテゴリのID
            category_name: str
                カテゴリの名前
        published_at: str
            ニュースの公開日（ISO 8601形式）
    """
    news = news_crud.find_news_by_published(db)

    li = []
    
    for data in news[(page-1)*limit : page*limit]:
        news_category = news_crud.find_news_categories_by_category_id(db, data.news_category_id)
        di = {
            "category_id": news_category.id,
            "category_name": news_category.name
        }

        re_di = {
            "id": data.id,
            "title": data.title,
            "category": di,
            "published_at": data.published_at.isoformat()
        }
        li.append(re_di)

    return {"news": li}