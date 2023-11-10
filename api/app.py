import os
import sys

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from views.goods_view import goods_router
from views.purchase_entry_view import purchase_entries_router
from views.purchases_view import purchases_router
from views.report_view import report_router
from views.user_view import user_router
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

load_dotenv(os.path.join(BASE_DIR, '.env'))
sys.path.append(BASE_DIR)
load_dotenv(".env")

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

app.include_router(user_router, prefix="/user")
app.include_router(goods_router, prefix="/good")
app.include_router(purchases_router, prefix="/purchase")
app.include_router(purchase_entries_router, prefix="/purchase/entry")
app.include_router(report_router, prefix="/report")
