from fastapi import Depends, APIRouter, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
import requests, time

from app.database import get_db
from app.models import User

router = APIRouter()

@router.post("/facebook/schedule-post-dynamic")
def schedule_facebook_post_dynamic(
    user_id: int = Form(...),
    message: str = Form(None),
    image: UploadFile = File(None),
    schedule_minutes: int = Form(None),
    scheduled_datetime: str = Form(None),  # format: "YYYY-MM-DDTHH:MM:SS"
    db: Session = Depends(get_db)
):
    # 1. Get user from DB
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    user_token = user.session_token

    # 2. Get pages managed by the user
    pages = requests.get(
        "https://graph.facebook.com/v24.0/me/accounts",
        params={"access_token": user_token}
    ).json()

    if "data" not in pages or not pages["data"]:
        return {"error": "No pages found", "details": pages}

    page_id = pages["data"][0]["id"]
    page_token = pages["data"][0]["access_token"]

    # 3. Determine scheduled time
    if scheduled_datetime:
        dt = datetime.strptime(scheduled_datetime, "%Y-%m-%dT%H:%M:%S")
        scheduled_time = int(dt.timestamp())
    elif schedule_minutes is not None:
        scheduled_time = int(time.time()) + schedule_minutes * 60
        dt = datetime.fromtimestamp(scheduled_time)
    else:
        return {"error": "Either schedule_minutes or scheduled_datetime must be provided."}

    # 4. Prepare the post data dynamically
    post_data = {
        "published": False,
        "scheduled_publish_time": scheduled_time,
        "access_token": page_token
    }

    # Attach message if provided
    if message:
        post_data["message"] = message

    # Attach image if provided
    if image:
        # Upload the image first
        files = {"source": (image.filename, image.file, image.content_type)}
        upload_resp = requests.post(
            f"https://graph.facebook.com/v24.0/{page_id}/photos",
            params={"published": "false", "access_token": page_token},
            files=files
        ).json()

        if "id" not in upload_resp:
            return {"error": "Image upload failed", "details": upload_resp}

        photo_id = upload_resp["id"]
        # Attach the uploaded photo to post
        post_data["attached_media[0]"] = f'{{"media_fbid":"{photo_id}"}}'
    else:
        photo_id = None

    # 5. Create scheduled post
    post_resp = requests.post(
        f"https://graph.facebook.com/v24.0/{page_id}/feed",
        data=post_data
    ).json()

    return {
        "status": "scheduled",
        "page_id": page_id,
        "scheduled_timestamp": scheduled_time,
        "scheduled_datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "message": message,
        "photo_id": photo_id,
        "facebook_response": post_resp
    }
