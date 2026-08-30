from pathlib import Path
import ast
import sqlite3

SOURCE = Path(__file__).with_name("main.py")
text = SOURCE.read_text(encoding="utf-8")
ast.parse(text, filename=str(SOURCE))

for fragment, label in [
    ("purchase_returns = scalar(\"SELECT COALESCE(SUM(qty * unit_cost),0) FROM inventory_adjustments WHERE adjustment_type='مرتجع شراء'\")", "purchase return report total"),
    ("purch_net = max(purch - purchase_returns, 0.0)", "net purchase formula"),
    ('("إجمالي المشتريات (قبل المرتجعات)", purch, COLOR_WHITE)', "gross purchase report row"),
    ('("مرتجعات المشتريات", purchase_returns, COLOR_PUMPKIN_ORANGE)', "purchase return report row"),
    ('("صافي المشتريات بعد المرتجعات", purch_net, COLOR_WHITE)', "net purchase report row"),
]:
    assert fragment in text, f"Missing {label}"

conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE purchases(qty REAL, cost REAL);
CREATE TABLE inventory_adjustments(adjustment_type TEXT, qty REAL, unit_cost REAL);
""")
conn.execute("INSERT INTO purchases VALUES (2,5)")
conn.execute("INSERT INTO inventory_adjustments VALUES ('مرتجع شراء',1,5)")
gross = conn.execute("SELECT COALESCE(SUM(qty*cost),0) FROM purchases").fetchone()[0]
returns = conn.execute("SELECT COALESCE(SUM(qty*unit_cost),0) FROM inventory_adjustments WHERE adjustment_type='مرتجع شراء'").fetchone()[0]
assert gross == 10 and returns == 5 and max(gross - returns, 0) == 5
conn.close()
print("V157 purchase report check passed: gross purchases 10, returns 5, net purchases 5")
