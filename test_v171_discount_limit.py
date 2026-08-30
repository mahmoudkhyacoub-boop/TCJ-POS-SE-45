from pathlib import Path

source = Path(__file__).with_name('main.py').read_text(encoding='utf-8')

assert 'target_margin = 0.40' in source
assert 'maximum_discount = max(original_price - minimum_price, 0.0)' in source
assert 'allowed_discount = round(maximum_discount * 0.70, 2)' in source
assert 'if maximum_discount < 0.50:' in source
assert 'قيمة الخصم المتاحة:' in source
assert 'لا يمكن عمل خصم؛ قيمة أقصى خصم أقل من 0.50 دينار' in source
assert 'minimum_allowed_price = original_price - allowed_discount' in source
print('V171 discount limit checks passed: 70% display, target-margin guard, and minimum threshold')
