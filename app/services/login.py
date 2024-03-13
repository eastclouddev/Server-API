from datetime import datetime, timedelta
import jwt 



# アクセストークンをつくる
def create_access_token(user_id:int):
    # ペイロード作成
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.utcnow() + timedelta(seconds=3600),
        'user_id': user_id
    }    
    #  トークン作成  
    access_token = jwt.encode(access_payload, 'SECRET_KEY123', algorithm='HS256')

    return access_token