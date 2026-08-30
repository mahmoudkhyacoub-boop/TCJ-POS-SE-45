import sqlite3
from types import SimpleNamespace
import main

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.executescript('''
CREATE TABLE customers (id INTEGER PRIMARY KEY, phone TEXT UNIQUE, name TEXT, points INTEGER DEFAULT 0);
CREATE TABLE sales (id INTEGER PRIMARY KEY, customer_phone TEXT);
CREATE TABLE maintenance (id INTEGER PRIMARY KEY, client_phone TEXT);
CREATE TABLE transfers (id INTEGER PRIMARY KEY, client_phone TEXT);
CREATE TABLE customer_debts (id INTEGER PRIMARY KEY, customer_phone TEXT);
CREATE TABLE customer_notes (phone TEXT PRIMARY KEY, note TEXT, updated_at TEXT);
INSERT INTO customers(phone,name,points) VALUES ('0781250823','سلامة مهدي',22);
INSERT INTO sales(customer_phone) VALUES ('0781250823');
INSERT INTO maintenance(client_phone) VALUES ('0781250823');
''')
fake = SimpleNamespace(db=SimpleNamespace(conn=conn, cursor=cur))
ok, msg = main.TrendCenterApp._persist_customer_edit(fake, 1, '0781250823', 22, 'اسم معدل', '0799999999')
assert ok, msg
saved = cur.execute('SELECT phone,name,points FROM customers WHERE id=1').fetchone()
assert saved == ('0799999999', 'اسم معدل', 22), saved
assert cur.execute('SELECT customer_phone FROM sales').fetchone()[0] == '0799999999'
assert cur.execute('SELECT client_phone FROM maintenance').fetchone()[0] == '0799999999'
print('direct_customer_save=PASS')
print('points_preserved=PASS')
print('linked_records_updated=PASS')
