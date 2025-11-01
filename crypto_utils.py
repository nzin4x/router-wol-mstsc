#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cryptography utility module
Master password-based data encryption/decryption
"""

import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key_from_password(password: str, salt: bytes) -> bytes:
    """
    Derive encryption key from master password
    
    Args:
        password: Master password
        salt: Salt value
        
    Returns:
        Encryption key (bytes)
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_data(data: str, password: str, salt: bytes = None) -> dict:
    """
    Encrypt data
    
    Args:
        data: Data to encrypt (string)
        password: Master password
        salt: Salt value (auto-generated if None)
        
    Returns:
        {"encrypted": encrypted data, "salt": salt value}
    """
    if salt is None:
        salt = os.urandom(16)
    
    key = derive_key_from_password(password, salt)
    fernet = Fernet(key)
    
    encrypted = fernet.encrypt(data.encode())
    
    return {
        "encrypted": base64.b64encode(encrypted).decode(),
        "salt": base64.b64encode(salt).decode()
    }


def decrypt_data(encrypted_data: str, password: str, salt: str) -> str:
    """
    Decrypt data
    
    Args:
        encrypted_data: Encrypted data (base64 encoded string)
        password: Master password
        salt: Salt value (base64 encoded string)
        
    Returns:
        Decrypted data (string)
        
    Raises:
        Exception: Decryption failed (wrong password, etc.)
    """
    salt_bytes = base64.b64decode(salt)
    encrypted_bytes = base64.b64decode(encrypted_data)
    
    key = derive_key_from_password(password, salt_bytes)
    fernet = Fernet(key)
    
    try:
        decrypted = fernet.decrypt(encrypted_bytes)
        return decrypted.decode()
    except Exception as e:
        raise Exception("Decryption failed: Invalid master password or corrupted data")


def verify_password(encrypted_data: str, password: str, salt: str) -> bool:
    """
    Verify master password
    
    Args:
        encrypted_data: Encrypted data
        password: Password to verify
        salt: Salt value
        
    Returns:
        True if password matches
    """
    try:
        decrypt_data(encrypted_data, password, salt)
        return True
    except:
        return False


def hash_password(password: str) -> str:
    """
    Generate password hash (for verification)
    
    Args:
        password: Password to hash
        
    Returns:
        Hash value (hex string)
    """
    return hashlib.sha256(password.encode()).hexdigest()
