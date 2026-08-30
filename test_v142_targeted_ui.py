from pathlib import Path

SOURCE = Path(__file__).with_name('main.py').read_text(encoding='utf-8')


def require(fragment: str, label: str) -> None:
    if fragment not in SOURCE:
        raise AssertionError(f'Missing {label}: {fragment}')


# The sales labels highlighted in the supplied screenshot must be white.
for label in ('هاتف العميل:', 'الاسم:', 'الدفع:', 'الباركود:'):
    require(f'fix_arabic("{label}", for_ui=True), font=FONT_BOLD, text_color=COLOR_WHITE', f'white sales label {label}')

# Maintenance, transfer and purchase labels highlighted in the supplied screenshots.
require('fix_arabic("تكلفة القطعة:", for_ui=True), font=FONT_BOLD, text_color=COLOR_WHITE', 'white maintenance cost label')
require('fix_arabic("مصدر التمويل:", for_ui=True), font=FONT_BOLD, text_color=COLOR_WHITE', 'white funding label')
require('fix_arabic("إجمالي الفاتورة: 0.00", for_ui=True), font=FONT_BOLD, text_color=COLOR_WHITE', 'white purchase total label')
require('COLOR_PUMPKIN_ORANGE = "#FF9F1C"', 'Pumpkin Orange token')

# The sales total is intentionally larger and white; this is a presentation-only change.
require('self.total_lbl = ctk.CTkLabel(bottom, text=fix_arabic(f"المجموع: 0.00 {CURRENCY}", for_ui=True), font=FONT_NET_PROFIT_LABEL, text_color=COLOR_WHITE)', 'large white sales total')

# Exactly the requested report metrics use Pumpkin Orange; other values remain white.
for label in ('قيمة المنتجات المباعة (من رأس المال - COGS)', 'تكلفة قطع الصيانة', 'إجمالي المصاريف'):
    require(f'("{label}",', f'report metric {label}')
require('text_color=(COLOR_PUMPKIN_ORANGE if label in ("قيمة المنتجات المباعة (من رأس المال - COGS)", "تكلفة قطع الصيانة", "إجمالي المصاريف", "مرتجعات المشتريات") else COLOR_WHITE)', 'targeted report value color')

# Keep core accounting paths present and untouched.
for marker in ('def checkout(self):', 'def add_purchase(self):', 'def add_maintenance(self):', 'def add_transfer(self):', 'def _post_journal_entry(', 'def delete_operation_record(self):'):
    require(marker, f'core operation {marker}')

print('V142 targeted UI assertions passed.')
