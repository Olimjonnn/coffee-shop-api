from fastapi import FastAPI
from app.api.v1 import users, orders, menu, cart, order_items

app = FastAPI(title="Coffee Backend API")

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(orders.router)
app.include_router(menu.router)
app.include_router(cart.router)
app.include_router(order_items.router)
