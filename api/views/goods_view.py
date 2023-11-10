from typing import List

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy.exc import IntegrityError

from models import Good
from schema import GoodSchema

from fastapi.responses import JSONResponse

goods_router = APIRouter()


@goods_router.get("/")
def get_good(good_id: int):
    good_obj = db.session.get(Good, good_id)

    if not good_obj:
        return JSONResponse(content={"error": "Good doesn't exist."}, status_code=404)

    return GoodSchema(
        name=good_obj.name,
        buy_price=good_obj.buy_price,
        sell_price=good_obj.sell_price
    )


@goods_router.get("/all")
def get_all_goods() -> List[GoodSchema]:
    good_objs = db.session.query(Good).all()

    goods = [
        GoodSchema(
            id=good.id,
            name=good.name,
            buy_price=good.buy_price,
            sell_price=good.sell_price
        )
        for good in good_objs
    ]

    return goods


@goods_router.post("/add", status_code=201)
def add_good(good: GoodSchema):
    good_obj = Good(**good.model_dump())

    try:
        db.session.add(good_obj)
        db.session.commit()
    except IntegrityError:
        return JSONResponse(content={"error": "Good already exists."}, status_code=422)

    return {"response": "OK"}


@goods_router.put("/update")
def update_good(good_id: int, good: GoodSchema):
    good_obj = db.session.get(Good, good_id)

    if not good_obj:
        return JSONResponse(content={"error": "Good doesn't exist."}, status_code=404)

    good_obj.name = good.name
    good_obj.buy_price = good.buy_price
    good_obj.sell_price = good.sell_price

    good.id = good_obj.id

    db.session.commit()

    return good


@goods_router.delete("/delete")
def delete_good(good_id: int):
    good_obj = db.session.get(Good, good_id)

    if not good_obj:
        return JSONResponse(content={"error": "Good doesn't exist."}, status_code=404)

    db.session.delete(good_obj)
    db.session.commit()

    return {"response": "Deleted."}

