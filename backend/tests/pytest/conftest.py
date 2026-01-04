import pytest
import pytest_asyncio
from datetime import datetime
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db
from app.core.security import create_access_token
from app.models import Base, User, Group, GroupMember, Food, Category, Unit

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def override_get_db(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def client(override_get_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User",
        username="testuser",
        language="en",
        timezone=0,
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_group(db_session, test_user):
    group = Group(
        name="Test Group",
        owner_id=test_user.id,
        is_active=True,
    )
    db_session.add(group)
    db_session.commit()
    db_session.refresh(group)

    group_member = GroupMember(
        user_id=test_user.id,
        group_id=group.id,
        role="admin",
        is_active=True,
    )
    db_session.add(group_member)
    db_session.commit()

    return group


@pytest.fixture
def test_category(db_session):
    category = Category(
        name="Vegetables",
        description="Fresh vegetables",
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def test_unit(db_session):
    unit = Unit(
        name="kg",
        type="weight",
    )
    db_session.add(unit)
    db_session.commit()
    db_session.refresh(unit)
    return unit


@pytest.fixture
def test_food(db_session, test_group, test_category, test_unit, test_user):
    food = Food(
        name="Tomato",
        description="Fresh tomato",
        category_id=test_category.id,
        unit_id=test_unit.id,
        group_id=test_group.id,
        is_active=True,
        created_by=test_user.id,
    )
    db_session.add(food)
    db_session.commit()
    db_session.refresh(food)
    return food


@pytest.fixture
def auth_headers(test_user):
    token = create_access_token({"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}
