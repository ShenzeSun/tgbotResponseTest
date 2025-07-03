#!/usr/bin/env python3
"""
Session management utility for Telegram Bot Response Monitor
Helps users manage their Telegram sessions.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

def get_session_dir():
    """Get the sessions directory."""
    return os.getenv("SESSION_DIR", "sessions")

def list_sessions():
    """List all existing sessions."""
    session_dir = get_session_dir()
    if not os.path.exists(session_dir):
        print("📁 No sessions directory found.")
        return []
    
    session_files = [f for f in os.listdir(session_dir) if f.endswith('.session')]
    
    if not session_files:
        print("📭 No sessions found.")
        return []
    
    print(f"📋 Found {len(session_files)} session(s):")
    sessions = []
    for session_file in session_files:
        session_name = session_file.replace('.session', '').replace('_bot_monitor', '')
        session_path = os.path.join(session_dir, session_file)
        file_size = os.path.getsize(session_path)
        mod_time = os.path.getmtime(session_path)
        
        from datetime import datetime
        mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"  💾 @{session_name} (Modified: {mod_date}, Size: {file_size} bytes)")
        sessions.append(session_name)
    
    return sessions

def clear_sessions():
    """Clear all sessions."""
    session_dir = get_session_dir()
    if not os.path.exists(session_dir):
        print("📁 No sessions directory found.")
        return
    
    session_files = [f for f in os.listdir(session_dir) if f.endswith('.session') or f.endswith('.session-journal')]
    
    if not session_files:
        print("📭 No sessions to clear.")
        return
    
    print(f"🗑️  Found {len(session_files)} session file(s) to delete:")
    for session_file in session_files:
        print(f"  - {session_file}")
    
    confirm = input("\n❓ Are you sure you want to delete all sessions? (y/N): ").lower()
    if confirm == 'y':
        for session_file in session_files:
            session_path = os.path.join(session_dir, session_file)
            try:
                os.remove(session_path)
                print(f"✅ Deleted: {session_file}")
            except Exception as e:
                print(f"❌ Error deleting {session_file}: {e}")
        print("🎉 All sessions cleared!")
    else:
        print("❌ Operation cancelled.")

def clear_specific_session(username):
    """Clear a specific session."""
    if not username.startswith('@'):
        username = f"@{username}"
    
    session_dir = get_session_dir()
    clean_username = username.replace('@', '')
    session_name = f"{clean_username}_bot_monitor"
    
    session_files = [
        f"{session_name}.session",
        f"{session_name}.session-journal"
    ]
    
    deleted_count = 0
    for session_file in session_files:
        session_path = os.path.join(session_dir, session_file)
        if os.path.exists(session_path):
            try:
                os.remove(session_path)
                print(f"✅ Deleted: {session_file}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Error deleting {session_file}: {e}")
    
    if deleted_count > 0:
        print(f"🎉 Session for {username} cleared!")
    else:
        print(f"📭 No session found for {username}")

def main():
    """Main session management interface."""
    print("🔧 Telegram Bot Response Monitor - Session Management")
    print("=" * 55)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "list":
            list_sessions()
        elif command == "clear":
            if len(sys.argv) > 2:
                username = sys.argv[2]
                clear_specific_session(username)
            else:
                clear_sessions()
        elif command == "help":
            print_help()
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
    else:
        # Interactive mode
        while True:
            print("\n📋 Session Management Options:")
            print("1. 📋 List sessions")
            print("2. 🗑️  Clear all sessions")
            print("3. 🎯 Clear specific session")
            print("4. ❓ Help")
            print("5. 🚪 Exit")
            
            choice = input("\n👉 Enter your choice (1-5): ").strip()
            
            if choice == "1":
                list_sessions()
            elif choice == "2":
                clear_sessions()
            elif choice == "3":
                username = input("👤 Enter username (e.g., @mybot): ").strip()
                if username:
                    clear_specific_session(username)
                else:
                    print("❌ Username cannot be empty")
            elif choice == "4":
                print_help()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")

def print_help():
    """Print help information."""
    print("\n📚 Session Management Help:")
    print("\nCommands:")
    print("  python manage_sessions.py list              - List all sessions")
    print("  python manage_sessions.py clear             - Clear all sessions")
    print("  python manage_sessions.py clear @username   - Clear specific session")
    print("  python manage_sessions.py help              - Show this help")
    print("\nInteractive Mode:")
    print("  python manage_sessions.py                   - Run interactive menu")
    print("\n💡 Tips:")
    print("  - Sessions are stored in the 'sessions/' directory")
    print("  - Clearing sessions will require re-authentication")
    print("  - Sessions are automatically created on first login")

if __name__ == "__main__":
    main()
