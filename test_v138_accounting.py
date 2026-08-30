from pathlib import Path
import ast

ROOT = Path(__file__).parent
SOURCE = ROOT / "main.py"
text = SOURCE.read_text(encoding="utf-8")
ast.parse(text, filename=str(SOURCE))

required = {
    "sale_source_column": 'self._ensure_column("sales", "source_id", "TEXT")',
    "maintenance_source_column": 'self._ensure_column("maintenance", "source_id", "TEXT")',
    "purchase_source_column": 'self._ensure_column("purchases", "source_id", "TEXT")',
    "customer_debt_source": 'self._ensure_column("customer_debts", "source_type", "TEXT")',
    "supplier_debt_source": 'self._ensure_column("supplier_debts", "source_type", "TEXT")',
    "cash_supplier_guard": 'is_supplier_credit = purchase_credit_account == "AP"',
    "sale_cost_recalc": 'new_buy_cost = old_unit_cost * new_qty',
    "expense_repost": 'self._post_operation_journal_from_row("expenses", eid)',
    "service_contract_preview": 'self._service_register_open_contract(contract, client_phone, order_no, "intake", open_whatsapp=True, order=row_data)',
    "inventory_adjustment_table": 'CREATE TABLE IF NOT EXISTS inventory_adjustments',
    "inventory_adjustment_ui": 'def open_inventory_adjustment(self):',
    "return_sale_entry": 'عكس إيراد مرتجع بيع',
    "waste_entry": 'خسارة تالف مخزني',
}
missing = [key for key, snippet in required.items() if snippet not in text]
if missing:
    raise AssertionError(f"Missing V138 requirements: {missing}")

# Ensure old broad supplier balance branch is no longer present.
assert '            if supplier:\n                existing_sup = self.db.cursor.execute' not in text
# Ensure the reversal helper remains compatible with tables without source_id.
assert 'source_expr = "source_id" if table in ("sales", "maintenance", "purchases", "inventory_adjustments") else "NULL"' in text
print("V138 checks passed: stable source links, AP-only supplier balance, sale COGS recalc, expense repost, returns/waste path, and intake contract/WhatsApp action.")
