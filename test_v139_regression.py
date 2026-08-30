from pathlib import Path
import ast

ROOT = Path(__file__).parent
SOURCE = ROOT / "main.py"
text = SOURCE.read_text(encoding="utf-8")
ast.parse(text, filename=str(SOURCE))

required = {
    "version": 'APP_VERSION = "V139',
    "delete_purchase_reads_funding": 'SELECT code, qty, cost, supplier, funding_source FROM purchases WHERE id=?',
    "delete_purchase_ap_guard": 'if row[3] and self._ledger_account_for_payment(row[4]) == "AP":',
    "duplicate_migration_removed": 'self._ensure_column("purchases", "funding_source", "TEXT DEFAULT \'صندوق المحل (نقدي)\'")\n        self.cursor.execute',
    "cliq_detail_snapshot": '"cliq", "CLIQ (تفصيل ضمن BANK)"',
    "bank_total_snapshot": '"bank", "الحساب البنكي الإجمالي"',
    "cliq_detail_reconciliation": 'تفصيل حركة CLIQ (ضمن الحساب البنكي):',
}
missing = [key for key, snippet in required.items() if snippet not in text]
if missing:
    raise AssertionError(f"Missing V139 regression requirements: {missing}")

# The old unsafe deletion branch must not remain.
assert 'if row[3]: self.db.cursor.execute("UPDATE suppliers SET balance=MAX(0, balance-?) WHERE name=?"' not in text
# The migration call must occur only once.
assert text.count('self._ensure_column("purchases", "funding_source"') == 1
print("V139 regression checks passed: AP-only purchase deletion, V139 versioning, and BANK/CLIQ display safeguards.")
