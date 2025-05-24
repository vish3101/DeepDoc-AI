import os

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from Backend.database import get_db  # Your DB session dependency
from Backend.database.models import User  # Your SQLAlchemy User model

router = APIRouter()

# OAuth configuration
oauth = OAuth()
oauth.register(
    name='github',
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@router.get("/login/github")
async def login_with_github(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        # Step 1: Authorize and get token
        token = await oauth.github.authorize_access_token(request)
        
        # Step 2: Fetch user profile data
        user_data = await oauth.github.get('user', token=token)
        user_info = user_data.json()

        username = user_info.get("login")
        email = user_info.get("email")

        # Step 3: If email is hidden, fetch from user/emails endpoint
        if not email:
            email_data = await oauth.github.get("user/emails", token=token)
            email_list = email_data.json()
            for item in email_list:
                if item.get("primary") and item.get("verified"):
                    email = item.get("email")
                    break

        # Step 4: Store or fetch from DB
        user = db.query(User).filter(User.username == username).first()
        if not user:
            user = User(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)

        # Step 5: Return user info (you can replace this with token/session logic)
        return JSONResponse(content={
            "username": user.username,
            "email": user.email,
            "message": "Login successful"
        })

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
