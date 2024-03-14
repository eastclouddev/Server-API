


def cereate_users_list(role, found_user):

    users_list = []

    # ユーザーを辞書型に格納
    for user in found_user:
        user_personal = {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": role,
            "last_login": user.last_login.isoformat()
        }
        # ユーザーデータをリストに追加
        users_list.append(user_personal)

    # リストを辞書型に格納
    return {"users": users_list}
    # ↑↑↑↑↑↑↑↑↑↑userをなんの順番で並び替えるのか、last_login順、user_id順、名前の昇順降順などなど。↑↑↑↑↑↑↑↑
   