import re
import sqlite3
from pathlib import Path

source = Path('main.py').read_text(encoding='utf-8')
assert 'producing `WHERE ... WHERE ...`' in source
assert 're.search(r"\\bWHERE\\b", query, re.IGNORECASE)' in source

conn = sqlite3.connect(':memory:')
conn.execute('CREATE TABLE expenses (amount REAL, date TEXT, status TEXT)')
conn.executemany('INSERT INTO expenses VALUES (?,?,?)', [(10, '2026-08-26', 'paid'), (4, '2026-08-27', 'unpaid')])
where = 'WHERE date >= ? AND date <= ?'
query = "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE LOWER(TRIM(COALESCE(status,'paid'))) NOT IN ('unpaid','pending','credit','غير مسدد','على الحساب')"
suffix = (' AND ' + where[6:]) if re.search(r'\bWHERE\b', query, re.IGNORECASE) else (' ' + where)
value = conn.execute(query + suffix, ('2026-08-26', '2026-08-26')).fetchone()[0]
assert value == 10
print('V163 report date filter passed: existing WHERE receives AND date predicates')
