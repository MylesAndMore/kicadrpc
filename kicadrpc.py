# Copyright (c) 2024, MylesAndMore
# License: MIT

from getwindows import get_windows
from pypresence import Presence
import time
from typing import Tuple

client_id = "1312909179219869787"
rpc = Presence(client_id)

def parse_project_sheet(title: str) -> Tuple[str, str]:
    """Parse the current project and sheet name from the title of an eeschema window.
    :param title: the title of the eeschema window
    :returns: a tuple containing the project name and the sheet name
    """
    sheet = "Root"
    if "[" in title and "]" in title:
        # Editing a hierarchical sheet in eeschema
        project_part = title.split("[")[1].split("]")[0]
        if "/" in project_part:
            project = project_part.split("/")[0]
            sheet = project_part[len(project) + 1:].strip()
        else:
            # Root sheet (but unsaved)
            project = project_part.strip()
    else:
        # The root sheet in eeschema uses this format, as well as pcbnew and the project manager (always)
        project = title.split("—")[0].strip()
    return project, sheet

def parse_project(title: str) -> str:
    """Parse the current project name from the title of any KiCad window.
    :param title: the title of the window (eeschema, pcbnew, or kicad)
    :returns: the project name
    """
    return parse_project_sheet(title)[0]

def find_window_endswith(endswith: str) -> str | None:
    """Find an open window that ends with a specific string.
    :param endswith: the string to check for at the end of the window title
    :returns: the window title if found, otherwise None
    """
    for window in get_windows():
        if window.endswith(endswith):
            return window
        
def find_window_contains(contains: str) -> str | None:
    """Find an open window that contains a specific string.
    :param contains: the string to check for in the window title
    :returns: the window title if found, otherwise None
    """
    for window in get_windows():
        if contains in window:
            return window

def get_eeschema_window() -> str | None:
    """:returns: the title of the currently open eeschema window if found, otherwise None"""
    return find_window_endswith("Schematic Editor")

def get_pcbnew_window() -> str | None:
    """:returns: the title of the currently open pcbnew window if found, otherwise None"""
    return find_window_endswith("PCB Editor")

def get_kicad_window() -> str | None:
    """:returns: the title of the currently open KiCad (project) window if found, otherwise None"""
    return find_window_contains(" — KiCad")

def main():
    rpc.connect()
    began = time.time()
    while True:
        eeschema = get_eeschema_window()
        pcbnew = get_pcbnew_window()
        kicad = get_kicad_window()
        if pcbnew:
            project = parse_project(pcbnew)
            rpc.update(
                details=f"Working on {project}",
                state="In the PCB Editor",
                large_image="pcbnew",
                large_text="PCB Editor",
                small_image="kicad",
                small_text="KiCad EDA",
                start=began
            )
        elif eeschema:
            project, sheet = parse_project_sheet(eeschema)
            rpc.update(
                details=f"Working on {project}",
                state=f"Editing {sheet}",
                large_image="eeschema",
                large_text="Schematic Editor",
                small_image="kicad",
                small_text="KiCad EDA",
                start=began
            )
        elif kicad:
            project = parse_project(kicad)
            rpc.update(
                details=f"Working on {project}",
                state="Idling",
                large_image="kicad",
                large_text="KiCad EDA",
                start=began
            )
        else:
            time.sleep(5)
            if not get_kicad_window():
                exit(0) # Still no KiCad after five seconds of waiting, we can safely exit
        time.sleep(15)

if __name__ == "__main__":
    main()
