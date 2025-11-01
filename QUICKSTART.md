# Quick Start Guide

## First Time Setup

1. Run `run.bat`
2. Press **Enter** at the password prompt
3. Select **"1. Configure and Run"**
4. Enter configuration details:
   - Master password (twice)
   - Router URL, ID, password
   - PC MAC address
   - **Router LAN port number** (1-4, or 0 to disable check)
   - RDP server, username, password
5. Done! Configuration saved encrypted.

## Normal Use

1. Run `run.bat`
2. Enter your master password
3. Wait while the program:
   - Sends WOL packet
   - **Monitors port status every second** (up to 30s)
   - Launches Remote Desktop **immediately** when PC wakes up
   - Or prompts after 30s timeout if PC not detected

## Options Menu

Press **Enter** (blank password) to access:

- **1**: Configure/reconfigure and run
- **2**: Change master password only
- **3**: Delete all configuration
- **4**: Exit

## Command Line

```bash
python wol_mstsc.py                 # Normal run
python wol_mstsc.py --change-password   # Change password
python wol_mstsc.py --reset-config      # Delete config
```

## Files

- `config.enc` - Your encrypted configuration
- `run.bat` - Windows launcher
- All `*.py` files - Python modules

## Troubleshooting

- **Wrong password**: Delete `config.enc` and reconfigure
- **Python not found**: Windows will open Microsoft Store to install
- **WOL fails**: Check MAC address format and router credentials
- **RDP fails**: Verify PC is booted and RDP is enabled
