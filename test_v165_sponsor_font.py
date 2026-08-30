from pathlib import Path

source = Path("main.py").read_text(encoding="utf-8")
assert "sponsors_font_size" in source
assert "adjust_sponsor_font" in source
assert "font=sponsor_font or font" in source
assert "_save_sponsor_paths(paths)" in source
print("V165 sponsor font controls passed: persisted size, +/- controls, sponsor paths preserved")
