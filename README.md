# WOL-MSTSC

**Wake-on-LAN + Remote Desktop Connection Tool**

A Windows utility that wakes up a remote PC via your router (Wake-on-LAN) and automatically connects to it via Remote Desktop (MSTSC).

## 🎯 Key Features

- ✅ **Master Password Security**: All sensitive data (router & RDP credentials) encrypted with a master password
- ✅ **IPTIME Router Support**: Send WOL packets via IPTIME routers
- ✅ **Smart Boot Detection**: Checks router port link status to skip wait if PC is already on
- ✅ **Automatic Remote Desktop**: Launches MSTSC after WOL
- ✅ **Easy Setup**: Interactive configuration on first run
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

### First Run (Initial Setup)

Run `run.bat` (or `python wol_mstsc.py`):

```bash
run.bat
```

**You will be prompted for your master password immediately.**

- **Enter a password**: Proceeds with configuration or runs the WOL flow if already configured
- **Press Enter (blank)**: Opens the options menu for setup, password change, or reset

#### Initial Configuration

On first run (or after selecting "Configure and Run" from the options menu), you'll provide:

1. **Master Password**: Entered twice to confirm (encrypts all settings)
2. **Router Information** (IPTIME):
   - URL (e.g., `http://192.168.0.1:80` or `http://14.39.91.241:8112`)
   - Login ID
   - Login Password
3. **PC to Wake**:
   - MAC Address (e.g., `10:FF:E0:38:F4:D5`)
   - Router LAN Port Number (e.g., `4` if your PC is connected to LAN port 4; used to detect if PC is already on)
4. **Remote Desktop**:
   - Server Address (e.g., `192.168.0.100:3389` or `domain.com:3389`)
   - RDP Username
   - RDP Password

All configuration is saved encrypted in `config.enc`.

### Normal Use

After setup, just run `run.bat` and enter your master password when prompted. The program will:

1. Login to your router
2. Send WOL packet to wake your PC
3. **Check if PC is already on** (via router port link status)
4. Wait 5 seconds if needed, or skip wait if PC is already on
5. Launch Remote Desktop (MSTSC) to connect

## 🔧 Options Menu

Press **Enter** (blank) at the master password prompt to access:

- **Configure and Run**: Overwrite current config and proceed
- **Change Master Password**: Update your master password (keeps all other settings)
- **Reset Configuration**: Delete `config.enc` and start fresh
- **Exit**: Quit the program

You can also use command-line arguments:

```bash
python wol_mstsc.py --change-password
python wol_mstsc.py --reset-config
```

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
├── config.enc            # Encrypted config (auto-generated)
└── README.md             # This file
```

## 🔐 Security

- All sensitive data (router credentials, RDP credentials) is encrypted with your master password
- Uses **Fernet (AES-128)** encryption from the `cryptography` library
- **PBKDF2** key derivation with 100,000 iterations
- `config.enc` cannot be decrypted without the correct master password

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

### "Failed to load configuration: Invalid master password..."

- You entered the wrong master password. Try again.
- If the config file is corrupted, delete `config.enc` and reconfigure.

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

- **Boot Wait Time**: Defaults to 5 seconds. If port link status check is enabled (you provided a LAN port number), the wait is automatically skipped if the PC is already on.
- **MSTSC Auto-Login**: If you have saved credentials in Remote Desktop, it will log in automatically. Otherwise, you'll need to enter credentials manually.
- **RDP Port**: Default is 3389. Specify a custom port in the server address if needed (e.g., `192.168.0.100:13389`).

## 📝 License

This project is for personal use.

## 🔄 Version History

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
