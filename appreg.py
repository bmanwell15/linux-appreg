#!/usr/bin/env python3

import os
import sys
import shutil
from pathlib import Path

def displayHelp():
    print("""App Registration Program for Kubuntu KDE

Commands:
    register <App-File/Folder>          Registers the app to allow it to be accessible to Kubuntu KDE
        Options:
            -i, --icon <icon path>      Set the icon picture for the application.
            -c, --category <category>   Sets the category for the app.
            -n, --name <app name>       Sets the name of the app. If not set, the file/folder name will be used.
            -a, --autostart             Start the app automatically upon login.
            -t, --terminal              Run the app in a terminal window.

    remove <App-Name>                   Removes the specified app.
    list                                Lists the registered apps.
    help                                Displays this menu.
""")


def listApps():
    appPathLocation = Path("~/.local/share/applications").expanduser().resolve()
    autoStartLocation = Path("~/.config/autostart").expanduser().resolve()

    print("Registered Apps:")
    for filePath in appPathLocation.glob("*.desktop"):
        print(filePath.stem)

    print("\nAutostart Apps:")
    for filePath in autoStartLocation.glob("*.desktop"):
        print(filePath.stem)


def deleteApp(args):
    if not args:
        print("Missing app name.")
        return

    appName = args[0]

    desktopPathLocation = Path("~/.local/share/applications").expanduser().resolve()

    for app in desktopPathLocation.iterdir():
        if app.stem == appName:
           desktopPath = desktopPathLocation / app.name
           os.remove(str(desktopPath))
           appLocation = Path("~/Documents/Apps").expanduser().resolve() / app.stem
           if appLocation.is_dir():
              shutil.rmtree(appLocation)
           else:
              os.remove(appLocation)
           print("Successfully removed", appName)
           return;

    print(f"{appName} not found in known locations.")


def registerApp(args: list[str]):
    if not args:
        print("Missing target file/folder.")
        return

    # Defaults
    category = "Utility"
    iconPath = "application-x-executable"
    terminalProgram = False
    autostart = False

    # Parse positional argument
    filePath = Path(args[0]).expanduser().resolve()
    if not filePath.exists():
        print("Error: File or folder does not exist.")
        return

    givenName = filePath.stem
    isFile = filePath.is_file()

    # Parse optional flags
    i = 1
    while i < len(args):
        arg = args[i]
        if arg in ("-i", "--icon"):
            i += 1
            iconPath = args[i]
        elif arg in ("-c", "--category"):
            i += 1
            category = args[i]
        elif arg in ("-n", "--name"):
            i += 1
            givenName = args[i]
        elif arg in ("-a", "--autostart"):
            autostart = True
        elif arg in ("-t", "--terminal"):
            terminalProgram = True
        else:
            print(f"Unknown option: {arg}")
        i += 1

    # Copy to new destination (original left behind unless moved)
    appDestination = Path("~/Documents/Apps").expanduser().resolve()
    appDestination.mkdir(parents=True, exist_ok=True)
    shutil.move(filePath, appDestination / givenName)

    appPath = appDestination / givenName
    os.chmod(appPath, 0x755)

    if isFile:
    	iconPath = appPath

    # If icon is a file path

    # Create .desktop entry
    desktopContent = f"""[Desktop Entry]
Name={givenName}
Exec="{appPath}"
Icon="{iconPath}"
Type=Application
Terminal={'true' if terminalProgram else 'false'}
Categories="{category}"
{"X-GNOME-Autostart-enabled=true" if autostart else ""}
{"Hidden=false" if autostart else ""}
{"NoDisplay=false" if autostart else ""}
"""

    desktopFile = (Path("~/.config/autostart") if autostart else Path("~/.local/share/applications")).expanduser().resolve() / f"{givenName}.desktop"
    desktopFile.parent.mkdir(parents=True, exist_ok=True)
    desktopFile.write_text(desktopContent.strip() + '\n')
    os.chmod(desktopFile, 0o755)
    print(f"Registered app: {givenName}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        displayHelp()
        sys.exit(1)

    command = sys.argv[1]

    match command:
        case "register": registerApp(sys.argv[2:])
        case "remove": deleteApp(sys.argv[2:])
        case "list": listApps()
        case "help": displayHelp()
        case _:
            print(f"Unknown command: {command}\n\n")
            displayHelp()
            sys.exit(2)
    sys.exit(1)
