from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from Backend.routers import list_pdf, query, upload_pdf, user_auth

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="YOUR_SECRET_KEY_HERE")
app.include_router(user_auth.router)
app.include_router(upload_pdf.router)
app.include_router(list_pdf.router)
app.include_router(query.router)


