from app.database.db import engine
from app.database.models import Base
from sqlalchemy import inspect, text

#python -m app.database.init_db

print("Creating tables...")

Base.metadata.create_all(bind=engine)

inspector = inspect(engine)
columns = [
    column["name"]
    for column in inspector.get_columns("jobs")
]

if "active" not in columns:
    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE jobs ADD COLUMN active INTEGER DEFAULT 1")
        )
    print("Added active column")

if "remote" not in columns:
    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE jobs ADD COLUMN remote INTEGER DEFAULT 0")
        )
    print("Added remote column")

if "easy apply" in columns:
    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE jobs ADD COLUMN easy_apply INTEGER DEFAULT 1")
        )
    print("Added easy_apply column")

print("Tables created")
print(Base.metadata.tables.keys())
