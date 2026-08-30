import os
import shutil
import sqlite3
import tempfile
from pathlib import Path

source = Path('/home/ubuntu/trend_center_v57.db')
with tempfile.TemporaryDirectory() as tmp:
    target = Path(tmp) / 'trend_center_v57.db'
    shutil.copy2(source, target)
    before = target.stat().st_size
    os.chdir(tmp)
    import sys
    sys.path.insert(0, '/home/ubuntu/trend_center_advanced')
    import main
    db = main.Database()
    after = target.stat().st_size
    cur = db.cursor
    required = {
        'transfers': {'payment_method', 'collection_account', 'settlement_account', 'settlement_amount'},
        'supplier_debts': {'debt_reference'},
        'journal_entries': {'status'},
    }
    for table, columns in required.items():
        actual = {row[1] for row in cur.execute(f'PRAGMA table_info({table})')}
        missing = columns - actual
        assert not missing, (table, missing)
    counts = {}
    for table in ['sales','purchases','maintenance','expenses','transfers','customer_debts','supplier_debts']:
        counts[table] = cur.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
    print('compatibility migration passed; bytes before/after:', before, after)
    print('preserved counts:', counts)
    db.conn.close()
