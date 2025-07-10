from database import get_connection
from models.order import Order
import datetime

def create_order(order: Order):
    conn = get_connection()
    cursor = conn.cursor()

    total = 0
    for item in order.items:
        product = cursor.execute("SELECT price FROM products WHERE id = ?", (item.product_id,)).fetchone()
        if product:
            total += product["price"] * item.quantity
        else:
            conn.close()
            return {"status":"error", "msg": "Producto no encontrado"}
    
    now = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO orders (total, created_at) VALUES (?, ?)", (total, now))
    order_id = cursor.lastrowid

    for item in order.items:
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?,?,?)",
            (order_id, item.product_id, item.quantity)
        )
    
    conn.commit()
    conn.close()
    return {"status":"ok", "msg": "Compra guardada con éxito"}

def list_order():
    return {"status":"ok", "msg": "Listado"}