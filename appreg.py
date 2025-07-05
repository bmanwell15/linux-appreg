#!/usr/bin/env python3

import os
import sys
import shutil
from pathlib import Path

def displayHelp():
    print("""@author Benjamin Manwell (bmanwell15)
@version v1.0.0
@date 7/5/2025

Application Registration Program for Kubuntu KDE
This command-line utility enables you to register both single-file executables (for example, AppImage bundles or standalone binaries) and entire application directories with the KDE Plasma application menu. By moving the target file or folder into the user's ~/Applications directory and generating a desktop entry file, it makes your custom applications immediately visible and launchable from the KDE "Start" menu. Although it was developed and tested on Kubuntu, it should work on any Linux distribution running the KDE Plasma desktop—such as KDE Neon, openSUSE KDE Plasma, Fedora KDE Spin, Arch Linux with KDE, and Linux Mint KDE Edition.

To report an issue, please submit a new issue at https://github.com/bmanwell15/linux-appreg/issues

IMPORTANT: DO NOT USE SUDO FOR THIS COMMAND!

Commands:
    register <App-File/Folder>          Registers the app to allow it to be accessible to Kubuntu KDE
        Options:
            -i, --icon <icon path>      Set the icon picture for the application (required for files).
            -c, --category <category>   Sets the category for the app.
            -n, --name <app name>       Sets the name of the app. If not set, the file/folder name will be used.
            -a, --autostart             Start the app automatically upon login.
            -t, --terminal              Run the app in a terminal window.
            -e, --exec <executable>     If the provided app is a directory, then the executable file must be given RELATIVE TO THE APP FOLDER as well.

    remove <App-Name>                   Removes the specified app.
    list                                Lists the registered apps.
    help                                Displays this menu.
""")


def listApps():
    appPathLocation = Path("~/.local/share/applications").expanduser().resolve()
    autoStartLocation = Path("~/.config/autostart").expanduser().resolve()
    a = "autostart=false"

    print("Registered Apps:")
    for filePath in appPathLocation.glob("*.desktop"):
        print(f"{filePath.stem:<50}{a:<20} location={appPathLocation}")

    a = "autostart=true"
    for filePath in autoStartLocation.glob("*.desktop"):
         print(f"{filePath.stem:<50}{a:<20} location={autoStartLocation}")


def deleteApp(args):
    if not args:
        print("Missing app name.")
        return

    appName = args[0]
    desktopPathLocation = Path("~/.local/share/applications").expanduser().resolve()

    confirm: str = input("Are you sure you want to delete '" + appName + "'? (y/n): ")
    if not confirm.lower().count('y'): return

    for app in desktopPathLocation.iterdir():
        if app.stem == appName:
            desktopPath = desktopPathLocation / app.name
            os.remove(str(desktopPath))
            appLocation = Path("~/Applications").expanduser().resolve() / app.stem
            if appLocation.is_dir():
                shutil.rmtree(appLocation)
            else:
                os.remove(appLocation)
            print("Successfully removed", appName)
            return

    print(f"{appName} was not found.")


def findIcon(folder):
    for ext in (".png", ".svg", ".xpm", ".ico"):
        icons = list(folder.glob(f"*{ext}"))
        if icons:
            return str(icons[0])
    return None


def chmodRecursive(path, mode):
    for root, dirs, files in os.walk(path):
        for dirname in dirs:
            os.chmod(os.path.join(root, dirname), mode)
        for filename in files:
            os.chmod(os.path.join(root, filename), mode)
    os.chmod(path, mode)  # Don't forget to chmod the root itself


def registerApp(args: list[str]):
    if not args:
        print("Missing target file/folder.")
        return

    # Defaults
    execPath = None
    category = "Utility"
    iconPath = None
    terminalProgram = False
    autostart = False

    # Parse positional argument
    filePath = Path(args[0]).expanduser().resolve()
    if not filePath.exists():
        print("Error: File or folder does not exist.")
        return

    givenName = filePath.stem

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
        elif arg in ("-e", "--exec"):
            i += 1
            execPath = args[i]
        elif arg in ("-t", "--terminal"):
            terminalProgram = True
        else:
            print(f"Unknown option: {arg}")
            return
        i += 1

    # Move app to destination
    appDestination = Path("~/Applications").expanduser().resolve()
    appDestination.mkdir(parents=True, exist_ok=True)
    newAppPath = appDestination / givenName
    shutil.move(filePath, newAppPath)
    os.chmod(newAppPath, 0o755) if newAppPath.is_file() else chmodRecursive(newAppPath, 0o755)
    appPath = newAppPath

    
    if appPath.is_dir():
        if not execPath:
            print("Error: App is a folder. You must provide the path to the main executable using --exec.")
            return
        execCandidate = appPath / execPath
        if not execCandidate.exists():
            print(f"Error: Executable '{execPath}' not found inside the folder.")
            return
        if not os.access(execCandidate, os.X_OK):
            print(f"Error: File '{execPath}' is not executable.")
            return
        mainExecutable = str(execCandidate)
    else:
        if not os.access(appPath, os.X_OK):
            print(f"Error: File '{appPath}' is not executable.")
            return
        mainExecutable = str(appPath)


    # Icon logic
    if iconPath:
        iconPath = str(Path(iconPath).expanduser().resolve())
        if not Path(iconPath).is_file():
            print(f"Error: Provided icon file does not exist: {iconPath}")
            return
    elif appPath.is_dir():
        foundIcon = findIcon(appPath)
        if foundIcon:
            iconPath = foundIcon
        else:
            print("Error: No icon found in folder. Use --icon to specify one.")
            return
    else:
        print("Error: You must provide an icon using --icon when registering a file.")
        return

    # Create desktop entry
    desktopContent = f"""[Desktop Entry]
Name={givenName}
Exec={mainExecutable}
Icon={iconPath}
Type=Application
Terminal={'true' if terminalProgram else 'false'}
Categories={category}
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