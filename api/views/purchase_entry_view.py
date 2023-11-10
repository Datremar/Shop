from typing import List, Optional

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from fastapi.responses import JSONResponse

from models import PurchaseEntry, Good, Purchase
from schema import PurchaseEntrySchema

purchase_entries_router = APIRouter()


@purchase_entries_router.get("/")
def get_entry(entry_id: int):
    entry_obj = db.session.get(PurchaseEntry, entry_id)

    if not entry_obj:
        return JSONResponse(content={"error": "Purchase entry doesn't exist."}, status_code=404)

    return PurchaseEntrySchema(
        item_id=entry_obj.item_id,
        item_quantity=entry_obj.item_quantity,
        summary_price=entry_obj.summary_price,
        purchase_id=entry_obj.purchase_id
    )


@purchase_entries_router.get("/all")
def get_all_entries(purchase_id: Optional[int] = None):
    entry_objs = db.session.query(PurchaseEntry)

    if not purchase_id:
        entry_objs = entry_objs.all()
    else:
        purchase_obj = db.session.get(Purchase, purchase_id)

        if not purchase_obj:
            return JSONResponse(content={"error": "Purchase doesn't exist."}, status_code=404)

        entry_objs = entry_objs.filter(PurchaseEntry.purchase_id == purchase_id).all()

    entries = [
        PurchaseEntrySchema(
            id=entry.id,
            item_id=entry.item_id,
            item_quantity=entry.item_quantity,
            summary_price=entry.summary_price,
            purchase_id=entry.purchase_id
        )
        for entry in entry_objs
    ]

    return entries


@purchase_entries_router.post("/add", status_code=201)
def add_entry(entry: PurchaseEntrySchema):
    good_obj = db.session.get(Good, entry.item_id)

    if not good_obj:
        return JSONResponse(content={"error": "Good doesn't exist."}, status_code=404)

    purchase_obj = db.session.get(Purchase, entry.purchase_id)

    if not purchase_obj:
        return JSONResponse(content={"error": "Purchase doesn't exist."}, status_code=404)

    entry_obj = PurchaseEntry(
        item_id=entry.item_id,
        item_quantity=entry.item_quantity,
        purchase_id=entry.purchase_id,
        summary_price=good_obj.sell_price * entry.item_quantity
    )

    db.session.add(entry_obj)
    db.session.commit()

    entry.id = entry_obj.id
    entry.summary_price = entry_obj.summary_price

    return entry


@purchase_entries_router.put("/update")
def update_entry(entry_id: int, entry: PurchaseEntrySchema):
    entry_obj = db.session.get(PurchaseEntry, entry_id)

    if not entry_obj:
        return JSONResponse(content={"error": "Purchase doesn't exist."}, status_code=404)

    item_obj = db.session.get(Good, entry_obj.item_id)

    entry_obj.item_id = entry.item_id
    entry_obj.item_quantity = entry.item_quantity
    entry_obj.summary_price = entry.item_quantity * item_obj.sell_price
    entry_obj.purchase_id = entry.purchase_id

    entry.id = entry_obj.id
    entry.summary_price = entry_obj.summary_price

    return entry


@purchase_entries_router.delete("/delete")
def delete_entry(entry_id: int):
    entry_obj = db.session.get(PurchaseEntry, entry_id)

    if not entry_obj:
        return JSONResponse(content={"error": "Purchase entry doesn't exist."}, status_code=404)

    db.session.delete(entry_obj)
    db.session.commit()

    return {"response": "Deleted."}
