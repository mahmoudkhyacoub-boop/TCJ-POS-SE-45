from pathlib import Path
import ast

source_path = Path(__file__).with_name("main.py")
source = source_path.read_text(encoding="utf-8")
ast.parse(source, filename=str(source_path))

required_methods = {
    "ui_analytics", "ui_financial_liquidity_view", "ui_financial_position",
    "ui_pos", "ui_maintenance", "ui_transfers", "ui_inventory", "ui_purchases",
    "open_inventory_adjustment", "ui_customers", "ui_debts", "ui_loyalty",
    "ui_service_register", "ui_operations_management", "ui_advanced_reports",
    "ui_reports", "ui_balance_reconciliation", "ui_internal_transfers",
    "ui_sponsors", "ui_expenses", "ui_audit_logs", "ui_settings",
}
for method in required_methods:
    assert f"def {method}(" in source, f"Missing callback: {method}"

assert 'add_nav_group("نظرة المدير"' in source
assert 'add_nav_group("المخزون والمشتريات"' in source
assert '("مرتجع / تالف", self.open_inventory_adjustment)' in source
assert 'def _post_journal_entry(' in source
assert 'def _void_journals_for_record(' in source
assert 'def _operational_account_net(' in source
assert 'def checkout(self):' in source
assert 'def add_purchase(self):' in source
assert 'def add_maintenance(self):' in source
assert 'def add_transfer(self):' in source
manager_block = source.split('else:\n            # Deliberate manager order:', 1)[1].split('\n\n        # Content shell', 1)[0]
assert manager_block.count('(\"قسم الصيانة\", self.ui_maintenance)') == 1
assert manager_block.count('(\"سجل استلام وتسليم الأجهزة\", self.ui_service_register)') == 1
print("V159 manager navigation passed: reordered manager UI keeps original callbacks and no duplicates")
