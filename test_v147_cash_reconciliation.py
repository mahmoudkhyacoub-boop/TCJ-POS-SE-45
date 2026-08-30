import importlib.util
import tempfile
from pathlib import Path

SOURCE = Path(__file__).with_name("main.py")
spec = importlib.util.spec_from_file_location("tcj_v147_cash", SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

root = Path(tempfile.mkdtemp(prefix="tcj_v147_cash_"))
mod.DB_NAME = str(root / "cash.db")
db = mod.Database()


class Stub:
    current_user = "audit"

    def __init__(self, database):
        self.db = database

    _ledger_account_for_payment = mod.TrendCenterApp._ledger_account_for_payment
    _operational_account_net = mod.TrendCenterApp._operational_account_net
    _operational_channel_net = mod.TrendCenterApp._operational_channel_net
    _post_journal_entry = mod.TrendCenterApp._post_journal_entry


app = Stub(db)
DAY = "2026-08-25"
TIME = "10:00:00"


def insert_transfer(kind, amount, commission, payment, reference):
    db.cursor.execute(
        "INSERT INTO transfers(type, client_name, amount, commission, reference, date, time, user, payment_method) "
        "VALUES(?,?,?,?,?,?,?,?,?)",
        (kind, "Audit client", amount, commission, reference, DAY, TIME, "audit", payment),
    )
    return int(db.cursor.lastrowid)


def outgoing_lines(payment, amount, commission):
    return [
        (app._ledger_account_for_payment(payment), amount, 0, "تحصيل قيمة خروج الحوالة"),
        ("CASH", 0, amount - commission, "المبلغ النقدي المسلم للمستفيد"),
        ("TRANSFER_REVENUE", 0, commission, "عمولة خروج الحوالة"),
    ]


# Two Visa remittances reproduce the reported symptom: the operational table
# shows 9.50 + 9.50, while a legacy and a current journal row for each operation
# would make the old journal-based display show Visa 40.00 and Cash -38.00.
for index in range(2):
    transfer_id = insert_transfer("خروج حوالة", 10.00, 0.50, "Visa", f"V-{index}")
    lines = outgoing_lines("Visa", 10.00, 0.50)
    app._post_journal_entry("transfer", f"transfer-{transfer_id}", "قيد اختبار", lines, DAY, TIME)
    db._legacy_post("legacy_transfer", transfer_id, DAY, TIME, "قيد قديم مكرر للاختبار", lines)

# A CLIQ remittance is a bank movement and a visible channel detail, but the
# detail must never be added again to the unified bank balance.
cliq_id = insert_transfer("خروج حوالة", 10.00, 0.50, "CLIQ", "C-1")
cliq_lines = outgoing_lines("CLIQ", 10.00, 0.50)
app._post_journal_entry("transfer", f"transfer-{cliq_id}", "قيد اختبار CLIQ", cliq_lines, DAY, TIME)
db.conn.commit()


def ledger_net(account):
    row = db.cursor.execute(
        "SELECT COALESCE(SUM(jl.debit - jl.credit), 0) "
        "FROM journal_lines jl JOIN journal_entries je ON je.id=jl.entry_id "
        "WHERE COALESCE(je.status, 'active')='active' AND jl.account_code=?",
        (account,),
    ).fetchone()
    return round(float(row[0] or 0.0), 2)


# Reproduce the old display's duplicated active-journal result. The third
# CLIQ transfer adds one more legitimate -9.50 cash movement.
assert ledger_net("VISA") == 40.00, ledger_net("VISA")
assert ledger_net("CASH") == -47.50, ledger_net("CASH")

# V147 authoritative cash-count values read one operational row once.
assert app._operational_account_net("VISA", DAY, DAY) == 20.00
assert app._operational_account_net("CASH", DAY, DAY) == -28.50
assert app._operational_account_net("BANK", DAY, DAY) == 10.00
assert app._operational_channel_net("CLIQ", DAY, DAY) == 10.00

# With a user-entered 50.00 daily opening, the expected physical cash is 21.50.
assert round(50.00 + app._operational_account_net("CASH", DAY, DAY), 2) == 21.50

# BANK contains the CLIQ movement once; the CLIQ number is informational only.
expected_bank = app._operational_account_net("BANK", DAY, DAY)
cliq_detail = app._operational_channel_net("CLIQ", DAY, DAY)
assert expected_bank == 10.00 and cliq_detail == 10.00
assert round(expected_bank, 2) != round(expected_bank + cliq_detail, 2)

print("V147 cash reconciliation checks passed: duplicate journal rows no longer duplicate displayed operational balances; BANK/CLIQ remains non-additive.")
print("TEMP_DB=" + str(root / "cash.db"))
