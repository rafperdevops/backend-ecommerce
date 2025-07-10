from fastapi import APIRouter
from models.order import Order
from controllers import order_controller

router = APIRouter(prefix="/orders")

# [{product_id: 20, quantity: 2}, {product_id: 41, quantity: 3}]
@router.post("/")
def create_order(order: Order):
    return order_controller.create_order(order)