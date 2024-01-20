# PalWorlds Mod Patcher
This is meant to be a Starter Pack, a basic organized setup for those who want to start tinkering

FlyingMountSPUsage - NO SP COST While flying,
MapUnlocker - Unlock the entire map,
PlayerPointsPerLevel - Modify points increase per level,
PlayerSPUsage - No SP usage for player "except gliding for some reason",
PlayerWeight - Weight modifier "Default value may get reset when increased via points",
RarePalAppearRate_AndLevel - "Change Rare Rate Appearance rate and its level"

Modify the respective mods main.lua for the different modifiers.

## Overview

PalWorlds Mod Patcher is a PyQt5-based GUI tool designed to simplify modding for the game PalWorld. It automates the process of downloading and applying a custom patch, managing game modifications, and reverting changes as needed.

## Features

- **Download and Apply Patch**: Automatically downloads and applies the UE4SS DevKit patch to the specified PalWorld game directory.
- **Manage Mods**: Enables users to easily enable or disable mods by editing the `Mods.txt` file in a user-friendly manner.
- **Revert Changes**: Provides an option to 'Unpatch' the game, reverting it back to its pre-modded state.

## Setup

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/your-github-username/palworlds-mod-patcher.git

Install Dependencies:
Ensure Python is installed on your system.
Install required Python packages

Usage
Run the Tool:

Navigate to the cloned repository's directory.
Execute the main script:
sh
Copy code
python gui.py
Select Game Path:

Use the 'Select Game Path' button to choose the PalWorld game directory.
Patch Game:

Click 'Patch Game' to download and apply the patch.
Manage Mods:

Use the 'Manage Mods' button to enable/disable mods as desired.
Unpatch Game (Optional):

To revert all changes, use the 'Unpatch Everything' button or check json file.

Contributions / Credits
https://gist.github.com/DRayX
https://github.com/UE4SS-RE/RE-UE4SS

Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.

License
Distributed under the MIT License. See LICENSE for more information.




