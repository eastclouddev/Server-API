import jwt

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from logging import getLogger
logger = getLogger("uvicorn.app")

def get_email(token):
    try:
        # トークンのデコード
        payload = jwt.decode(token, key='SECRET_KEY123', algorithms='HS256')
        

        # ペイロードからユーザー情報を取得
        user_info = {
            "email": payload.get("email")
        }
        
        return user_info
    
    except jwt.ExpiredSignatureError:
        # トークンが期限切れの場合の処理
        raise HTTPException(status_code=400, detail="Invalid or expired token.")
    except jwt.InvalidTokenError as e:
        logger.error(e)
        # トークンが無効な場合の処理
        raise HTTPException(status_code=400, detail="Invalid or expired token.")