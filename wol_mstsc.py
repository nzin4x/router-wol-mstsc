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


def get_master_password(confirm=False):
    """Get master password input"""
    password = getpass.getpass("Enter master password: ")
    
    if confirm:
        password_confirm = getpass.getpass("Confirm master password: ")
        if password != password_confirm:
            print("❌ Passwords do not match")
            sys.exit(1)
    
    return password


def initialize_config():
    """Initial configuration process"""
    print("=" * 60)
    print("🔧 Starting initial configuration")
    print("=" * 60)
    
    # Set master password
    master_password = get_master_password(confirm=True)
    
    # Router information
    print("\n📡 Enter router information (IPTIME)")
    router_url = input("Router URL (e.g., http://192.168.0.1:80): ").strip()
    router_id = input("Router ID: ").strip()
    router_pw = getpass.getpass("Router PW: ")
    
    # PC to wake information
    print("\n💻 Enter PC information to wake")
    mac_address = input("PC MAC address (e.g., 10:FF:E0:38:F4:D5): ").strip()
    
    # MSTSC information
    print("\n🖥️  Enter Remote Desktop information")
    rdp_server = input("Server address (e.g., 192.168.0.100:3389 or domain.com:3389): ").strip()
    rdp_id = input("RDP ID: ").strip()
    rdp_pw = getpass.getpass("RDP PW: ")
    
    # Save configuration
    config_data = {
        "router": {
            "type": "iptime",
            "url": router_url,
            "id": router_id,
            "pw": router_pw
        },
        "wol": {
            "mac_address": mac_address
        },
        "rdp": {
            "server": rdp_server,
            "id": rdp_id,
            "pw": rdp_pw
        }
    }
    
    config_manager = ConfigManager()
    config_manager.save_config(config_data, master_password)
    
    print("\n✅ Configuration completed!")
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


def main():
    """Main program"""
    print("=" * 60)
    print("🚀 WOL-MSTSC Program Start")
    print("=" * 60)
    
    config_manager = ConfigManager()
    
    # Check configuration file
    if not config_manager.config_exists():
        master_password = initialize_config()
    else:
        master_password = get_master_password(confirm=False)
    
    # Load and decrypt configuration
    try:
        config_data = config_manager.load_config(master_password)
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        print("   Please verify your master password")
        sys.exit(1)
    
    print("\n✅ Configuration loaded successfully")
    
    # Execute WOL
    print("\n" + "=" * 60)
    print("📡 Sending WOL packet...")
    print("=" * 60)
    
    try:
        wol = IPTimeWOL(
            router_url=config_data["router"]["url"],
            router_id=config_data["router"]["id"],
            router_pw=config_data["router"]["pw"]
        )
        
        wol.send_wol_packet(config_data["wol"]["mac_address"])
        print("✅ WOL packet sent successfully")
        
    except Exception as e:
        print(f"❌ WOL transmission failed: {e}")
        response = input("\nContinue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    
    # Wait for PC to boot
    print("\n⏳ Waiting for PC to boot... (5 seconds)")
    time.sleep(5)
    
    # MSTSC connection
    print("\n" + "=" * 60)
    print("🖥️  Connecting to Remote Desktop...")
    print("=" * 60)
    
    try:
        mstsc = MSTSCConnector(
            server=config_data["rdp"]["server"],
            username=config_data["rdp"]["id"],
            password=config_data["rdp"]["pw"]
        )
        
        mstsc.connect()
        print("✅ Remote Desktop connection initiated")
        
    except Exception as e:
        print(f"❌ Remote Desktop connection failed: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 All tasks completed!")
    print("=" * 60)


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
