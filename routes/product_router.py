from fastapi import APIRouter
from models.product import Product
from controllers import product_controller
from fastapi import UploadFile, File, Form

router = APIRouter()

@router.get("/products") # Método y ruta
def get_products(): # Endpoint
    return product_controller.list_produts()


@router.post("/products")
def save_product(id:int = Form(...),
                 name:str = Form(...),
                 price:str = Form(...),
                 stock:int = Form(...),
                 image: UploadFile = File(...)):
    return product_controller.create_product(id,
                                            name,
                                            price,
                                            stock,
                                            image
                                            )

# /products/10
@router.get("/products/{product_id}")
def get_one(product_id:int):
    return product_controller.get_product(product_id)

@router.put("/products/{product_id}")
def update(product_id:int, product:Product):
    return product_controller.update_product(product_id,product)

@router.delete("/products/{product_id}")
def delete(product_id:int):
    return product_controller.delete_product(product_id)