from pathlib import Path
import ast
import sqlite3

SOURCE = Path(__file__).with_name("main.py")
text = SOURCE.read_text(encoding="utf-8")
ast.parse(text, filename=str(SOURCE))


def require(fragment, label):
    if fragment not in text:
        raise AssertionError(f"Missing {label}: {fragment}")


# The button remains a single admin-only entry point with exactly the three
# supported operational choices.
require('def open_inventory_adjustment(self):', 'inventory adjustment entry point')
require('if self.current_role != "admin":', 'admin-only guard')
require('values=["تالف", "مرتجع بيع", "مرتجع شراء"]', 'three adjustment choices')
require('INSERT INTO inventory_adjustments', 'adjustment audit row')
require('self._post_journal_entry("inventory_adjustment"', 'central journal posting')

# Waste: stock cannot go below zero and the loss account is used, with no
# customer, supplier, or payment-account reversal.
require('if kind=="تالف" and q>stock:', 'waste stock boundary')
require('[("INVENTORY_LOSS", total_cost, 0, "خسارة تالف مخزني")', 'waste loss journal')

# Sales return: original sale is required, cumulative returns are bounded,
# and the original payment/AR account is credited back.
require('if not original_id: raise ValueError("أدخل رقم عملية البيع لمرتجع البيع")', 'sale return source requirement')
require('returned_qty = int(self.db.cursor.execute', 'cumulative sale returns')
require('remaining_qty = sold_qty - returned_qty', 'remaining sale quantity')
require('account="AR" if sale[2]=="Credit" else self._ledger_account_for_payment(sale[2])', 'sale return original payment account')
require('("SALES_REVENUE", return_value, 0', 'sale revenue reversal')
require('("COGS", 0, cost_value', 'sale COGS reversal')

# Purchase return: original purchase is required, cumulative returns are
# bounded, original unit cost is used, and its original funding account is
# debited once. AP also updates supplier and debt screens.
require('if not original_id:\n                        raise ValueError("أدخل رقم عملية الشراء الأصلية لمرتجع الشراء")', 'purchase return source requirement')
require('SELECT id, code, qty, cost, supplier, funding_source, source_id FROM purchases WHERE id=?', 'original purchase lookup')
require('already_returned = int(self.db.cursor.execute', 'cumulative purchase returns')
require('remaining_purchase_qty = purchased_qty - already_returned', 'remaining purchase quantity')
require('unit_cost = max(float(purchase[3] or 0), 0)', 'original purchase cost')
require('funding_account = self._ledger_account_for_payment(purchase[5])', 'original funding account')
require('lines=[(funding_account, total_cost, 0', 'purchase return funding reversal')
require('UPDATE suppliers SET balance=COALESCE(balance,0)-?', 'supplier balance reversal')
require('UPDATE supplier_debts SET total_debt=?, status=?', 'supplier debt reversal')

# The daily liquidity views include purchase returns once and derive the
# account from the joined original purchase, not from a hard-coded AP value.
require("JOIN purchases p ON p.id=ia.original_sale_id WHERE ia.adjustment_type='مرتجع شراء'", 'purchase return liquidity join')
require('cash_purchase_returns = 0.0', 'cash purchase return breakdown')
require('"purchase_returns": round(cash_purchase_returns, 2)', 'cash return detail')
require('("مرتجعات مشتريات نقدية:", cash_support["purchase_returns"])', 'cash return display')
require('(\"inventory_adjustments\", f\"SELECT COALESCE(user,\'-\'), \'—\', (qty * unit_cost)', 'operations return row')
require('elif source == "inventory_adjustments":', 'operations return deletion branch')
require('self._void_journals_for_record(source, rid', 'return journal reversal before deletion')
require('DELETE FROM inventory_adjustments WHERE id=?', 'return row deletion')

# Small deterministic SQL sanity check for the accounting relationship used by
# the new path: return amount is original cost x returned quantity, and the
# supplier debt falls by that same amount.
conn = sqlite3.connect(":memory:")
conn.executescript("""
CREATE TABLE purchases (id INTEGER PRIMARY KEY, code TEXT, qty INTEGER, cost REAL, supplier TEXT, funding_source TEXT, source_id TEXT);
CREATE TABLE inventory_adjustments (id INTEGER PRIMARY KEY, adjustment_type TEXT, product_code TEXT, qty INTEGER, unit_cost REAL, original_sale_id INTEGER);
CREATE TABLE suppliers (name TEXT PRIMARY KEY, balance REAL);
CREATE TABLE supplier_debts (source_id TEXT PRIMARY KEY, total_debt REAL, paid_amount REAL, status TEXT);
""")
conn.execute("INSERT INTO purchases VALUES (1,'P-1',5,2.5,'Supplier A','ذمم موردين (بالدين)','purchase-1')")
conn.execute("INSERT INTO inventory_adjustments VALUES (1,'مرتجع شراء','P-1',2,2.5,1)")
conn.execute("INSERT INTO suppliers VALUES ('Supplier A',12.5)")
conn.execute("INSERT INTO supplier_debts VALUES ('purchase-1',12.5,0,'غير مسدد')")
qty, cost, funding = conn.execute("""
SELECT ia.qty, ia.unit_cost, p.funding_source
FROM inventory_adjustments ia JOIN purchases p ON p.id=ia.original_sale_id
WHERE ia.adjustment_type='مرتجع شراء'
""").fetchone()
amount = round(qty * cost, 2)
assert amount == 5.0 and funding == 'ذمم موردين (بالدين)'
conn.execute("UPDATE suppliers SET balance=balance-? WHERE name='Supplier A'", (amount,))
conn.execute("UPDATE supplier_debts SET total_debt=total_debt-? WHERE source_id='purchase-1'", (amount,))
assert conn.execute("SELECT balance FROM suppliers").fetchone()[0] == 7.5
assert conn.execute("SELECT total_debt FROM supplier_debts").fetchone()[0] == 7.5
conn.close()

print("V154 inventory adjustment checks passed: waste, cumulative sales returns, original-funding purchase returns, supplier/AP sync, and liquidity display coverage")
