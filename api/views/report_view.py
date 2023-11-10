from datetime import date

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import func

from models import User, Purchase, PurchaseEntry
from schema import ReportSchema

report_router = APIRouter()


@report_router.get("/")
async def get_report(start_date: date, end_date: date):
    users = (
        db.session.query(
            User.id, User.name, User.email, func.sum(PurchaseEntry.summary_price).label('total_purchase_cost')
        )
        .join(Purchase, Purchase.buyer_id == User.id)
        .join(PurchaseEntry, PurchaseEntry.purchase_id == Purchase.id)
        .filter(Purchase.purchased_at > start_date, Purchase.purchased_at < end_date)
        .group_by(User.id, User.name, User.email)
        .order_by('total_purchase_cost').all()
    )

    report = [
        ReportSchema(
            id=user.id,
            name=user.name,
            email=user.email,
            total=user.total_purchase_cost
        )
        for user in users
    ]

    return report
