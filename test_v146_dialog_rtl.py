from pathlib import Path
import sys

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
import main

source = (ROOT / "main.py").read_text(encoding="utf-8")

# The two central themed dialogs must use one formatter, not a second shaping pass.
for marker in (
    'def format_dialog_arabic(text):',
    'get_display(reshaped, base_dir="R")',
    'ctk.CTkLabel(frame, text=str(message or "")',
):
    if marker not in source:
        raise AssertionError(f"Missing global dialog RTL guard: {marker}")

if 'messagebox.showwarning(' in source:
    raise AssertionError('A native warning dialog bypasses the themed RTL path')
formatter_block = source.split('def format_dialog_arabic(text):', 1)[1].split('def hash_password', 1)[0]
if 'if _has_visual_arabic(raw): return raw' not in formatter_block:
    raise AssertionError('Dialog formatter is not idempotent for already-shaped Arabic text')
if 'ctk.CTkLabel(frame, text=str(message or "")' not in source:
    raise AssertionError('Customer-facing dialogs still pre-shape the message text')
if 'lambda match: "\\u200f"' in formatter_block or '"\\1"' in formatter_block:
    raise AssertionError('Legacy control-character replacement remains in the active formatter')

samples = [
    "هل تريد إرسال الفاتورة وتفاصيل الولاء للعميل mk عبر واتساب فوراً؟",
    "تنبيه مهم بخصوص العميل (0795552671):\\n\\nملاحظة تجريبية",
    "هل تريد إغلاق الفترة 2026-08 وترحيل الأرصدة؟",
]
for raw in samples:
    formatted = main.format_dialog_arabic(raw)
    if "\\x01" in formatted:
        raise AssertionError(f"Control character remains: {formatted!r}")
    for fragment in ("mk", "0795552671", "2026-08"):
        if fragment in raw and fragment not in formatted:
            raise AssertionError(f"Mixed fragment disappeared: {fragment!r} -> {formatted!r}")

print("V146 global dialog RTL checks passed.")
