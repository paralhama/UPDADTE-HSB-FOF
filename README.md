# Fistful of Frags Server List Update Installer

## About This Project
Due to the absence of the main developer of *Fistful of Frags*, I created this executable to install a modified `client.dll` by [Weasel](https://github.com/Mecha-Weasel), allowing the game to list the new existing servers.


## Core Features

### Multi-Language Support
- Auto-detects system language (English, Portuguese, French, Spanish, Russian)
- Allows manual language selection via dropdown
- Interface updates immediately when language is changed

### Main Buttons
1. Install Update
- Downloads modified client.dll from GitHub repository
- Creates backup of original files before installation
- Shows progress bar during installation
- Verifies internet connection before proceeding
- Blocks installation if game is running

2. Select Game Manually
- For when auto-detection fails or game is installed in custom location
- Guides user through selecting correct Fistful of Frags folder
- Validates selected path contains required game files
- Enables Install button once valid path is found

3. Uninstall Update  
- Only appears if update is already installed
- Restores original files from backup
- Removes modified client.dll
- Blocks uninstall if game is running

### Safety Features
- Verifies internet connection before downloading updated files
- Prevents installation/uninstallation while game is running (checks for hl2.exe)
- If game files appear corrupted, provides Steam verification instructions:
 1. Locate 'Fistful of Frags' in Steam library
 2. Right-click and select Properties
 3. Go to Installed Files
 4. Click "Verify Integrity of Game Files"

### Source Files
- Modified client.dll is downloaded from GitHub repository
