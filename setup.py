import sys

from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["serial.win32","serial.tools"], "includes": ["tkinter","serial.tools"]}


base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name = "HAL320 controller",
        version = "0.23",
        description = "Controller for Asahi Spectrum HAL320 solar simulator",
        options={"build_exe": build_exe_options},
        executables = [Executable("main.py", base = base, icon='HAL302icon.ico')])