# create connection

import sqlite3
from datetime import datetime
 
 
DB_NAME = "greenfield_system.db"
 
 

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
# create tables function - define primary keys, foreign keys and constraints

 
def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS categories")
    cursor.execute("DROP TABLE IF EXISTS customers")
 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    )
    """)
 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category_id INTEGER,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        description TEXT,
        created_at TEXT,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    """)
 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        phone_number TEXT,
        home_address TEXT,
        created_at TEXT
)
""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        created_at TEXT
    )
    """)

    connection.commit()
    connection.close()


# add categories, add customers, add products functions

def add_category(name, description):
    connection = get_connection()
    cursor = connection.cursor()
 
    cursor.execute(
        "INSERT INTO categories (name, description) VALUES (?, ?)",
        (name, description)
    )
 
    connection.commit()
    connection.close()



def add_product(name, category_id, price, stock, description):
    connection = get_connection()
    cursor = connection.cursor()
 
    cursor.execute(
        """
        INSERT INTO products 
        (name, category_id, price, stock, description, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, category_id, price, stock, description, datetime.now().isoformat())
    )
 
    connection.commit()
    connection.close()



def add_customer(email, password, full_name, phone_number, home_address):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO customers
        (email, password, full_name, phone_number, home_address, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
    (email, password, full_name, phone_number, home_address, datetime.now().isoformat()))

    connection.commit()
    connection.close()

def add_order(customer_id, product_id, quantity):
    connection = get_connection()
    cursor = connection.cursor()

    # Check if product exists and get stock
    cursor.execute(
        "SELECT stock FROM products WHERE id = ?",
        (product_id,)
    )
    result = cursor.fetchone()

    if not result:
        connection.close()
        raise Exception("Product not found")

    stock = result[0]

    # Check if enough stock
    if quantity > stock:
        connection.close()
        raise Exception("Not enough stock")

    # Insert order
    cursor.execute(
        """
        INSERT INTO orders (customer_id, product_id, quantity, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (customer_id, product_id, quantity, datetime.now().isoformat())
    )

    # Reduce stock
    cursor.execute(
        """
        UPDATE products
        SET stock = stock - ?
        WHERE id = ?
        """,
        (quantity, product_id)
    )

    connection.commit()
    connection.close()
    
        

# Fetching data from all table - get categories, get products, get customers

def get_categories():
    connection = get_connection()
    cursor = connection.cursor()
 
    cursor.execute("SELECT * FROM categories") #displays all columns of categories
    data = cursor.fetchall() 
 
    connection.close()
    return data

def get_customers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()

    connection.close()
    return data
 
    

def get_products_with_categories(category_id=None):
    connection = get_connection()
    cursor = connection.cursor()

    if category_id:
        cursor.execute("""
        SELECT products.id,
               products.name,
               categories.name,
               products.price,
               products.stock
        FROM products
        JOIN categories ON products.category_id = categories.id
        WHERE products.category_id = ?
        """, (category_id,))
    else:
        cursor.execute("""
        SELECT products.id,
               products.name,
               categories.name,
               products.price,
               products.stock
        FROM products
        JOIN categories ON products.category_id = categories.id
        """)

    data = cursor.fetchall()
    connection.close()
    return data


if __name__ == "__main__":
    create_tables()


    add_category("fruits", "fresh fruits")
    add_category("veg", "fresh veg")
    add_category("meats", "fresh meats")
    add_category("fish", "fresh fish")
    add_category("dairy", "fresh dairy")
    add_category("vegan", "vegan options")
    add_category("staples", "fresh staples")


    # add_category("groceries", "salads&veggies")
    add_product("Oranges", 1, 2.99, 30, "fruits")
    add_product("apple", 1, 1.50, 15, "fruits")
    add_product("banana", 1, 1.20, 30, "fruits")
    add_product("grapes", 1, 2.25, 100, "fruits")
    add_product("pear", 1, 2.50, 100, "fruits")
    add_product("mango", 1, 4.50, 100, "fruits")
    add_product("watermelon", 1, 5.00, 40, "fruits")
    add_product("pineapple", 1, 5.50, 30, "fruits")

    add_product("cabbage", 2, 2.97, 30, "veg")
    add_product("lettuce", 2, 0.50, 200, "veg")
    add_product("carrot", 2, 1.00, 150, "veg")
    add_product("tomato", 2, 1.00, 150, "veg")
    add_product("cucumber", 2, 1.20, 150, "veg")
    add_product("beetroot", 2, 1.00, 150, "veg")

    add_product("beef", 3, 11.00, 50, "meats" )
    add_product("lamb", 3, 12.00, 50, "meats" )
    add_product("pork", 3, 4.00, 50, "meats" )
    add_product("chicken", 3, 4.99, 50, "meats")
    add_product("bacon", 3, 7.00, 50, "meats")

    add_product("salmon", 4, 13.00, 50, "fish")
    add_product("prawns", 4, 10.00, 50, "fish")
    add_product("cod", 4, 9.00, 50, "fish")

    add_product("milk", 5, 1.00, 150, "dairy")
    add_product("cheese", 5, 7.00, 150, "dairy")
    add_product("eggs", 5, 2.50, 150, "dairy")
    add_product("butter", 5, 11.00, 150, "dairy")

    add_product("tofu", 6, 3.00, 20, "vegan")
    add_product("seitan", 6, 2.50, 20, "vegan")
    add_product("oat milk", 6, 2.25, 20, "vegan")
    add_product("vegan sausages", 6, 3.50, 20, "vegan")
    add_product("vegan mince", 6, 3.00, 20, "vegan")

    add_product("bread", 7, 1.25, 150, "staples")
    add_product("pasta", 7, 1.15, 150, "staples")
    add_product("rice", 7, 2.25, 150, "staples")
    add_product("flour", 7, 1.25, 150, "staples")






    


    add_customer("greeshma@gmail.com", "Greeshma", "Halesh", "Bangalore", "India")
    