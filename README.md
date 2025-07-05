# Application Registration Program for Kubuntu KDE

Creator: Benjamin Manwell (bmanwell15)
Version: v1.0.0
Last Modified: 7/5/2025

---

## Description
This command-line utility enables you to register both single-file executables (for example, AppImage bundles or standalone binaries) and entire application directories with the KDE Plasma application menu. By moving the target file or folder into the user's ~/Applications directory and generating a desktop entry file, it makes your custom applications immediately visible and launchable from the KDE "Start" menu. Although it was developed and tested on Kubuntu, it should work on any Linux distribution running the KDE Plasma desktop—such as KDE Neon, openSUSE KDE Plasma, Fedora KDE Spin, Arch Linux with KDE, and Linux Mint KDE Edition.

To report an issue or give a suggestion, please submit a new issue at [https://github.com/bmanwell15/linux-appreg/issues](https://github.com/bmanwell15/linux-appreg/issues).

**IMPORTANT: DO NOT USE SUDO FOR THIS COMMAND!**

#### Version Log

| Version | Date     | Description     |
| :---    | :---     | :---            |
| v1.0.0  | 7/5/2025 | Initial Release |

---

## Install

To Install, move into the github directory and run the following command:

```bash
sh install.sh
```

Note that the install script will install [dos2unix](https://linux.die.net/man/1/dos2unix), a command that simply converts a file to a Unix friendly format.

---

## Commands

### `register <App-File/Folder>`
Registers an application so that it appears in the KDE Plasma application menu.

#### Options:
- `-i`, `--icon <icon path>`  
  Specify the icon file for this application (required when registering a single file).

- `-c`, `--category <category>`  
  Assign a category (e.g., "Utility", "Development") under which the application will be grouped.

- `-n`, `--name <app name>`  
  Override the default name (derived from the file or folder) to display in menus.

- `-a`, `--autostart`  
  Enable automatic launch of this application upon user login.

- `-t`, `--terminal`  
  Force the application to run in a terminal window.

- `-e`, `--exec <executable>`  
  **(Required when registering a folder)** Provide the path, *relative to the application folder*, of the main executable to run.


### `remove <App-Name>`
Unregisters and removes the specified application entry (and its files if applicable).

### `list`
Displays all currently registered applications, indicating whether each is set to autostart.

### `help`
Shows this help text, describing available commands and options.

### `version`
Shows the version number and modify date of the application

---
## Examples

```bash
# Register a basic .AppImage. Note the icon file is not automatically extracted.
appreg register ~/Downloads/MyApp_x86_64.AppImage -n MyApp -i MyAppIcon.png
```

```bash
# Registers a folder as an application, with main.sh being the entering file.
appreg register ~/Downloads/MyDirApp -n DirApp -i dirApp.png -e main.sh
```

```bash
# Lists all applications registered with this command. Useful for finding the name of the app, which is needed to remove the application.
appreg list
```

```bash
# Removes an application that has been registered. Remove by the name of the application, not the path.
appreg remove MyApp
```