from pathlib import Path

SOURCE = Path(__file__).with_name("main.py").read_text(encoding="utf-8")

assert 'add_nav_group("نظرة المدير", [("لوحة التحكم والتحليلات", self.ui_analytics), ("التقارير والأرباح", self.ui_reports)' in SOURCE
assert 'add_nav_group("العمليات اليومية", [("نقطة البيع", self.ui_pos), ("قسم الصيانة", self.ui_maintenance), ("حوالات وفواتير", self.ui_transfers)]' in SOURCE
assert 'add_nav_group("الصيانة والأجهزة", [("سجل استلام وتسليم الأجهزة", self.ui_service_register)]' in SOURCE
assert SOURCE.count('(\"التقارير والأرباح\", self.ui_reports)') == 1
assert SOURCE.count('(\"قسم الصيانة\", self.ui_maintenance)') == 2
assert 'notes._textbox.configure(font=FONT_NORMAL_BOLD, justify="right", wrap="word")' in SOURCE
assert 'notes._textbox.tag_configure("rtl", justify="right")' in SOURCE
print("V161 UI navigation and intake RTL checks passed")
