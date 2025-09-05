# createdb.py
from app.db.base import engine
from app.db.base import Base
Base.metadata.create_all(bind=engine)
print("Database and tables created successfully.")
