order_functions = [
        {
            "name": "take_order",
            "description": """Take an order from a user by specifying a list of items. 
                            If quantity not specified then its one for each item on list that's not specified""",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "description": "List of order items with item name(Capitalized, Plural Form) and quantity.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "item_name": {
                                    "type": "string",
                                    "description": "Name of the item (e.g., Fries, Burger)."
                                },
                                "quantity": {
                                    "type": "integer",
                                    "description": "Quantity of the item."
                                }
                            },
                            "required": ["item_name", "quantity"]
                        }
                    }
                },
                "required": ["items"]
            }
        },
        {
            "name": "delete_order",
            "description": "Delete a specific order by providing the order number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_number": {
                        "type": "integer",
                        "description": "The order number of the order to delete."
                    }
                },
                "required": ["order_number"]
            }
        }
    ]