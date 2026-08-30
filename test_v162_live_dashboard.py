from pathlib import Path
s = Path('main.py').read_text(encoding='utf-8')
assert 'def ui_live_operations_dashboard(self):' in s
assert 'self.ui_live_operations_dashboard() if self.current_role == "admin" else self.ui_pos()' in s
assert 'SELECT code, name, stock, COALESCE(min_stock, 3) FROM products' in s
assert 'WHERE COALESCE(stock,0) <= COALESCE(min_stock,3)' in s
assert 'state = "نافد" if stock <= 0 else "حرج"' in s
assert 'self.after(15000' in s
assert 'لا يتم إنشاء قيود أو تعديل أرصدة' in s
print('V162 live dashboard checks passed')
