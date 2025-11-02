#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WOL-MSTSC Main Program
Wake-on-LAN + Remote Desktop Connection Tool
"""

import sys
import time
import getpass
import argparse
from pathlib import Path

from crypto_utils import encrypt_data, decrypt_data, verify_password
from config_manager import ConfigManager
from iptime_wol import IPTimeWOL
from mstsc_connector import MSTSCConnector


def get_master_password(confirm=False, prompt="Enter master password: "):
    """Get master password input"""
    password = getpass.getpass(prompt)
    
    if confirm:
        password_confirm = getpass.getpass("Confirm master password: ")
        if password != password_confirm:
            print("❌ Passwords do not match")
            sys.exit(1)
    
    return password


def initialize_config(master_password=None, add_target=False):
    """Initial configuration or add new target"""
    print("=" * 60)
    print("🔧 Starting configuration" if not add_target else "➕ Add new target")
    print("=" * 60)
    config_manager = ConfigManager()
    if not master_password:
        master_password = get_master_password(confirm=True)
    # Load or create config/credentials
    try:
        config = config_manager.load_config() if config_manager.config_exists() else {"targets": []}
    except Exception:
        config = {"targets": []}
    try:
        credentials = config_manager.load_credentials(master_password) if config_manager.credentials_exists() else {}
    except Exception:
        credentials = {}
    # Target name
    name = input("Target name (unique, e.g. 'main' or 'office'): ").strip() or f"target{len(config['targets'])+1}"
    # Router info
    print("\n📡 Enter router information (IPTIME)")
    router_url = input("Router URL (e.g., http://192.168.0.1:80): ").strip()
    router_id = input("Router ID: ").strip()
    router_pw = getpass.getpass("Router PW: ")
    # PC info
    print("\n💻 Enter PC information to wake")
    mac_address = input("PC MAC address (e.g., 1F:2F:3F:4F:5F:6F): ").strip()
    if not mac_address:
        mac_address = "00:00:00:00:00:00"  # Default MAC address if blank
        print(f"[Info] No MAC address entered. Using default: {mac_address}")
    lan_port_str = input("Router LAN port number connected to PC (e.g., 1-4): ").strip()
    try:
        lan_port = int(lan_port_str)
    except ValueError:
        print("⚠️  Invalid port number, defaulting to port check disabled")
        lan_port = 0
    # MSTSC info
    print("\n🖥️  Enter Remote Desktop information")
    rdp_server = input("Server address (e.g., 192.168.0.100:3389 or domain.com:3389): ").strip()
    rdp_id = input("RDP ID: ").strip()
    rdp_pw = getpass.getpass("RDP PW: ")
    # Add to config/credentials
    config["targets"].append({
        "name": name,
        "router": {"type": "iptime", "url": router_url},
        "wol": {"mac_address": mac_address, "lan_port": lan_port},
        "rdp": {"server": rdp_server}
    })
    credentials[name] = {
        "router_id": router_id,
        "router_pw": router_pw,
        "rdp_id": rdp_id,
        "rdp_pw": rdp_pw
    }
    config_manager.save_config(config)
    config_manager.save_credentials(credentials, master_password)
    print(f"\n✅ Target '{name}' added and configuration saved!")
    return master_password


def change_master_password():
    """Change master password"""
    print("=" * 60)
    print("🔑 Change Master Password")
    print("=" * 60)
    
    config_manager = ConfigManager()
    
    # Check configuration file
    if not config_manager.config_exists():
        print("\n❌ Configuration file does not exist")
        print("   Please complete initial configuration first\n")
        sys.exit(1)
    
    print("\nEnter current master password:")
    old_password = getpass.getpass("Current password: ")
    
    # Verify current password
    try:
        config_data = config_manager.load_config(old_password)
        print("✅ Current password verified\n")
    except Exception as e:
        print(f"\n❌ Current password is incorrect: {e}\n")
        sys.exit(1)
    
    # Enter new password
    print("Enter new master password:")
    new_password = get_master_password(confirm=True)
    
    # Change password
    try:
        config_manager.change_master_password(old_password, new_password)
        print("\n✅ Master password changed successfully!\n")
    except Exception as e:
        print(f"\n❌ Failed to change master password: {e}\n")
        sys.exit(1)


def install_command_to_path():
    r"""Install a shortcut command (wolrdp.bat) to %USERPROFILE%\.local\bin and guide PATH setup."""
def uninstall_command_from_path():
    r"""Remove wolrdp.bat from %USERPROFILE%\.local\bin."""
    import os
    user_bin = os.path.expandvars(r"%USERPROFILE%\.local\bin")
    bat_path = os.path.join(user_bin, "wolrdp.bat")
    if os.path.exists(bat_path):
        try:
            os.remove(bat_path)
            print(f"\n✅ 'wolrdp.bat' removed from: {bat_path}")
        except Exception as e:
            print(f"\n[!] Failed to remove: {e}")
    else:
        print(f"\n[!] 'wolrdp.bat' not found in {user_bin}")
    import shutil
    import os
    user_bin = os.path.expandvars(r"%USERPROFILE%\.local\bin")
    os.makedirs(user_bin, exist_ok=True)
    bat_path = os.path.join(user_bin, "wolrdp.bat")
    # Create a simple batch file that runs run.bat in this folder
    script = f"@echo off\ncd /d \"{os.path.dirname(os.path.abspath(__file__))}\"\ncall run.bat %*\n"
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"\n✅ 'wolrdp.bat' installed to: {bat_path}")
    # Check if user_bin is in PATH
    path_env = os.environ.get("PATH", "")
    if user_bin.lower() not in [p.lower() for p in path_env.split(";")]:
        print(f"\n[!] {user_bin} is not in your PATH.")
        print("    Add it to your PATH environment variable to use 'wolrdp' from Win+R or any terminal.")
        print("    Example (PowerShell):")
        print(f"    [Environment]::SetEnvironmentVariable('PATH', $env:PATH + ';{user_bin}', 'User')")
        print("    Or add via Windows System Properties > Environment Variables > User PATH")
    else:
        print("\nYou can now press Win+R and type 'wolrdp' to launch the tool from anywhere!")

def options_menu():
    """Show an interactive options menu for multi-target config."""
    config_manager = ConfigManager()
    while True:
        print("\n" + "=" * 60)
        print("Options")
        print("=" * 60)
        print("1. Add/Configure Target")
        print("2. Run (select target)")
        print("3. Change Master Password")
        print("4. Reset Configuration")
        print("5. Migrate from old config.enc")
        print("6. Install command to PATH (Win+R: wolrdp)")
        print("7. Uninstall command from PATH (remove wolrdp)")
        print("8. Exit")
        print()
        choice = input("Select (1-8): ").strip()
        if choice == "1":
            master_password = get_master_password(confirm=False, prompt="Enter master password: ")
            initialize_config(master_password, add_target=True)
        elif choice == "2":
            master_password = get_master_password(confirm=False, prompt="Enter master password: ")
            run_main_flow(master_password)
        elif choice == "3":
            change_master_password()
        elif choice == "4":
            if config_manager.config_exists() or config_manager.credentials_exists():
                confirm = input("Are you sure you want to delete ALL configuration? (yes/no): ").strip().lower()
                if confirm == "yes":
                    config_manager.delete_config()
                else:
                    print("Cancelled.")
            else:
                print("No configuration file to delete.")
        elif choice == "5":
            master_password = get_master_password(confirm=False, prompt="Enter master password for old config.enc: ")
            config_manager.migrate_from_old("config.enc", master_password)
        elif choice == "6":
            install_command_to_path()
        elif choice == "7":
            uninstall_command_from_path()
        elif choice == "8":
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid selection. Please choose 1-8.")


def run_main_flow(master_password: str):
    """Select target, load config/credentials, run WOL+MSTSC for that target."""
    config_manager = ConfigManager()
    # Load config/credentials
    try:
        config = config_manager.load_config()
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        sys.exit(1)
    try:
        credentials = config_manager.load_credentials(master_password)
    except Exception as e:
        print(f"❌ Failed to load credentials: {e}")
        sys.exit(1)
    # Target 선택
    targets = config.get("targets", [])
    if not targets:
        print("⚠️  No targets configured. Please add a target first.")
        return
    print("\nAvailable targets:")
    for idx, t in enumerate(targets):
        print(f"  {idx+1}. {t['name']} (RDP: {t['rdp']['server']})")
    sel = input(f"Select target (1-{len(targets)}): ").strip()
    try:
        sel_idx = int(sel) - 1
        assert 0 <= sel_idx < len(targets)
    except Exception:
        print("Invalid selection.")
        return
    target = targets[sel_idx]
    name = target["name"]
    cred = credentials.get(name)
    if not cred:
        print(f"❌ No credentials found for target '{name}'. Please re-add this target.")
        return
    # WOL
    print("\n" + "=" * 60)
    print(f"📡 Sending WOL packet for target '{name}'...")
    print("=" * 60)
    wol_obj = None
    try:
        wol_obj = IPTimeWOL(
            router_url=target["router"]["url"],
            router_id=cred["router_id"],
            router_pw=cred["router_pw"]
        )
        wol_obj.send_wol_packet(target["wol"]["mac_address"])
        print("✅ WOL packet sent successfully")
    except Exception as e:
        print(f"❌ WOL transmission failed: {e}")
        response = input("\nContinue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return
    # Wait for PC to wake up
    lan_port = target.get("wol", {}).get("lan_port", 0)
    if wol_obj and lan_port > 0:
        print(f"\n⏳ Waiting for PC to wake up (checking port {lan_port} status)...")
        max_wait_seconds = 30
        check_interval = 1
        for elapsed in range(0, max_wait_seconds, check_interval):
            try:
                if wol_obj.is_lan_port_up(lan_port):
                    print(f"✅ PC is awake! (port {lan_port} up after {elapsed} seconds)")
                    break
            except Exception:
                pass
            if elapsed % 5 == 0 and elapsed > 0:
                print(f"   Still waiting... ({elapsed}/{max_wait_seconds}s)")
            time.sleep(check_interval)
        else:
            print(f"\n❌ Timeout: Could not detect PC wake up after {max_wait_seconds} seconds")
            print("   The PC may still be booting, or WOL may have failed.")
            response = input("   Continue to Remote Desktop anyway? (y/n): ").strip().lower()
            if response != 'y':
                return
    else:
        print("\n⏳ Waiting for PC to boot... (5 seconds, no port check configured)")
        time.sleep(5)
    # MSTSC
    print("\n" + "=" * 60)
    print("🖥️  Connecting to Remote Desktop...")
    print("=" * 60)
    try:
        mstsc = MSTSCConnector(
            server=target["rdp"]["server"],
            username=cred["rdp_id"],
            password=cred["rdp_pw"]
        )
        mstsc.connect()
        print("✅ Remote Desktop connection initiated")
    except Exception as e:
        print(f"❌ Remote Desktop connection failed: {e}")
        return
    print("\n" + "=" * 60)
    print("🎉 All tasks completed!")
    print("=" * 60)


def main():
    """Main program entry: prompt for master password immediately, options menu if blank."""
    print("=" * 60)
    print("🚀 WOL-MSTSC Program Start")
    print("=" * 60)
    
    config_manager = ConfigManager()
    
    # Prompt for master password immediately (or press Enter for options)
    master_password = get_master_password(confirm=False, prompt="Enter master password (or press Enter for options): ")
    
    if master_password == "":
        # Show options menu
        options_menu()
        return
    
    # If no config exists, must initialize first
    if not config_manager.config_exists():
        print("\n⚠️  No configuration found. Starting initial setup...")
        master_password = initialize_config()
    
    # Run the main flow
    run_main_flow(master_password)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='WOL-MSTSC: Wake-on-LAN + Remote Desktop Connection Tool')
    parser.add_argument('--change-password', action='store_true', 
                       help='Change master password')
    
    args = parser.parse_args()
    
    try:
        if args.change_password:
            change_master_password()
        else:
            main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error occurred: {e}")
        sys.exit(1)
