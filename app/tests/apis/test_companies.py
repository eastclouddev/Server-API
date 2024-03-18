from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base, get_db
from main import app
from models.companies import Companies

# テスト用のデータベース設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_update_company_success():
    with TestClient(app) as client:

        new_company = {
            "name": "Test Company",
            "prefecture": "Test Prefecture",
            "city": "Test City",
            "town": "Test Town",
            "address": "Test Address",
            "postal_code": "123-4567",
            "phone_number": "123-456-7890",
            "email": "test@example.com"
        }
        # インテグテスト前提のため単体では動作しない
        response = client.post("/companies", json=new_company)
        company_data = response.json()

        update_data = {
            "name": "Updated Company",
            "city": "Updated City"
        }
        response = client.put(f"/companies/{company_data['id']}", json=update_data)
        assert response.status_code == 200
        updated_company = response.json()
        assert updated_company['name'] == update_data['name']
        assert updated_company['city'] == update_data['city']

def test_update_company_failure():
    with TestClient(app) as client:

        update_data = {"name": "Updated Company"}
        response = client.put("/companies/99999", json=update_data)
        assert response.status_code == 404