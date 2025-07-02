import subprocess
import re
import threading
import time
from PIL import Image, ImageDraw
import pystray
import ctypes

# === create colored icon ===
def create_icon(color):
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill=color)
    return image

# === popup for equal or less then 20 days ===
def show_warning_popup(days):
    title = "⚠️ Windows-Evaluation ends soon"
    message = f"Your Windows Server-Evaluation ends in {days} days!\nPlease activate your system in time."
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)  # OK, Info

# === get remaining duration of evaluation (bilingual) ===
def get_evaluation_days_remaining():
    try:
        result = subprocess.run(
            ['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dli'],
            capture_output=True,
            text=True,
            shell=True
        )
        output = result.stdout

        # German: Ablauf ... (180 Tag(e))
        match = re.search(r"Ablauf.*?\((\d+)\s*Tag", output, re.IGNORECASE)

        # English: Remaining evaluation period: 123 days
        if not match:
            match = re.search(r"Remaining.*?(\d+)\s+days", output, re.IGNORECASE)

        if match:
            return int(match.group(1))

    except Exception as e:
        print("Failed to get license information:", e)

    return None

# === update Tooltip & Icon regularly ===
def update_tooltip_and_icon(icon):
    while True:
        days = get_evaluation_days_remaining()
        if days is not None:
            icon.title = f"Remaining Eval-Days: {days}"

            if days > 60:
                icon.icon = create_icon('gray')
            elif days > 30:
                icon.icon = create_icon('orange')
            else:
                icon.icon = create_icon('red')
        else:
            icon.title = "Didn`t found Evaluation"
            icon.icon = create_icon('gray')

        time.sleep(3600)  # check every hour

# === set up Tray-Icon ===
def setup_tray_icon():
    icon = pystray.Icon("eval_days")
    icon.icon = create_icon('gray')
    icon.title = "Eval-Check wird geladen…"

    icon.menu = pystray.Menu(
        pystray.MenuItem("Exit", lambda icon, item: icon.stop())
    )

    # check at start up
    days = get_evaluation_days_remaining()
    if days is not None and days <= 20:
        show_warning_popup(days)

    threading.Thread(target=update_tooltip_and_icon, args=(icon,), daemon=True).start()

    icon.run()

# === start point ===
if __name__ == "__main__":
    setup_tray_icon()
