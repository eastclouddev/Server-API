from sqlalchemy.orm import Session
from models.roles import Roles
from models.users import Users

from logging import getLogger

logger = getLogger("uvicorn.app")

# Rolesのnameと受け取ったroleが一致するユーザーを取得
def find_by_role(db: Session, role: str, page: int, limit: int):

    # Roles.nameと受け取ったroleが一致するRoles(役割のテーブル)を取得
    role = db.query(Roles).filter(Roles.name == role).first()

    logger.warning("ok")

    users = None

    if page>0 and limit>0:
    # Userのrole_idと受けとったrole.idが一致するユーザーを全員取得
        users = db.query(Users).filter(Users.role_id == role.id).offset((page - 1) * limit).limit(limit).all()  

    logger.warning("ok")

    return users



