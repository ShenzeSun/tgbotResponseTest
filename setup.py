#!/usr/bin/env python3
"""
Setup script for Telegram Bot Response Monitor
Helps users configure the application on first run.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create a .env file with user input."""
    print("🔧 Telegram Bot Response Monitor Setup")
    print("=" * 40)
    
    if os.path.exists('.env'):
        overwrite = input("📄 .env file already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("✅ Keeping existing .env file.")
            return
    
    print("\n📋 Please provide your Telegram API credentials:")
    print("   Get them from: https://my.telegram.org/apps")
    
    api_id = input("\n🔑 API ID: ").strip()
    api_hash = input("🔑 API Hash: ").strip()
    
    if not api_id or not api_hash:
        print("❌ API ID and API Hash are required!")
        return False
    
    bot_username = input("\n🤖 Target bot username (e.g., @mybot): ").strip()
    if not bot_username:
        bot_username = "@hwjz"
    
    if not bot_username.startswith('@'):
        bot_username = f"@{bot_username}"
    
    # Optional configuration
    print("\n⚙️  Optional configuration (press Enter for defaults):")
    duration = input("⏱️  Duration between batches in minutes (1): ").strip() or "1"
    message_count = input("📨 Messages per batch (20): ").strip() or "20"
    max_runtime = input("⏰ Max runtime in hours (24): ").strip() or "24"
    threshold = input("🐌 Slow response threshold in seconds (5): ").strip() or "5"
    loop_enabled = input("🔄 Enable continuous monitoring? (Y/n): ").strip().lower()
    loop_enabled = "true" if loop_enabled != 'n' else "false"
    
    # Create .env content
    env_content = f"""# Telegram API Configuration
# Get these from https://my.telegram.org/apps
API_ID={api_id}
API_HASH={api_hash}

# Bot Monitoring Configuration
TARGET_BOT_USERNAME={bot_username}
DURATION_MINUTES={duration}
MESSAGE_COUNT={message_count}
MAX_RUNTIME_HOURS={max_runtime}
RESPONSE_THRESHOLD_SECONDS={threshold}
LOOP={loop_enabled}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error creating .env file: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import pyrogram
        import dotenv
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def main():
    """Main setup function."""
    print("🚀 Welcome to Telegram Bot Response Monitor Setup!")
    
    # Check if we're in the right directory
    if not os.path.exists('res_bot.py'):
        print("❌ Please run this script from the project directory")
        sys.exit(1)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    # Create .env file
    print("\n📝 Setting up configuration...")
    if create_env_file():
        print("\n🎉 Setup completed successfully!")
        print("\n🚀 You can now run the monitor with:")
        print("   python res_bot.py")
        print("\n📚 Check README.md for more information")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
