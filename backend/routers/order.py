from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db, Order, OrderItem

router = APIRouter(
    tags=["orders"],
    responses={404: {"description": "Endpoint not found"}},
)

@router.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    """
    Return all orders sorted by order_number, including their items.
    """
    orders = db.query(Order).order_by(Order.order_number).all()
    return [
        {
            "order_id": order.id,
            "order_number": order.order_number,
            "user_id": order.user_id,
            "items": [
                {
                    "item_name": item.item_name,
                    "quantity": item.quantity
                }
                for item in order.items
            ]
        }
        for order in orders
    ]

@router.get("/order_items")
def get_order_items(db: Session = Depends(get_db)):
    """
    Return all order items grouped by item_name, showing the combined quantity.
    """
    grouped_items = (
        db.query(
            OrderItem.item_name,
            func.sum(OrderItem.quantity).label("total_quantity")
        )
        .group_by(OrderItem.item_name)
        .all()
    )
    return [
        {
            "item_name": row.item_name,
            "total_quantity": row.total_quantity
        }
        for row in grouped_items
    ]
