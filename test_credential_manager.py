#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Windows Credential Manager integration
"""

import sys
from crypto_utils import (
    is_keyring_available,
    save_master_password,
    load_master_password,
    delete_master_password
)


def test_credential_manager():
    """Test credential manager functions"""
    print("=" * 60)
    print("Windows Credential Manager Test")
    print("=" * 60)
    
    # Check availability
    print("\n1. Checking keyring availability...")
    if is_keyring_available():
        print("   ✅ Windows Credential Manager is available")
    else:
        print("   ❌ Windows Credential Manager is NOT available")
        print("   Please install keyring: pip install keyring")
        return False
    
    # Save test password
    print("\n2. Saving test password...")
    test_password = "test_password_123"
    if save_master_password(test_password):
        print(f"   ✅ Successfully saved: '{test_password}'")
    else:
        print("   ❌ Failed to save password")
        return False
    
    # Load password
    print("\n3. Loading password...")
    loaded_password = load_master_password()
    if loaded_password:
        print(f"   ✅ Successfully loaded: '{loaded_password}'")
        if loaded_password == test_password:
            print("   ✅ Password matches!")
        else:
            print(f"   ❌ Password mismatch! Expected '{test_password}', got '{loaded_password}'")
            return False
    else:
        print("   ❌ Failed to load password")
        return False
    
    # Delete password
    print("\n4. Deleting password...")
    if delete_master_password():
        print("   ✅ Successfully deleted")
    else:
        print("   ⚠️  Delete returned False (password might not exist)")
    
    # Verify deletion
    print("\n5. Verifying deletion...")
    loaded_after_delete = load_master_password()
    if loaded_after_delete is None:
        print("   ✅ Password successfully deleted (no longer exists)")
    else:
        print(f"   ❌ Password still exists: '{loaded_after_delete}'")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    try:
        success = test_credential_manager()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
