#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration management module
Save/load encrypted configuration files
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

from crypto_utils import encrypt_data, decrypt_data


class ConfigManager:
    """Configuration file management class"""
    
    def __init__(self, config_file: str = "config.enc"):
        """
        Args:
            config_file: Configuration file name
        """
        self.config_dir = Path(__file__).parent
        self.config_path = self.config_dir / config_file
    
    def config_exists(self) -> bool:
        """
        Check if configuration file exists
        
        Returns:
            True if configuration file exists
        """
        return self.config_path.exists()
    
    def save_config(self, config_data: Dict[str, Any], master_password: str):
        """
        Save configuration (encrypted)
        
        Args:
            config_data: Configuration data to save
            master_password: Master password
        """
        # Serialize to JSON
        json_data = json.dumps(config_data, ensure_ascii=False, indent=2)
        
        # Encrypt
        encrypted = encrypt_data(json_data, master_password)
        
        # Save to file
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(encrypted, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Configuration saved: {self.config_path}")
    
    def load_config(self, master_password: str) -> Dict[str, Any]:
        """
        Load configuration (decrypt)
        
        Args:
            master_password: Master password
            
        Returns:
            Configuration data
            
        Raises:
            FileNotFoundError: Configuration file not found
            Exception: Decryption failed
        """
        if not self.config_exists():
            raise FileNotFoundError(f"Configuration file does not exist: {self.config_path}")
        
        # Load encrypted data
        with open(self.config_path, 'r', encoding='utf-8') as f:
            encrypted = json.load(f)
        
        # Decrypt
        json_data = decrypt_data(
            encrypted["encrypted"],
            master_password,
            encrypted["salt"]
        )
        
        # Parse JSON
        config_data = json.loads(json_data)
        
        return config_data
    
    def delete_config(self):
        """Delete configuration file"""
        if self.config_exists():
            self.config_path.unlink()
            print(f"✅ Configuration file deleted: {self.config_path}")
    
    def change_master_password(self, old_password: str, new_password: str):
        """
        Change master password
        
        Args:
            old_password: Current master password
            new_password: New master password
            
        Raises:
            Exception: Old password mismatch or decryption failed
        """
        # Load existing configuration
        config_data = self.load_config(old_password)
        
        # Re-save with new password
        self.save_config(config_data, new_password)
        
        print("✅ Master password changed successfully")
