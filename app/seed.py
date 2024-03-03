from database.database import SessionLocal
# from models.product import Product

db = SessionLocal()

def seed():
    print("Seeding init data...")
    # # 初期データの定義
    # products = [
    #     Product(id=1, name='商品1', price=1000, description='ジャンク品です'),
    #     Product(id=2, name='商品2', price=10000, description='ほぼ新品です')
    # ]

    # # 初期データの登録
    # with db.begin():
    #     [db.merge(product) for product in products] # addだとdocker起動のたびにレコードが出来るので mergeが良い


if __name__ == '__main__':
    seed()
