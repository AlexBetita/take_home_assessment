import json
from fastapi import APIRouter, HTTPException
from sqlalchemy import func
from pydantic import BaseModel

from db import Order, OrderItem, get_db
from models import client
from utils import order_functions

router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Endpoint not found"}},
)

class ChatRequest(BaseModel):
    message: str

class CommandRequest(BaseModel):
    message: str
    user_id: int
    
@router.post("/command")
def command(command_request: CommandRequest):
    message = command_request.message
    user_id = command_request.user_id

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": message}],
        functions=order_functions,
        function_call="auto"
    )

    message_response = response.choices[0].message

    if message_response.function_call is not None:
        function_call = message_response.function_call
        arguments = json.loads(function_call.arguments)
        
        if function_call.name == "take_order":
            order_result = take_order(arguments["items"], user_id)
            return {"bot_response": "Order received and stored in database", "response": order_result}
        elif function_call.name == "delete_order":
            order_result = delete_order(arguments["order_number"], user_id)
            return {"bot_response": "Order deleted", "response": order_result}
        else:
            return {"bot_response": "Unknown function call", "response": {}}
    else:
        content = message_response.content if message_response.content else "No response from assistant."
        return {"bot_response": content, "response": {}}

def take_order(items: list, user_id: int):
    """
    Process and store the order in the database with an auto-incrementing order number.
    Only orders for Burgers, Fries, and Drinks are accepted.
    If any items are not on the menu, they are ignored and the response will note them.
    """
    allowed_menu = {"Burgers", "Fries", "Drinks"}
    valid_items = []
    invalid_items = []
    
    for item in items:
        # Only process allowed items
        if item["item_name"] in allowed_menu:
            valid_items.append(item)
        else:
            invalid_items.append(item["item_name"])
    
    if not valid_items:
        return {"status": "No valid items ordered. Allowed items are: Burgers, Fries, Drinks."}
    
    db = next(get_db())
    max_order_number = db.query(func.max(Order.order_number)).scalar()
    new_order_number = 1 if max_order_number is None else int(max_order_number) + 1

    new_order = Order(order_number=new_order_number, user_id=user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in valid_items:
        new_order_item = OrderItem(
            order_id=new_order.id,
            item_name=item["item_name"],
            quantity=item["quantity"]
        )
        db.add(new_order_item)
    db.commit()
    
    response = {
        "order_id": new_order.id,
        "order_number": new_order_number,
        "items": valid_items,
        "status": "Order received and stored in database"
    }
    if invalid_items:
        response["note"] = f"The following items were not processed as they are not on the menu: {', '.join(invalid_items)}"
    
    return response

def delete_order(order_number: int, user_id: int):
    """
    Delete a specific order (and its items) from the database by order number,
    but only if it belongs to the given user.
    """
    db = next(get_db())
    
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sorry that order is not found, please try again.")
    
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="Sorry, you're not allowed to cancel others' orders")
    
    for item in order.items:
        db.delete(item)
    db.delete(order)
    db.commit()
    
    return {"status": "Order deleted", "order_number": order_number}
