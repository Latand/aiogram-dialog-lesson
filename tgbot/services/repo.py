# create class with dataclasses
from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    name: str
    product_id: int
    price: float
    stock: int

    def __str__(self):
        return f'{self.name}'


@dataclass
class Category:
    name: str
    category_id: int
    items: List[Product]

    def __str__(self):
        return f'{self.name}'


class Repo:
    categories = []

    def __init__(self):
        # Add Fruits and Vegetables categories
        self.test_add_category(Category('Fruits', 1, []))
        self.test_add_category(Category('Vegetables', 2, []))
        # Add products to Fruits category
        self.test_add_product('Fruits', Product('Apple 🍎', 1, 1.5, 10))
        self.test_add_product('Fruits', Product('Orange 🍊', 2, 1.5, 10))
        self.test_add_product('Fruits', Product('Banana 🍌', 3, 1.5, 10))
        # Add products to Vegetables category
        self.test_add_product('Vegetables', Product('Tomato 🍅', 4, 1.5, 10))
        self.test_add_product('Vegetables', Product('Potato 🥔', 5, 1.5, 10))
        self.test_add_product('Vegetables', Product('Carrot 🥕', 6, 1.5, 10))

    def test_add_category(self, category: Category):
        self.categories.append(category)

    def test_add_product(self, category_name, product: Product):
        for category in self.categories:
            if category.name == category_name:
                category.items.append(product)

    async def get_categories(self, session) -> List[Category]:
        # stmt = select(Categories.category_name, Categories.category_id)
        # result = await session.execute(stmt)
        # categories = result.execute().all()
        return self.categories

    async def get_products(self, session, category_id) -> List[Product]:
        # stmt = select(
        #   Products.product_name, Products.product_id, Products.price, Products.stock
        # ).where(Products.category_id == category_id)
        # result = await session.execute(stmt)
        # products = result.execute().all()
        for category in self.categories:
            if category.category_id == category_id:
                return category.items

    async def get_product(self, session, product_id) -> Product:
        # stmt = select(
        #   Products.product_name, Products.product_id, Products.price, Products.stock
        # ).where(Products.product_id == product_id)
        # result = await session.execute(stmt)
        # product = result.execute().all()
        for category in self.categories:
            for product in category.items:
                if product.product_id == product_id:
                    return product

    async def buy_product(self, session, product_id, amount) -> bool:
        # stmt = update(Products).where(Products.product_id == product_id).values(
        #   stock=Products.stock - amount
        # )
        # await session.execute(stmt)
        # await session.commit()
        for category in self.categories:
            for product in category.items:
                if product.product_id == product_id:
                    product.stock -= amount
                    return True
