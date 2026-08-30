from pathlib import Path

source = Path("main.py").read_text(encoding="utf-8")
block = source[source.index("    def ui_reports"):source.index("    def refresh_reports")]
assert block.index('text=fix_arabic("من:", for_ui=True)') < block.index('text=fix_arabic("إلى:", for_ui=True)')
assert 'self.rep_from' in block and 'self.rep_to' in block
print("V164 report field order passed: من right, إلى left")
