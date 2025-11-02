
# WOL-MSTSC

**Wake-on-LAN + Remote Desktop Connection Tool (Multi-Target, Secure, Editable)**

A Windows utility that wakes up one or more remote PCs via your router (Wake-on-LAN) and automatically connects to them via Remote Desktop (MSTSC). Now supports multiple named targets, editable config, and only encrypts sensitive credentials.

## 🎯 Key Features

- ✅ **Multi-Target Support**: Register and manage multiple PCs/servers by name
- ✅ **Editable Config**: All network info (IP, DNS, port, MAC, etc.) is stored in plain JSON for easy editing
- ✅ **Master Password Security**: Only credentials (router & RDP id/pw) are encrypted with your master password
- ✅ **IPTIME Router Support**: Send WOL packets via IPTIME routers
- ✅ **Real-Time Wake Detection**: Monitors router port status every second (up to 30s) and connects immediately when PC is ready
- ✅ **Automatic Remote Desktop**: Launches MSTSC as soon as PC wakes up
- ✅ **Easy Setup & Migration**: Interactive configuration, add/upgrade targets, migrate from old config.enc
- ✅ **Password Management**: Change master password or reset configuration anytime


## 📋 Requirements

- **OS**: Windows 10/11
- **Python**: 3.8 or higher (if not installed, Windows will prompt you to install from Microsoft Store)
- **Network**: Access to your router's admin page


## 🚀 Installation

### 1. Download the Project

```bash
git clone https://github.com/nzin4x/router-wol-mstsc.git
cd router-wol-mstsc
```

### 2. Install Dependencies

Run `run.bat` or manually install:

```bash
pip install -r requirements.txt
```


## 📖 Usage

### First Run & Migration

Run `run.bat` (or `python wol_mstsc.py`).

**You will be prompted for your master password immediately.**

- **Enter a password**: Proceeds to target selection and WOL flow if already configured
- **Press Enter (blank)**: Opens the options menu for setup, add/upgrade targets, password change, migration, or reset

#### Initial Configuration / Add Target

From the options menu, choose **Add/Configure Target**. For each target, you'll provide:

1. **Target Name**: Unique name for this PC/server (e.g., `main`, `office`, `server1`)
2. **Router Information** (IPTIME):
   - URL (e.g., `http://192.168.0.1:80`)
   - Login ID (encrypted)
   - Login Password (encrypted)
3. **PC to Wake**:
   - MAC Address (e.g., `10:FF:E0:38:F4:D5`)
   - Router LAN Port Number (e.g., `4`)
4. **Remote Desktop**:
   - Server Address (e.g., `192.168.0.100:3389`)
   - RDP Username (encrypted)
   - RDP Password (encrypted)

You can add as many targets as you want. All network info is saved in `config.json` (plain), credentials in `credentials.enc` (encrypted).

#### Migration from Old Version

If you have an old `config.enc`, use the menu option **Migrate from old config.enc**. You'll be prompted for a target name and your master password. The tool will convert your old config to the new format.

### Normal Use

After setup, just run `run.bat` and enter your master password. The program will:

1. Show a list of all registered targets (by name)
2. Let you select which PC/server to wake and connect
3. Login to your router
4. Send WOL packet to wake your PC
5. **Monitor port link status in real-time** (checks every second for up to 30 seconds)
6. Launch Remote Desktop as soon as PC is detected awake
7. If timeout (30s) without wake detection, prompt to continue or abort


## 🔧 Options Menu

Press **Enter** (blank) at the master password prompt to access:

- **Add/Configure Target**: Add a new PC/server or update info
- **Run (select target)**: Choose a target and run WOL+MSTSC
- **Change Master Password**: Update your master password (keeps all targets)
- **Reset Configuration**: Delete all config and credentials
- **Migrate from old config.enc**: Upgrade from previous version
- **Exit**: Quit the program


## 📁 Project Structure

```
router-wol-mstsc/
├── wol_mstsc.py          # Main program
├── crypto_utils.py       # Encryption/decryption utilities
├── config_manager.py     # Configuration management
├── iptime_wol.py         # IPTIME WOL module
├── mstsc_connector.py    # Remote Desktop connection
├── requirements.txt      # Python dependencies
├── run.bat               # Launcher batch script
├── config.json           # Plain config (targets, editable)
├── credentials.enc       # Encrypted credentials (auto-generated)
└── README.md             # This file
```


## 🔐 Security

- All sensitive data (router credentials, RDP credentials) is encrypted with your master password in `credentials.enc`
- All network info (IP, DNS, port, MAC, etc.) is stored in plain `config.json` for easy editing
- Uses **Fernet (AES-128)** encryption from the `cryptography` library
- **PBKDF2** key derivation with 100,000 iterations
- `credentials.enc` cannot be decrypted without the correct master password


## 🌐 Supported Routers

Currently supports **IPTIME** routers (hardcoded).

Future enhancements may include:
- Additional router brands (TP-Link, Asus, etc.)
- Router type selection in configuration


## ⚙️ Tech Stack

- **Python 3.8+**: Core language
- **cryptography**: Encryption/decryption
- **requests**: HTTP communication (router API)
- **Windows MSTSC**: Remote Desktop client


## 🐛 Troubleshooting

### "Failed to load config/credentials: Invalid master password..."

- You entered the wrong master password. Try again.
- If the credentials file is corrupted, delete `credentials.enc` and reconfigure.

### "Router connection failed"

- Check your router URL is correct and accessible
- Verify network connectivity
- Confirm router login credentials

### "WOL transmission failed"

- Ensure MAC address format is correct (e.g., `10:FF:E0:38:F4:D5`)
- Confirm WOL is enabled on your router
- Check that your PC supports Wake-on-LAN (enabled in BIOS/UEFI)

### "Remote Desktop connection failed"

- Verify server address and port
- Ensure the PC has finished booting (may take longer than 5 seconds)
- Confirm Remote Desktop is enabled on the target PC


## 📌 Notes

- **Wake Detection**: If you configure a LAN port number, the program monitors port link status every second for up to 30 seconds. It connects immediately when the PC wakes up, or prompts to continue/abort after timeout.
- **No Port Check**: If LAN port is set to 0 or invalid, uses a simple 5-second wait instead.
- **MSTSC Auto-Login**: If you have saved credentials in Remote Desktop, it will log in automatically. Otherwise, you'll need to enter credentials manually.
- **RDP Port**: Default is 3389. Specify a custom port in the server address if needed (e.g., `192.168.0.100:13389`).
- **Config Structure**: All targets and network info are in `config.json` (plain). All credentials are in `credentials.enc` (encrypted, per target name).

## 📝 License

This project is for personal use.

## 🔄 Version History


### v2.0.0 (2025-11-02)
- **Multi-target support**: Register and select multiple PCs/servers by name
- **Editable config**: All network info in plain `config.json`, only credentials encrypted
- **Migration tool**: Upgrade from old `config.enc` to new format
- **Menu overhaul**: Add/upgrade targets, select target to run, improved flows

### v1.2.0 (2025-11-01)
- Real-time wake detection: Monitors port status every second (up to 30s max)
- Connects immediately when PC is detected awake
- Timeout error with option to continue or abort after 30s

### v1.1.0 (2025-11-01)
- Added router port link status check to skip boot wait if PC is already on
- Improved entry flow: master password prompt first, options menu on blank input
- Fully translated to English

### v1.0.0 (2025-11-01)
- Initial release
- IPTIME router WOL support
- Master password-based encryption
- Automatic Remote Desktop connection

## 🆘 Support

If you encounter issues or have feature requests, please create an issue on GitHub.
