# 🖥️ Windows Server Evaluation Tray Tool

A lightweight Python-based tray application for Windows Server 2022 that displays the remaining evaluation period (days) directly in the taskbar. The icon changes color based on urgency, and critical warnings are shown as popups to ensure proactive license management.

---

## ✅ Features

- 🕒 Reads remaining evaluation days using `slmgr.vbs /dli`
- 🎨 Taskbar icon color changes:
  - **Gray**: More than 60 days remaining
  - **Orange**: 31–60 days remaining
  - **Red**: 30 days or fewer
- ⚠️ Popup warning when 20 days or fewer are left
- 🔁 Hourly background refresh
- 🌐 Supports both English and German output from `slmgr.vbs`

---

## 📦 Requirements

- Windows Server 2022 (or compatible Windows edition)
- Python 3.11+ installed
- Packages:
  - `pystray`
  - `pillow`
  - `pyinstaller`

---

## 🚀 Installation

1. Clone the repository or copy the `eval_tray.py` script to your desired directory:

```powershell
git clone https://github.com/yourusername/eval-tray

2. Install required packages

```powershell
& "C:\Program Files\Python311\python.exe" -m pip install pillow pystray

3. Create .exe file

```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile "C:\Program Files\EvalTray\eval_tray.py"

4. Create shortcut for auto start in the folder: "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"



Copyright 2025 srcdevlogs

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0