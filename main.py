from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import database_models
from database import engine, sessionLocal
from model import Product

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "Hey, Backend Developer"


products = [
    Product(id=1, name="phone", description="budget phone", price=99, quantity=10),
    Product(id=2, name="Tablet", description="Budget Tablet", price=499, quantity=5),
    Product(id=3, name="Monitor", description="Budget Monitor", price=599, quantity=10),
    Product(id=4, name="Mouse", description="Budget Mouse", price=12, quantity=50),
]


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = sessionLocal()
    count = db.query(database_models.Product)

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()


init_db()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db = sessionLocal()
    db_products = db.query(database_models.Product).all()
    return db_products


@app.get("/product/{id}")
def get_product_id(id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_models.Product)
        .filter(database_models.Product.id == id)
        .first()
    )
    if db_product:
        return db_product
    return "Product not found"


@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/product/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_models.Product)
        .filter(database_models.Product.id == id)
        .first()
    )
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"
    else:
        return "Product not found"


@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = (
        db.query(database_models.Product)
        .filter(database_models.Product.id == id)
        .first()
    )
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        return "Product not found"
