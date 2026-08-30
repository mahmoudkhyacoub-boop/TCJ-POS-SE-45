from pathlib import Path

source = Path("main.py").read_text(encoding="utf-8")
assert 'APP_FONT_FAMILY' in source
assert 'FONT_BOLD = (APP_FONT_FAMILY, 14, "bold")' in source
assert 'FONT_NORMAL_BOLD = (APP_FONT_FAMILY, 14, "bold")' in source
assert 'HEADER_FONT_WHITE = (APP_FONT_FAMILY, 14, "bold")' in source
assert 'FONT_BOLD = ("Arial", 14, "bold")' not in source
assert 'FONT_NORMAL_BOLD = ("Arial", 14, "bold")' not in source
print("V168 UI font passed: Cocon family is used by interface constants without Arial override")
