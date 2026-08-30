import os
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    import sys
    sys.path.insert(0, '/home/ubuntu/trend_center_advanced')
    import main

    db = main.Database()
    app = object.__new__(main.TrendCenterApp)
    app.db = db
    app.current_user = 'test'

    cases = [
        ('خروج حوالة', 10.0, 0.5, 'Visa'),
        ('خروج حوالة', 10.0, 0.5, 'CLIQ'),
        ('دخول حوالة', 10.0, 0.5, 'Cash'),
        ('دفع فاتورة', 10.0, 0.5, 'Cash'),
        ('دفع فاتورة', 10.0, 0.5, 'Visa'),
    ]
    for idx, (kind, amount, commission, payment) in enumerate(cases, 1):
        db.cursor.execute(
            'INSERT INTO transfers (type, client_name, amount, commission, reference, payment_method, date, time, user) VALUES (?,?,?,?,?,?,?,?,?)',
            (kind, f'عميل {idx}', amount, commission, f'R{idx}', payment, '2026-08-24', f'10:00:0{idx}', 'test'),
        )
        rid = db.cursor.lastrowid
        app._post_operation_journal_from_row('transfers', rid)
    db.conn.commit()

    rows = db.cursor.execute('''
        SELECT je.source_id, SUM(jl.debit), SUM(jl.credit)
        FROM journal_entries je JOIN journal_lines jl ON jl.entry_id=je.id
        GROUP BY je.id ORDER BY je.id
    ''').fetchall()
    assert rows, 'No journal rows created'
    for source_id, debit, credit in rows:
        assert abs(float(debit) - float(credit)) < 0.005, (source_id, debit, credit)

    bank_net = db.cursor.execute("SELECT COALESCE(SUM(debit-credit),0) FROM journal_lines WHERE account_code='BANK'").fetchone()[0]
    cliq_rows = db.cursor.execute("SELECT COUNT(*) FROM journal_lines WHERE account_code='CLIQ'").fetchone()[0]
    assert abs(float(bank_net) - (-20.0)) < 0.005, bank_net
    assert cliq_rows == 0, cliq_rows

    assert app._ledger_account_for_payment('CLIQ') == 'BANK'
    assert app._ledger_account_for_payment('فيزا') == 'VISA'
    assert app._ledger_account_for_payment('صندوق المحل (نقدي)') == 'CASH'
    print('V132 accounting smoke tests passed:', len(rows), 'balanced entries')
