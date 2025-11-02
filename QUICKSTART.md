
# Quick Start Guide (v2)

## First Time Setup / Migration

1. Run `run.bat`
2. Press **Enter** at the password prompt
3. Select **"1. Add/Configure Target"** (or **"5. Migrate from old config.enc"** if upgrading)
4. Enter details for each target:
   - Target name (unique)
   - Router URL, ID, password (ID/PW encrypted)
   - PC MAC address
   - Router LAN port number (1-4, or 0 to disable check)
   - RDP server, username, password (ID/PW encrypted)
5. Add as many targets as you want. All network info is saved in `config.json` (plain), credentials in `credentials.enc` (encrypted).

## Normal Use

1. Run `run.bat`
2. Enter your master password
3. Select a target from the list
4. Wait while the program:
   - Sends WOL packet
   - **Monitors port status every second** (up to 30s)
   - Launches Remote Desktop **immediately** when PC wakes up
   - Or prompts after 30s timeout if PC not detected

## Options Menu

Press **Enter** (blank password) to access:

- **1**: Add/Configure Target (multi-target supported)
- **2**: Run (select target)
- **3**: Change master password only
- **4**: Delete all configuration
- **5**: Migrate from old config.enc
- **6**: Exit

## Command Line

```bash
python wol_mstsc.py                 # Normal run
python wol_mstsc.py --change-password   # Change password
```

## Files

- `config.json` - All targets/network info (plain, editable)
- `credentials.enc` - All credentials (encrypted, per target)
- `run.bat` - Windows launcher
- All `*.py` files - Python modules

## Troubleshooting

- **Wrong password**: Delete `credentials.enc` and reconfigure
- **Python not found**: Windows will open Microsoft Store to install
- **WOL fails**: Check MAC address format and router credentials
- **RDP fails**: Verify PC is booted and RDP is enabled
