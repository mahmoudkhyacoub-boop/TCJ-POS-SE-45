from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import main

sample = "هل تريد إرسال الفاتورة وتفاصيل الولاء للعميل mk عبر واتساب فوراً؟"
formatted = main.format_dialog_arabic(sample)
if "mk" not in formatted:
    raise AssertionError(f"Latin client name disappeared from formatted dialog: {formatted!r}")
if "\x01" in formatted:
    raise AssertionError("Old replacement-control-character bug remains")

sample_contract = "ترند سنتر الأردن\nTREND CENTER JORDAN\nإيصال استلام جهاز رقم: SR-20260825-1300\nالعميل: mk"
formatted_contract = main.format_dialog_arabic(sample_contract)
for expected in ("TREND", "CENTER", "JORDAN", "SR-20260825-1300", "mk"):
    if expected not in formatted_contract:
        raise AssertionError(f"Contract text fragment disappeared: {expected!r} -> {formatted_contract!r}")

source = Path(__file__).with_name("main.py").read_text(encoding="utf-8")
for expected in (
    'f"{order[1]}_{kind}.png"',
    "def _service_register_copy_png(self, path, notify=True):",
    "def _service_register_open_png(self, path):",
    "نسخ PNG وفتح WhatsApp",
):
    if expected not in source:
        raise AssertionError(f"Missing PNG contract capability: {expected}")

print("V145 WhatsApp mixed-text and PNG contract checks passed.")
