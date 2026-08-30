from pathlib import Path

text = Path(__file__).with_name("main.py").read_text(encoding="utf-8")

# Sales returns must account for previous returns and reject excess quantity.
assert "returned_qty = int(self.db.cursor.execute" in text
assert "remaining_qty = sold_qty - returned_qty" in text
assert "if q > remaining_qty:" in text
assert "تم إرجاع كامل كمية عملية البيع سابقاً" in text

# Purchase returns must reject excess stock and must not silently clamp it.
assert "if q > stock:" in text
assert "كمية مرتجع الشراء أكبر من المخزون المتاح" in text
assert "UPDATE products SET stock=stock-? WHERE code=?" in text
assert "UPDATE products SET stock=MAX(0,stock-?)" not in text

# AP purchase identity must be normalized before balance/debt writes.
ap_block = text[text.index("purchase_credit_account = self._ledger_account_for_payment(funding_source)"):text.index("self._post_journal_entry(\"purchase\"", text.index("purchase_credit_account = self._ledger_account_for_payment(funding_source)"))]
assert ap_block.index("supplier_input = sup_input") < ap_block.index("UPDATE suppliers SET balance = balance + ?")
assert ap_block.index("UPDATE suppliers SET balance = balance + ?") < ap_block.index("INSERT INTO supplier_debts")
assert "supplier_phone = supplier_input if supplier_input.isdigit() else None" in ap_block

# Supplier debt payment must reduce the matching supplier balance in the same path.
pay_block = text[text.index("supplier_name_for_balance = None"):text.index("self.db.cursor.execute(\"INSERT INTO debt_payments", text.index("supplier_name_for_balance = None"))]
assert "SELECT supplier_name FROM supplier_debts WHERE id=?" in pay_block
assert "UPDATE suppliers SET balance=MAX(0, balance-?) WHERE name=?" in pay_block

print("V151 accounting guard tests passed: cumulative sales returns, bounded purchase returns, normalized AP supplier identity, and supplier balance payment sync")
