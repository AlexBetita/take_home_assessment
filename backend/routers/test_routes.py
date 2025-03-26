from fastapi import APIRouter, Depends

from db import (User, 
                Order,
                Session, get_db)

router = APIRouter(
    tags=["test"],
    responses={404: {"description": "Endpoint not found"}},
)

@router.get("/test/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "username": user.username} for user in users]

@router.get("/test/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return [{
        "id": order.id,
        "order_number": order.order_number,
        "user_id": order.user_id,
        "items": [
            {"id": item.id, "item_name": item.item_name, "quantity": item.quantity}
            for item in order.items
        ]
    } for order in orders]