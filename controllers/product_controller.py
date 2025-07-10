from fastapi import HTTPException
from models.product import Product
from database import get_connection
import shutil
import os

products_db = []

def list_produts():
    conn = get_connection()
    cursor = conn.cursor()
    products = cursor.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [dict(row) for row in products]

def create_product(id,name,price,stock,image):
    #Guardar imagen
    ext = os.path.splitext(image.filename)[1]
    filename = f"{id}{ext}"
    image_path = f"images/{filename}"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (id, name, price, stock, image_url) VALUES (?,?,?,?,?)", (id, name, price, stock,image_path))
        conn.commit()
        conn.close()
        return {"status": "ok", "msg": f"{name}, guardado exitosamente el producto"}
    except Exception as ex:
        print(ex)
        conn.close()
        return {"status": "error", "msg": f"{name}, No se pudo guardar"}

def get_product(product_id:int):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    if row is None:
        return {"status":"error", "msg": "Producto no encontrado"}
    
    return {"status":"ok", "msg": "Producto encontrado", "data": dict(row)} 

def update_product(product_id:int, updated:Product):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?",(product_id,))
    if cursor.fetchone() is None:
        conn.close()
        return {"status":"error", "msg": "Producto no encontrado"}

    try:
        cursor.execute("UPDATE products SET name = ?, price = ?, stock =? WHERE id=?", (updated.name, updated.price, updated.stock, updated.id))
        conn.commit()
        conn.close()
        return {"status": "ok", "msg": f"{updated.name}, actualizado exitosamente"}
    except Exception as ex:
        print(ex)
        conn.close()
        return {"status": "error", "msg": f"{updated.name}, No se pudo actualizar"}    

def delete_product(product_id:int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?",(product_id,))
    if cursor.fetchone() is None:
        conn.close()
        return {"status":"error", "msg": "Producto no encontrado"}

    try:
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()
        return {"status": "ok", "msg": f"Eliminado exitosamente"}
    except Exception as ex:
        print(ex)
        conn.close()
        return {"status": "error", "msg": f"No se pudo eliminar"}  