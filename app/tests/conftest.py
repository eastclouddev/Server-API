import os
import sys

app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(app_dir)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker
from models import product
from main import app
from database.database import get_db
from database.database import Base


@pytest.fixture()
def session_fixture():
    engine = create_engine(
        url="sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # common test_data
    try:
        # product1 = product.Product(name="product1", price=9999, description="test1")
        # product2 = product.Product(name="product2", price=8900, description="test2")
        # db.add(product1)
        # db.add(product2)
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture()
def client_fixture(session_fixture: Session):
    def override_get_db():
        return session_fixture

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
