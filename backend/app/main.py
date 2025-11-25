from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
import httpx
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from datetime import datetime, timedelta
import requests
from app.routes.facebook_analytics import router as analytics_router
from app.routes.insta_analytics import router as insta_analytics_router
from app.routes.post_scheduling import router as scheduling_router



load_dotenv()

app = FastAPI()
app.include_router(analytics_router)
app.include_router(scheduling_router)
app.include_router(insta_analytics_router)

FB_APP_ID = os.getenv("FB_APP_ID")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


@app.get("/auth/facebook/login")
def facebook_login():
    auth_url = (
        "https://www.facebook.com/v24.0/dialog/oauth"
        f"?client_id={FB_APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&state=test_state"
        "&scope=pages_show_list,pages_read_engagement,public_profile,business_management,instagram_basic,instagram_manage_insights"
    )
    return RedirectResponse(auth_url)


@app.get("/auth/facebook/callback")
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code returned from Facebook"}

    token_url = (
        f"https://graph.facebook.com/v18.0/oauth/access_token"
        f"?client_id={FB_APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&client_secret={FB_APP_SECRET}"
        f"&code={code}"
    )

    token_response = requests.get(token_url).json()
    if "access_token" not in token_response:
        return {"error": "Failed to exchange code for token", "details": token_response}

    short_token = token_response["access_token"]

    long_url = (
        f"https://graph.facebook.com/v18.0/oauth/access_token"
        f"?grant_type=fb_exchange_token"
        f"&client_id={FB_APP_ID}"
        f"&client_secret={FB_APP_SECRET}"
        f"&fb_exchange_token={short_token}"
    )

    long_token_response = requests.get(long_url).json()
    long_token = long_token_response.get("access_token", short_token)

    user_info_url = f"https://graph.facebook.com/me?fields=id,name&access_token={long_token}"
    user_data = requests.get(user_info_url).json()

    if "id" not in user_data:
        return {"error": "Could not fetch Facebook user id", "details": user_data}

    facebook_id = user_data["id"]
    name = user_data.get("name")

    user = db.query(User).filter(User.facebook_id == facebook_id).first()

    if user:
        user.session_token = long_token
    else:
        user = User(
            facebook_id=facebook_id,
            name=name,
            session_token=long_token
        )
        db.add(user)

    db.commit()

    return {
        "message": "Facebook authentication successful",
        "facebook_id": facebook_id,
        "session_token": long_token
    }
