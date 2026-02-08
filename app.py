from fastapi import FastAPI
import uvicorn
from src.api.user_route import router as user_router
from src.api.book_route import router as book_router
from src.api.loan_route import router as loan_router
from src.api.portfolio_route import router as portfolio_router
from src.api.report_route import router as report_router

app = FastAPI()
app.include_router(user_router, tags=["Users"])
app.include_router(book_router, tags=["Books"])
app.include_router(loan_router, tags=["Loans"])
app.include_router(portfolio_router, tags=["Portfolio"])
app.include_router(report_router, tags=["Reports"])

@app.get("/")
def home():
    return {"Hello": "HelloWorld('print')"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)