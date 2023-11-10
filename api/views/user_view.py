from typing import List

from fastapi import APIRouter, UploadFile, File
from fastapi_sqlalchemy import db
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError
from starlette.responses import FileResponse

from models import User
from schema import UserSchema
from utils.profile_pics import save_pic, delete_pic

user_router = APIRouter()


@user_router.post("/add", status_code=201)
async def add_user(user: UserSchema):
    user_obj = User(
        name=user.name,
        patronymic=user.patronymic,
        surname=user.surname,
        year=user.year,
        gender=user.gender.name,
        email=user.email,
        consent=user.consent
    )

    try:
        db.session.add(user_obj)
        db.session.commit()
    except IntegrityError:
        return JSONResponse(content={"error": "User already exists."}, status_code=422)

    return {"response": "OK", "user_id": user_obj.id}


@user_router.post("/profile-pic/add", status_code=201)
async def add_profile_pic(
        user_id: int,
        profile_pic: UploadFile = File(...)
):
    user_obj = db.session.get(User, user_id)

    if not user_obj:
        return JSONResponse(content={"error": "User doesn't exist."}, status_code=404)

    img_path = await save_pic(profile_pic)
    user_obj.profile_pic_dir = img_path

    db.session.commit()

    return {"response": "OK"}


@user_router.get("/profile-pic/get")
async def get_profile_pic(user_id: int):
    user_obj = db.session.get(User, user_id)

    if not user_obj:
        return JSONResponse(content={"error": "User doesn't exist."}, status_code=404)

    if not user_obj.profile_pic_dir:
        return JSONResponse(content={"error": "User profile picture doesn't exist."}, status_code=404)

    return FileResponse(
        path=user_obj.profile_pic_dir,
        filename=f"{user_obj.name}_{user_obj.patronymic}_{user_obj.surname}_profile.jpg",
        media_type='multipart/form-data'
    )


@user_router.get("/")
async def get_user(user_id: int):
    user = db.session.get(User, user_id)

    if not user:
        return JSONResponse(content={"error": "User doesn't exist."}, status_code=404)

    return UserSchema(
        name=user.name,
        patronymic=user.patronymic,
        surname=user.surname,
        gender=user.gender.name,
        year=user.year,
        email=user.email,
        consent=user.consent
    )


@user_router.get("/all")
async def get_users() -> List[UserSchema]:
    user_objs = db.session.query(User).all()

    users = [
        UserSchema(
            id=user.id,
            name=user.name,
            patronymic=user.patronymic,
            surname=user.surname,
            gender=user.gender.name,
            year=user.year,
            email=user.email,
            consent=user.consent
        )
        for user in user_objs
    ]

    return users


@user_router.put("/update")
async def update_user(user_id: int, user: UserSchema):
    user_obj = db.session.get(User, user_id)

    if not user_obj:
        return JSONResponse(content={"error": "User doesn't exist."}, status_code=404)

    user_obj.name = user.name
    user_obj.patronymic = user.patronymic
    user_obj.surname = user.surname
    user_obj.email = user.email
    user_obj.gender = user.gender.name
    user_obj.year = user.year

    db.session.commit()

    user.id = user_obj.id

    return user


@user_router.delete("/delete")
async def delete_user(user_id: int):
    user_obj = db.session.get(User, user_id)

    if not user_obj:
        return JSONResponse(content={"error": "User doesn't exist."}, status_code=404)

    if user_obj.profile_pic_dir:
        await delete_pic(img_path=user_obj.profile_pic_dir)

    db.session.delete(user_obj)
    db.session.commit()

    return {"response": "Deleted."}
