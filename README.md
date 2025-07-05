# Application Registration Program for Kubuntu KDE

Creator: Benjamin Manwell (bmanwell15)
Version: v1.0.0
Last Modified: 7/5/2025

---

## Description
This command-line utility enables you to register both single-file executables (for example, AppImage bundles or standalone binaries) and entire application directories with the KDE Plasma application menu. By moving the target file or folder into the user's ~/Applications directory and generating a desktop entry file, it makes your custom applications immediately visible and launchable from the KDE "Start" menu. Although it was developed and tested on Kubuntu, it should work on any Linux distribution running the KDE Plasma desktop—such as KDE Neon, openSUSE KDE Plasma, Fedora KDE Spin, Arch Linux with KDE, and Linux Mint KDE Edition.

To report an issue or give a suggestion, please submit a new issue at [https://github.com/bmanwell15/linux-appreg/issues](https://github.com/bmanwell15/linux-appreg/issues).

IMPORTANT: DO NOT USE SUDO FOR THIS COMMAND!

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

---
## Examples

```bash
# Register a basic .AppImage. Note the icon file is not automatically extracted.
appreg register MyApp_x86_64.AppImage -n MyApp -I MyAppIcon.png
```

```bash
appreg remove MyApp
```