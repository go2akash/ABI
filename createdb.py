from app.db.base import engine
from app.db.base import Base
from app.models.users import User
from app.models.accounts import Account
from app.models.transactions import BankTransaction


Base.metadata.create_all(bind=engine)
print("Database and tables created successfully.")
