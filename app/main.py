from fastapi import FastAPI, HTTPException
from typing import List
from .models import Product
from .crud import create_product, get_product, update_product, delete_product, get_all_products

app = FastAPI()

@app.post("/products/", response_model=str)
def create(product: Product):
    product_id = create_product(product)
    return product_id

@app.get("/products/{product_id}", response_model=Product)
def read(product_id: str):
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=bool)
def update(product_id: str, product: Product):
    success = update_product(product_id, product)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return success

@app.delete("/products/{product_id}", response_model=bool)
def delete(product_id: str):
    success = delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return success

@app.get("/products/", response_model=List[Product])
def read_all():
    return get_all_products()
