#!/usr/bin/env python3
"""
Test script to validate configuration and dependencies
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import asyncio
        print("  ✅ asyncio")
    except ImportError:
        print("  ❌ asyncio (should be built-in)")
        return False
    
    try:
        import logging
        print("  ✅ logging")
    except ImportError:
        print("  ❌ logging (should be built-in)")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✅ python-dotenv")
    except ImportError:
        print("  ❌ python-dotenv - run: pip install python-dotenv")
        return False
    
    try:
        from pyrogram import Client
        print("  ✅ pyrogram")
    except ImportError:
        print("  ❌ pyrogram - run: pip install pyrogram")
        return False
    
    try:
        from pyrogram.errors import RPCError
        print("  ✅ pyrogram.errors")
    except ImportError:
        print("  ❌ pyrogram.errors")
        return False
    
    return True

def test_config():
    """Test configuration loading."""
    print("\n⚙️  Testing configuration...")
    
    # Check for .env file
    if os.path.exists('.env'):
        print("  ✅ .env file found")
    else:
        print("  ⚠️  .env file not found (will use environment variables)")
    
    # Test loading configuration
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_id = os.getenv("API_ID")
        api_hash = os.getenv("API_HASH")
        target_bot = os.getenv("TARGET_BOT_USERNAME", "@hwjz")
        
        if api_id:
            print(f"  ✅ API_ID found: {api_id[:4]}***")
        else:
            print("  ❌ API_ID not found")
            return False
        
        if api_hash:
            print(f"  ✅ API_HASH found: {api_hash[:4]}***")
        else:
            print("  ❌ API_HASH not found")
            return False
        
        print(f"  ✅ Target bot: {target_bot}")
        
        # Test integer conversion
        try:
            int(api_id)
            print("  ✅ API_ID is valid integer")
        except ValueError:
            print("  ❌ API_ID must be an integer")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

def test_file_permissions():
    """Test file permissions."""
    print("\n📁 Testing file permissions...")
    
    try:
        # Test write permission for log file
        with open('test_log.tmp', 'w') as f:
            f.write('test')
        os.remove('test_log.tmp')
        print("  ✅ Can write log files")
    except Exception as e:
        print(f"  ❌ Cannot write log files: {e}")
        return False
    
    try:
        # Test session file directory
        session_dir = Path('.')
        if session_dir.is_dir() and os.access(session_dir, os.W_OK):
            print("  ✅ Can create session files")
        else:
            print("  ❌ Cannot create session files")
            return False
    except Exception as e:
        print(f"  ❌ Session file error: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🧪 Telegram Bot Response Monitor - Configuration Test")
    print("=" * 55)
    
    all_passed = True
    
    # Run tests
    if not test_imports():
        all_passed = False
    
    if not test_config():
        all_passed = False
    
    if not test_file_permissions():
        all_passed = False
    
    # Summary
    print("\n" + "=" * 55)
    if all_passed:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 You can now run: python res_bot.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\n💡 Run python setup.py for guided setup")
        sys.exit(1)

if __name__ == "__main__":
    main()
