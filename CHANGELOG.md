# WOL-MSTSC Changelog

## v2.0.0 (2025-11-02)

### Multi-Target, Editable Config, Secure Credentials
- **Multiple named targets**: Register and select any number of PCs/servers by name
- **Editable config**: All network info (IP, DNS, port, MAC, etc.) is stored in plain `config.json` for easy editing
- **Credentials only encrypted**: Only router/RDP id/pw are encrypted in `credentials.enc` (per target)
- **Migration tool**: Convert old `config.enc` to new format via menu
- **Menu overhaul**: Add/upgrade targets, select target to run, improved flows
- **Backward compatible**: Old config.enc can be migrated

---
# WOL-MSTSC Changelog

## v1.2.0 (2025-11-01)

### Real-Time Wake Detection
- **Removed fixed 5-second wait**
- **Monitors port status every second** for up to 30 seconds
- **Connects immediately** when PC wake is detected
- **Timeout handling**: After 30 seconds without detection, shows error message and prompts user to continue or abort
- Progress updates every 5 seconds during wait

### Behavior
- If LAN port configured: Real-time monitoring (1-30 seconds)
- If no LAN port (0 or invalid): Simple 5-second wait (legacy behavior)

---

## v1.1.0 (2025-11-01)

## Changes Made

### 1. New Entry Flow
- **Master password prompt first**: When you run the program, it immediately asks for your master password
- **Options menu on blank input**: Press Enter (leave password blank) to access an interactive menu:
  - Configure and Run
  - Change Master Password
  - Reset Configuration
  - Exit

### 2. Smart Boot Detection (IPTIME Router Port Link Check)
- Added `lan_port` field during initial configuration (e.g., LAN port 4)
- After sending WOL packet, program queries router for port link status via `port/link/status` API
- If the specified LAN port already shows link up (e.g., `"link":"100f"` or `"link":"1000f"`), the 5-second boot wait is **skipped**
- If port is down or check fails, waits 5 seconds as before

### 3. Simplified Batch Script
- Removed Python installation check (Windows Store will prompt automatically if needed)
- Directly runs `python wol_mstsc.py` after checking/installing dependencies
- Cleaner, simpler flow

### 4. README Translation to English
- Fully translated to English for open-source distribution
- Updated usage instructions to reflect new entry flow
- Added notes about port link status check

## New Configuration Fields

When setting up, you'll now be asked:
- **Router LAN Port Number**: Which physical LAN port your PC is connected to (1-4 typically)
  - Used to detect if PC is already powered on
  - Set to 0 or leave invalid to disable this check

## API Enhancement (iptime_wol.py)

New methods added:
- `get_port_link_status()`: Queries router's port/link/status endpoint
- `_link_value_is_up(link_value)`: Helper to check if a link value indicates "up" (e.g., "100f", "1000f")
- `is_lan_port_up(lan_port)`: Returns True if specified LAN port has link up

## Files Modified

1. `wol_mstsc.py` - Main program flow, options menu, port check logic
2. `iptime_wol.py` - Added port link status query methods
3. `run.bat` - Simplified launcher
4. `README.md` - Full English translation with updated usage

## Testing

All Python modules compile without syntax errors.

## Version

- **Version**: 1.1.0
- **Date**: 2025-11-01
