import subprocess
import re
import threading
import time
from PIL import Image, ImageDraw
import pystray
import ctypes

# === Create tray icon with specified color ===
def create_icon(color):
    image = Image.new('RGB', (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill=color)
    return image

# === Show popup warning if evaluation is about to expire ===
def show_warning_popup(days):
    title = "⚠️ Windows Evaluation Period Expiring Soon"
    message = f"Your Windows Server evaluation will expire in {days} days.\nPlease activate the system in time."
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)  # OK, Information icon

# === Retrieve remaining evaluation days from slmgr.vbs output ===
def get_evaluation_days_remaining():
    try:
        result = subprocess.run(
            ['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dli'],
            capture_output=True,
            text=True,
            shell=True
        )
        output = result.stdout

        # Match German output: (180 Tag(e))
        match = re.search(r"Ablauf.*?\((\d+)\s*Tag", output, re.IGNORECASE)

        # Match English output: Remaining evaluation period: 180 days
        if not match:
            match = re.search(r"Remaining.*?(\d+)\s+days", output, re.IGNORECASE)

        if match:
            return int(match.group(1))

    except Exception as e:
        print("Error retrieving license info:", e)

    return None

# === Background updater for tooltip and icon color ===
def update_tooltip_and_icon(icon):
    while True:
        days = get_evaluation_days_remaining()
        if days is not None:
            icon.title = f"Remaining Eval Days: {days}"

            # Change color depending on how much time is left
            if days > 60:
                icon.icon = create_icon('gray')
            elif days > 30:
                icon.icon = create_icon('orange')
            else:
                icon.icon = create_icon('red')
        else:
            icon.title = "No evaluation period detected"
            icon.icon = create_icon('gray')

        time.sleep(3600)  # Update every hour

# === Initialize and start the tray icon ===
def setup_tray_icon():
    icon = pystray.Icon("eval_days")
    icon.icon = create_icon('gray')
    icon.title = "Loading evaluation info…"

    # Right-click menu with Exit option
    icon.menu = pystray.Menu(
        pystray.MenuItem("Exit", lambda icon, item: icon.stop())
    )

    # Initial check and warning popup if needed
    days = get_evaluation_days_remaining()
    if days is not None and days <= 20:
        show_warning_popup(days)

    # Start background update thread
    threading.Thread(target=update_tooltip_and_icon, args=(icon,), daemon=True).start()

    icon.run()

# === Main entry point ===
if __name__ == "__main__":
    setup_tray_icon()