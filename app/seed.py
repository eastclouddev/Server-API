from database.database import SessionLocal
from models.companies import Companies
from models.roles import Roles

db = SessionLocal()

def seed():
    print("Seeding init data...")

    companies = [
        Companies(
            id=1,
            name='会社1',
            prefecture='prefecture',
            city='Tokyo',
            town='Shibuya', 
            address='address',
            postal_code='000-0000',
            phone_number='090-0000-0000',
            email='test@test.mail',
        ),
    ]

    roles = [
        Roles(
            id=1,
            name='生徒',
            description='生徒向けロール'
        )
    ]

    with db.begin():
        [db.merge(companie) for companie in companies] # addだとdocker起動のたびにレコードが出来るので mergeが良い
        [db.merge(role) for role in roles]


if __name__ == '__main__':
    seed()
