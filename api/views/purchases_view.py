from typing import List

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from fastapi.responses import JSONResponse

from models import Purchase, User
from schema import PurchaseSchema

purchases_router = APIRouter()


@purchases_router.get("/")
def get_purchase(purchase_id: int):
    purchase_obj = db.session.get(Purchase, purchase_id)

    if not purchase_obj:
        return JSONResponse(content={"error": "Purchase doesn't exist."}, status_code=404)

    return PurchaseSchema(
        id=purchase_obj.id,
        buyer_id=purchase_obj.buyer_id,
        purchased_at=purchase_obj.purchased_at
    )


@purchases_router.get("/all")
def get_all_purchases(user_id: int) -> List[PurchaseSchema]:
    purchase_objs = db.session.query(Purchase).filter(Purchase.buyer_id == user_id).all()

    purchases = [
        PurchaseSchema(
            id=purchase.id,
            buyer_id=purchase.buyer_id,
            purchased_at=purchase.purchased_at
        )
        for purchase in purchase_objs
    ]

    return purchases


@purchases_router.post("/add", status_code=201)
def add_purchase(purchase: PurchaseSchema):
    user_obj = db.session.get(User, purchase.buyer_id)

    if not user_obj:
        return JSONResponse(content={"error": "User doesn't exist."}, status_code=404)

    purchase_obj = Purchase(**purchase.model_dump())

    db.session.add(purchase_obj)
    db.session.commit()

    purchase.id = purchase_obj.id
    purchase.purchased_at = purchase_obj.purchased_at

    return purchase


@purchases_router.put("/update")
def update_purchase(purchase_id: int, purchase: PurchaseSchema):
    purchase_obj = db.session.get(Purchase, purchase_id)

    if not purchase_obj:
        return JSONResponse(content={"error": "Purchase doesn't exist."}, status_code=404)

    user_obj = db.session.get(User, purchase.buyer_id)

    if not user_obj:
        return JSONResponse(content={"error": "User doesn't exist."}, status_code=404)

    purchase_obj.buyer_id = purchase.buyer_id
    if purchase.purchased_at:
        purchase_obj.purchased_at = purchase.purchased_at

    db.session.commit()

    purchase.id = purchase_obj.id
    purchase.purchased_at = purchase_obj.purchased_at

    return purchase


@purchases_router.delete("/delete")
def delete_purchase(purchase_id: int):
    purchase_obj = db.session.get(Purchase, purchase_id)

    if not purchase_obj:
        return JSONResponse(content={"error": "Purchase doesn't exist."}, status_code=404)

    db.session.delete(purchase_obj)
    db.session.commit()

    return {"response": "Deleted."}
