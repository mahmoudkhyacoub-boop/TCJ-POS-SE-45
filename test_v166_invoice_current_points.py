from pathlib import Path

source = Path("main.py").read_text(encoding="utf-8")
assert 'نقاطك الحالية:' in source
assert 'SELECT points FROM customers WHERE phone=?' in source
assert 'النقاط المكتسبة:' in source
assert 'font=sponsor_font or font' in source
assert 'self._save_sponsor_paths(paths)' in source
print("V166 invoice current points passed: invoice display and sponsor paths preserved")
