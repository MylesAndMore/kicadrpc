from sys import platform

if platform == "win32":
    import win32gui
elif platform == "darwin":
    import subprocess
elif platform == "linux":
    import Xlib.display
    import Xlib.X

def get_windows() -> list[str]:
    if platform == "win32":
        def enumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                ctx.append(win32gui.GetWindowText(hwnd))
        windows = []
        win32gui.EnumWindows(enumHandler, windows)
        return windows
    elif platform == "darwin":
        result = subprocess.run(
            ["osascript", "-e", "tell application \"System Events\" to get the name of every window of every process"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"osascript failed with error '{result.stderr}'")
        windows = result.stdout.split(", ")
        return [window.strip() for window in windows if window.strip()]
    elif platform == "linux":
        display = Xlib.display.Display()
        root = display.screen().root
        window_ids = root.get_full_property(display.intern_atom("_NET_CLIENT_LIST"), Xlib.X.AnyPropertyType).value
        windows = []
        for window_id in window_ids:
            window = display.create_resource_object("window", window_id)
            window_name = window.get_full_property(display.intern_atom("_NET_WM_NAME"), 0)
            if window_name:
                windows.append(window_name.value.decode("utf-8"))
        return windows
    else:
        raise NotImplementedError(f"Cannot get windows on platform {platform}")
