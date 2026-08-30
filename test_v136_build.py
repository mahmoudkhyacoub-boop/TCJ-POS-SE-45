from pathlib import Path
import ast

root = Path(__file__).parent
main = root / "main.py"
requirements = root / "requirements.txt"
workflow = root / ".github" / "workflows" / "build.yml"
root_workflow = root / "build.yml"

ast.parse(main.read_text(encoding="utf-8"), filename=str(main))
assert requirements.exists(), "requirements.txt is missing"
required_packages = {"customtkinter", "pillow", "arabic-reshaper", "python-bidi", "pandas", "openpyxl", "reportlab"}
req_text = requirements.read_text(encoding="utf-8").lower()
for package in required_packages:
    assert package in req_text, f"Missing package: {package}"

for path in (workflow, root_workflow):
    text = path.read_text(encoding="utf-8")
    assert "pip install -r requirements.txt" in text, f"requirements install missing in {path}"
    assert "requirements.txt is missing" in text, f"requirements preflight missing in {path}"
    assert "Trend_Center_Jordan_V139_Accounting_Service_Register" in text, f"V135 EXE name missing in {path}"
    assert "login_background.png" not in text, f"obsolete login background remains in {path}"
    assert "if (Test-Path -LiteralPath 'brand_logos')" in text, f"brand_logos fallback missing in {path}"
    assert "throw 'brand_logos is missing'" not in text, f"brand_logos must be optional in {path}"

print("V139 build checks passed: requirements, syntax, workflow paths, optional brand assets, V139 artifact name, and obsolete asset removal.")
