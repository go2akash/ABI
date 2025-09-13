from fastapi import FastAPI
from app.router.users import router as users
from app.router.accounts import router as accounts
from app.router.transactions import router as transactions
from app.router.admin import router as admin


app = FastAPI(title="Akash Bank of India", description="This is a sample Bank API", version="1.0.0")


app.include_router(users,tags=["Users"])
app.include_router(accounts,tags=["Accounts"])
app.include_router(transactions,tags=["Transactions"])
# app.include_router(auth,tags=["Authentication"])
app.include_router(admin,tags=["Admin"])

@app.get("/")
def read_root():
    return {"Hello": "Welcome to my bank"}
