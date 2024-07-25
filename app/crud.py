from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import List
from .models import Product

client = MongoClient("mongodb://mongodb:27017")  # Usar el nombre del servicio de MongoDB en docker-compose
db = client.my_database
products_collection = db.products

def create_product(product: Product) -> str:
    product_dict = product.dict()
    product_dict.pop("id", None)
    result = products_collection.insert_one(product_dict)
    return str(result.inserted_id)

def get_product(product_id: str) -> Product:
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if product:
        return Product(id=str(product["_id"]), **product)
    return None

def update_product(product_id: str, product: Product) -> bool:
    update_result = products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product.dict(exclude_unset=True)}
    )
    return update_result.modified_count > 0

def delete_product(product_id: str) -> bool:
    delete_result = products_collection.delete_one({"_id": ObjectId(product_id)})
    return delete_result.deleted_count > 0

def get_all_products() -> List[Product]:
    products = products_collection.find()
    return [Product(id=str(product["_id"]), **product) for product in products]
