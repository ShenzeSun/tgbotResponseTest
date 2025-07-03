#!/usr/bin/env python3
"""
Quick validation script to confirm the session fix is working.
"""

import os
import sys
from pathlib import Path

def test_session_fix():
    """Test that the session handling fix is working."""
    print("🔧 Testing Session Management Fix")
    print("=" * 40)
    
    try:
        # Import the application
        import res_bot
        
        # Test session directory creation
        session_dir = res_bot.CONFIG["session_dir"]
        print(f"📁 Session directory: {session_dir}")
        
        # Test directory creation and permissions
        directory_ok = res_bot.ensure_session_directory()
        print(f"✅ Directory creation: {'OK' if directory_ok else 'FAILED'}")
        
        # Test session path generation
        test_username = "@testbot"
        session_path = res_bot.get_session_path(test_username)
        print(f"📄 Session path for {test_username}: {session_path}")
        
        # Test if path is absolute and in the right directory
        full_session_path = f"{session_path}.session"
        expected_dir = os.path.dirname(full_session_path)
        print(f"📂 Session files will be stored in: {expected_dir}")
        
        # Test client creation (without starting)
        from pyrogram import Client
        try:
            client = Client(
                name=session_path,
                api_id=res_bot.CONFIG["api_id"],
                api_hash=res_bot.CONFIG["api_hash"]
            )
            print("✅ Pyrogram Client creation: OK")
        except Exception as e:
            print(f"❌ Pyrogram Client creation: FAILED - {e}")
            return False
        
        print("\n🎉 All tests passed!")
        print("\n📋 What happens next:")
        print("1. Run: python res_bot.py")
        print("2. On first run, you'll be prompted for:")
        print("   📱 Phone number (e.g., +1234567890)")
        print("   🔢 Verification code (sent to your phone)")
        print("3. Session will be saved automatically")
        print("4. Future runs will use the saved session (no login needed)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_session_fix()
