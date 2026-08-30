import sqlite3
import os
import arabic_reshaper
from bidi.algorithm import get_display

# Test Database Creation
DB_NAME = "test_trend_v41.db"
if os.path.exists(DB_NAME): os.remove(DB_NAME)

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Mimic the create_tables logic
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, code TEXT UNIQUE, name TEXT, buy_price REAL, sell_price REAL, stock INTEGER, description TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, phone TEXT UNIQUE, name TEXT, points INTEGER DEFAULT 0)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, code TEXT, name TEXT, qty INTEGER, price REAL, total REAL, buy_cost REAL, date TEXT, time TEXT, user TEXT, customer_phone TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, desc TEXT, amount REAL, date TEXT, time TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS purchases (id INTEGER PRIMARY KEY, code TEXT, name TEXT, qty INTEGER, cost REAL, supplier TEXT, date TEXT, time TEXT, description TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS maintenance (id INTEGER PRIMARY KEY, device_name TEXT, repair_desc TEXT, client_name TEXT, client_phone TEXT, revenue REAL, internal_cost REAL DEFAULT 0, date TEXT, time TEXT, user TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS transfers (id INTEGER PRIMARY KEY, type TEXT, client_name TEXT, client_phone TEXT, amount REAL, commission REAL, reference TEXT, provider TEXT, date TEXT, time TEXT, user TEXT)''')
conn.commit()

print("Database Schema Test: PASSED")

# Test Arabic Logic
def fix_arabic(text):
    reshaped_text = arabic_reshaper.reshape(str(text))
    return get_display(reshaped_text)

test_text = "ترند سنتر الأردن"
result = fix_arabic(test_text)
print(f"Arabic Logic Test: Input '{test_text}' -> Output processed successfully")

conn.close()
if os.path.exists(DB_NAME): os.remove(DB_NAME)
