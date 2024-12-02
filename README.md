# kicadrpc

(Experimental) Discord Rich Presence for KiCad

## Feature

- Displays currently open schematic/PCB file/project
- That's it

## To Use

- Clone the repository
- Install requirements `pip3 install -r requirements.txt`
- Run `python3 kicadrpc.py` and enjoy!

## Quick Notes

KiCad does in fact support plugins, but these only work in the PCB Editor. Therefore, this script must scan open applications on your system to function, hence the limited information.

If and when KiCad adds plugin support for the schematic editor, I'll consider rewriting this script.
