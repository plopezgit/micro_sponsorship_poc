from typing import Optional
from app.entities.product import Product

class ProductRepository:
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product) -> None:
        self.products[product.product_id] = product

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)