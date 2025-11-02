#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration management module
Save/load encrypted configuration files
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

from crypto_utils import encrypt_data, decrypt_data



class ConfigManager:
    """Configuration file management class (JSON + encrypted credentials)"""
    def __init__(self, config_file: str = "config.json", cred_file: str = "credentials.enc"):
        self.config_dir = Path(__file__).parent
        self.config_path = self.config_dir / config_file
        self.cred_path = self.config_dir / cred_file

    def config_exists(self) -> bool:
        return self.config_path.exists()

    def credentials_exists(self) -> bool:
        return self.cred_path.exists()

    def save_config(self, config_data: dict):
        """Save plain config (targets, no id/pw)"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Config saved: {self.config_path}")

    def load_config(self) -> dict:
        """Load plain config (targets, no id/pw)"""
        if not self.config_exists():
            raise FileNotFoundError(f"Config file does not exist: {self.config_path}")
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_credentials(self, credentials: dict, master_password: str):
        """Save encrypted credentials (id/pw per target)"""
        json_data = json.dumps(credentials, ensure_ascii=False, indent=2)
        encrypted = encrypt_data(json_data, master_password)
        with open(self.cred_path, 'w', encoding='utf-8') as f:
            json.dump(encrypted, f, ensure_ascii=False, indent=2)
        print(f"✅ Credentials saved: {self.cred_path}")

    def load_credentials(self, master_password: str) -> dict:
        """Load encrypted credentials (id/pw per target)"""
        if not self.credentials_exists():
            raise FileNotFoundError(f"Credentials file does not exist: {self.cred_path}")
        with open(self.cred_path, 'r', encoding='utf-8') as f:
            encrypted = json.load(f)
        json_data = decrypt_data(
            encrypted["encrypted"],
            master_password,
            encrypted["salt"]
        )
        return json.loads(json_data)

    def delete_config(self):
        if self.config_exists():
            self.config_path.unlink()
            print(f"✅ Config file deleted: {self.config_path}")
        if self.credentials_exists():
            self.cred_path.unlink()
            print(f"✅ Credentials file deleted: {self.cred_path}")

    def change_master_password(self, old_password: str, new_password: str):
        """Change master password for credentials only"""
        credentials = self.load_credentials(old_password)
        self.save_credentials(credentials, new_password)
        print("✅ Master password changed successfully")

    def migrate_from_old(self, old_enc_file: Optional[str], master_password: str):
        """Migrate from old config.enc (all encrypted) to new split format"""
        if not old_enc_file:
            old_enc_file = "config.enc"
        old_path = self.config_dir / old_enc_file
        if not old_path.exists():
            raise FileNotFoundError(f"Old config file not found: {old_path}")
        with open(old_path, 'r', encoding='utf-8') as f:
            encrypted = json.load(f)
        json_data = decrypt_data(
            encrypted["encrypted"],
            master_password,
            encrypted["salt"]
        )
        old_config = json.loads(json_data)
        # Extract id/pw per target (assume single target, upgrade to multi-target)
        # User must provide a name for the migrated target
        print("\n[Migration] Enter a name for your existing target (e.g. 'main' or 'office'):")
        name = input("Target name: ").strip() or "main"
        # Build new config/credentials structure
        config = {"targets": [{
            "name": name,
            "router": {
                "type": old_config["router"]["type"],
                "url": old_config["router"]["url"]
            },
            "wol": {
                "mac_address": old_config["wol"]["mac_address"],
                "lan_port": old_config["wol"].get("lan_port", 0)
            },
            "rdp": {
                "server": old_config["rdp"]["server"]
            }
        }]}
        credentials = {
            name: {
                "router_id": old_config["router"]["id"],
                "router_pw": old_config["router"]["pw"],
                "rdp_id": old_config["rdp"]["id"],
                "rdp_pw": old_config["rdp"]["pw"]
            }
        }
        self.save_config(config)
        self.save_credentials(credentials, master_password)
        print("\n✅ Migration complete! Please review config.json and add more targets if needed.")
