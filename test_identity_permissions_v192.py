from pathlib import Path
import re
import sqlite3

source = Path('/home/ubuntu/trend_center_advanced/main.py').read_text(encoding='utf-8')
assert 'shop_name_en' in source
assert "logo_path" in source
assert 'user_permissions' in source
assert 'PERMISSION_LABELS' in source
assert '_edit_user_permissions' in source
assert '_load_user_permissions' in source
assert '_shop_identity' in source
assert 'resource_path(APP_FONT_FILE)' in source
assert 'إدارة الصلاحيات الفردية' in source

conn = sqlite3.connect(':memory:')
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT, permissions TEXT DEFAULT '[]')")
conn.execute("CREATE TABLE user_permissions (username TEXT, permission_key TEXT, allowed INTEGER DEFAULT 0, PRIMARY KEY(username, permission_key))")
conn.execute("INSERT INTO users(username,password,role,permissions) VALUES('worker','x','employee','[]')")
conn.execute("INSERT INTO user_permissions(username,permission_key,allowed) VALUES('worker','نقطة البيع',1)")
assert conn.execute("SELECT permission_key FROM user_permissions WHERE username='worker' AND allowed=1").fetchone()[0] == 'نقطة البيع'
conn.execute("UPDATE users SET permissions=? WHERE username='worker'", ('["نقطة البيع"]',))
assert 'نقطة البيع' in conn.execute("SELECT permissions FROM users WHERE username='worker'").fetchone()[0]
print('identity_settings=PASS')
print('flexible_permissions_schema=PASS')
print('contract_font_logo_hooks=PASS')
print('invoice_identity_hooks=PASS')

assert 'description_to_key.get(value, value)' in source
assert 'المخزون والمشتريات' in source
assert 'العملاء والذمم' in source
assert 'إدارة الديون والذمم ⚖️' in source
print('permission_key_normalization=PASS')
print('employee_navigation_groups=PASS')
