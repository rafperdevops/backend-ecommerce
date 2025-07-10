from fastapi import FastAPI
from routes import product_router
from routes import order_router
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Inicializar BD
init_db()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(product_router.router)
app.include_router(order_router.router)

app.mount("/images",StaticFiles(directory="images"), name="images")