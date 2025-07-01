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
            -i, --icon <icon path>      Set the icon picture for the application (required for files).
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
            return

    print(f"{appName} not found in known locations.")


def extract_appimage_icon(appimage_path: Path) -> str | None:
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [str(appimage_path), '--appimage-extract'],
                cwd=tmpdir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            squashfs_root = Path(tmpdir) / 'squashfs-root'
            if not squashfs_root.exists():
                return None

            # Look for likely icon files
            icon_file = None
            for ext in (".png", ".svg", ".xpm", ".ico"):
                for candidate in squashfs_root.rglob(f"*{ext}"):
                    if 'icon' in candidate.name.lower():
                        icon_file = candidate
                        break
                if icon_file:
                    break

            if not icon_file:
                return None

            # Copy the image file to ~/.local/share/icons/
            icon_dest_dir = Path("~/.local/share/icons").expanduser().resolve()
            icon_dest_dir.mkdir(parents=True, exist_ok=True)
            final_icon = icon_dest_dir / f"{appimage_path.stem}{icon_file.suffix}"
            shutil.copy(icon_file, final_icon)
            return str(final_icon)

    except Exception as e:
        print("Error extracting icon from AppImage:", e)
        return None



def registerApp(args: list[str]):
    if not args:
        print("Missing target file/folder.")
        return

    # Defaults
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

    # Move app to destination
    appDestination = Path("~/Documents/Apps").expanduser().resolve()
    appDestination.mkdir(parents=True, exist_ok=True)
    newAppPath = appDestination / givenName
    shutil.move(filePath, newAppPath)
    os.chmod(newAppPath, 0o755)
    appPath = newAppPath

    # Detect icon if not set explicitly
    if not iconPath:
        if isFile and appPath.suffix == ".AppImage":
            extracted_icon = extract_appimage_icon(appPath)
            if extracted_icon:
                iconPath = extracted_icon
            else:
                iconPath = "application-x-executable"
        elif appPath.is_dir():
            for ext in (".png", ".svg", ".xpm", ".ico"):
                icons = list(appPath.glob(f"*{ext}"))
                if icons:
                    iconPath = str(icons[0])
                    break
            if not iconPath:
                iconPath = "application-x-executable"
        else:
            iconPath = "application-x-executable"

    # Create desktop entry
    desktopContent = f"""[Desktop Entry]
Name={givenName}
Exec={appPath}
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
        case "register":
            registerApp(sys.argv[2:])
        case "remove":
            deleteApp(sys.argv[2:])
        case "list":
            listApps()
        case "help":
            displayHelp()
        case _:
            print(f"Unknown command: {command}\n\n")
            displayHelp()
            sys.exit(2)

    sys.exit(1)
