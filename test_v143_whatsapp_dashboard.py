from pathlib import Path

SOURCE = Path(__file__).with_name('main.py').read_text(encoding='utf-8')


def require(fragment: str, label: str) -> None:
    if fragment not in SOURCE:
        raise AssertionError(f'Missing {label}: {fragment}')


# The message and confirmation dialogs now use one-pass Arabic shaping, a wider
# layout, and a larger white Arabic font for mixed Arabic/Latin customer names.
require('FONT_DIALOG = (APP_FONT_FAMILY, 17, "bold")', 'dialog font')
require('win.geometry("760x360")', 'wide WhatsApp confirmation')
require('text=str(message or ""), font=FONT_DIALOG', 'logical dialog message rendering')
require('text_color=COLOR_WHITE, wraplength=670, justify="right", anchor="e"', 'right-aligned readable confirmation message')

# The pink primary surfaces now use the dominant logo red throughout aliases.
require('COLOR_LOGO = "#AA1E1E"', 'logo color')
require('COLOR_RUBI = COLOR_LOGO', 'Rubi logo mapping')
require('COLOR_CRIMSON = COLOR_RUBI', 'legacy crimson alias')

# Screenshot-highlighted loyalty status is white and visually larger.
require('font=FONT_NET_PROFIT_LABEL, text_color=COLOR_WHITE', 'large white loyalty status')

# Dashboard maintenance revenue is white.
require('f"إيرادات الصيانة: {d_maint:.2f} {CURRENCY}", for_ui=True), font=FONT_BOLD, text_color=COLOR_WHITE', 'white dashboard maintenance revenue')

# Existing operational entry points remain present.
for marker in ('def checkout(self):', 'def add_maintenance(self):', 'def add_transfer(self):', 'def send_whatsapp(self, phone, message):'):
    require(marker, f'operational marker {marker}')

print('V143 WhatsApp/dashboard assertions passed.')
