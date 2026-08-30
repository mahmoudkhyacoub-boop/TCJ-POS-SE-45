import importlib.util
from pathlib import Path

ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location("tcj_v148_rtl", ROOT / "main.py")
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)

samples = [
    "تم تسجيل العميل بنجاح!\nتم منح العميل 20 نقطة هدية مجانية.",
    "هل تريد إرسال الفاتورة وتفاصيل الولاء للعميل mk عبر واتساب فوراً؟",
    "مرحباً بك يا mk\nشكراً لثقتك وزيارتك لـ ترند سنتر الأردن.",
]

for raw in samples:
    once = main.format_dialog_arabic(raw)
    twice = main.format_dialog_arabic(once)
    # A second formatter pass must be a no-op for already-shaped presentation
    # text. The customer-facing dialogs themselves use raw logical Unicode.
    assert twice == once, (raw, once, twice)
    assert "\u202e" not in twice and "\u202d" not in twice and "\u202c" not in twice

source = (ROOT / "main.py").read_text(encoding="utf-8")
assert "def _has_visual_arabic" in source
assert "base_dir=\"R\"" in source
assert "def format_dialog_arabic" in source
assert "ctk.CTkLabel(frame, text=str(message or \"\")" in source

print("V148 RTL idempotence checks passed for customer registration and WhatsApp mixed text.")
