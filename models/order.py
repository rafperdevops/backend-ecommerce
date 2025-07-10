from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    items: List[OrderItem]

# [{product_id: 20, quantity: 2}, {product_id: 41, quantity: 3}]