from fastapi import FastAPI
from pydantic import BaseModel
import database_app
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="greenfield Backend API")
# from here copy 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# till here

# ---------- DATA MODELS ----------
 
class Category(BaseModel):
    name: str
    description: str | None = None
 
 
class Product(BaseModel):
    name: str
    category_id: int
    price: float
    stock: int
    description: str | None = None
 
 
class Customer(BaseModel):
    email: str
    password: str
    full_name: str
    phone_number: str
    home_address: str

class Order(BaseModel):
    customer_id: int
    product_id: int
    quantity: int

class Login(BaseModel):
    email: str
    password: str
 
# ---------- CATEGORY ENDPOINTS ----------
 
@app.get("/categories")
def get_categories():
    data = database_app.get_categories()
    return [
        {"id": c[0], "name": c[1], "description": c[2]}
        for c in data
    ]
 
 
@app.post("/categories")
def create_category(category: Category):
    database_app.add_category(category.name, category.description)
    return {"message": "Category created"}
 
 
# ---------- PRODUCT ENDPOINTS ----------
from typing import Optional
from fastapi import Query

@app.get("/products")
def get_products(category_id:Optional[int]= Query(None)):
    data = database_app.get_products_with_categories(category_id)
    return [
        {
            "id": p[0],
            "product_name": p[1],
            "category_name": p[2],
            "price": p[3],
            "stock": p[4]
        }
        for p in data
    ]
 
 
@app.post("/products")
def create_product(product: Product):
    database_app.add_product(
        product.name,
        product.category_id,
        product.price,
        product.stock,
        product.description
    )
    return {"message": "Product created"}
 
 
# ---------- CUSTOMER ENDPOINTS ----------
 
@app.get("/customers")
def get_customers():
    data = database_app.get_customers()

    return [
        {
            "id": c[0],
            "email": c[1],
            "password": c[2],
            "full_name": c[3],
            "phone_number": c[4],
            "home_address": c[5]
        }
        for c in data
    ]
 
 

@app.post("/customers")
def create_customer(customer: Customer):

    database_app.add_customer(
        customer.email,
        customer.password,
        customer.full_name,
        customer.phone_number,
        customer.home_address
    )

    return {"message": "Customer registered successfully"}

@app.post("/login")
def login_user(login: Login):
    users = database_app.get_customers()

    for u in users:
        if u[1] == login.email and u[2] == login.password:
            return {"message": "Login successful"}

    return {"message": "Invalid email or password"}
# ---------- order ENDPOINTS ----------

@app.post("/orders")
def create_order(order: Order):
    database_app.add_order(
        order.customer_id,
        order.product_id,
        order.quantity
    )
    return {"message": "Order created"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)