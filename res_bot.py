import asyncio
import logging
import random
import string
import time
import os
import sys
import signal
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.errors import (
    AuthKeyUnregistered, 
    UserDeactivated, 
    FloodWait, 
    RPCError,
    SessionPasswordNeeded,
    PhoneNumberInvalid
)

# Load environment variables
load_dotenv()

# ----- CONFIGURATION -----
def load_config() -> Dict[str, Any]:
    """Load and validate configuration from environment variables."""
    config = {
        "api_id": os.getenv("API_ID"),
        "api_hash": os.getenv("API_HASH"),
        "target_bot_username": os.getenv("TARGET_BOT_USERNAME", "@hwjz"),
        "loop": os.getenv("LOOP", "true").lower() == "true",
        "duration_minutes": int(os.getenv("DURATION_MINUTES", "1")),
        "message_count": int(os.getenv("MESSAGE_COUNT", "20")),
        "max_runtime_hours": int(os.getenv("MAX_RUNTIME_HOURS", "24")),
        "response_threshold_seconds": float(os.getenv("RESPONSE_THRESHOLD_SECONDS", "5")),
        "stop_flag_file": "stop.flag"
    }
    
    # Validate required configuration
    if not config["api_id"]:
        raise ValueError("API_ID is required. Please set it in your .env file.")
    if not config["api_hash"]:
        raise ValueError("API_HASH is required. Please set it in your .env file.")
    if not config["target_bot_username"]:
        raise ValueError("TARGET_BOT_USERNAME is required. Please set it in your .env file.")
    
    try:
        config["api_id"] = int(config["api_id"])
    except ValueError:
        raise ValueError("API_ID must be a valid integer.")
    
    if not config["target_bot_username"].startswith("@"):
        config["target_bot_username"] = f"@{config['target_bot_username']}"
    
    return config

# Global configuration
CONFIG = load_config()

# ----- LOGGING SETUP -----
def setup_logging() -> logging.Logger:
    """Set up logging configuration."""
    logger = logging.getLogger("BotMonitor")
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler("bot_response_times.log")
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Stream (console) handler
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)
    
    return logger

logger = setup_logging()

# ----- GLOBAL STATE -----
shutdown_event = asyncio.Event()

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}. Initiating graceful shutdown...")
    shutdown_event.set()

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ----- UTILITY -----
def generate_random_message(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ----- MAIN CHECK FUNCTION -----
async def monitor_bot_responses(username: str) -> int:
    """
    Monitor bot response times for a specific username.
    
    Args:
        username: The bot username to monitor
        
    Returns:
        Number of slow responses detected
    """
    client = None
    try:
        client = Client(
            name=f"{username.replace('@', '')}_session", 
            api_id=CONFIG["api_id"], 
            api_hash=CONFIG["api_hash"]
        )
        
        logger.info(f"🔗 [{username}] Connecting to Telegram...")
        await client.start()
        logger.info(f"✅ [{username}] Successfully connected to Telegram")
        
        slow_responses = 0
        end_time = datetime.now() + timedelta(minutes=CONFIG["duration_minutes"])
        message_sent = 0

        while (datetime.now() < end_time and 
               message_sent < CONFIG["message_count"] and 
               not shutdown_event.is_set()):
            
            try:
                msg_text = generate_random_message()
                logger.info(f"🔹 [{username}] Sending message #{message_sent + 1}: {msg_text}")
                
                sent_msg = await client.send_message(username, msg_text)
                sent_time = sent_msg.date.timestamp()

                # Wait up to 10s for response
                max_wait = 10
                check_interval = 0.5
                waited = 0
                response_time = None

                while not response_time and waited < max_wait and not shutdown_event.is_set():
                    await asyncio.sleep(check_interval)
                    waited += check_interval
                    
                    try:
                        async for message in client.get_chat_history(username, limit=10):
                            if message.id != sent_msg.id and message.date.timestamp() > sent_time:
                                response_time = message.date.timestamp()
                                break
                    except RPCError as e:
                        logger.warning(f"⚠️ [{username}] Error fetching chat history: {e}")
                        break

                if response_time:
                    diff = response_time - sent_time
                    if diff > CONFIG["response_threshold_seconds"]:
                        slow_responses += 1
                        logger.warning(f"🐌 [{username}] Slow response ({diff:.2f}s) for message '{msg_text}'")
                    else:
                        logger.info(f"⚡ [{username}] Fast response time: {diff:.2f}s")
                else:
                    if not shutdown_event.is_set():
                        logger.warning(f"❌ [{username}] No response within 10s for message '{msg_text}'")

                message_sent += 1
                
                # Random delay between messages to avoid rate limiting
                if not shutdown_event.is_set():
                    delay = random.uniform(2, 5)
                    await asyncio.sleep(delay)
                    
            except FloodWait as e:
                logger.warning(f"🚦 [{username}] Rate limited. Waiting {e.value} seconds...")
                await asyncio.sleep(e.value)
            except RPCError as e:
                logger.error(f"❌ [{username}] Telegram API error: {e}")
                break
            except Exception as e:
                logger.error(f"❌ [{username}] Unexpected error sending message: {e}")
                break

        logger.info(f"🔚 [{username}] Finished. Sent: {message_sent}, Slow responses (> {CONFIG['response_threshold_seconds']}s): {slow_responses}")
        return slow_responses
        
    except AuthKeyUnregistered:
        logger.error(f"❌ [{username}] Authentication failed. Please check your API credentials.")
        return -1
    except UserDeactivated:
        logger.error(f"❌ [{username}] User account is deactivated.")
        return -1
    except SessionPasswordNeeded:
        logger.error(f"❌ [{username}] Two-factor authentication is enabled. Please disable it or implement 2FA handling.")
        return -1
    except PhoneNumberInvalid:
        logger.error(f"❌ [{username}] Invalid phone number in session.")
        return -1
    except Exception as e:
        logger.error(f"❌ [{username}] Unexpected error during monitoring: {e}")
        return -1
    finally:
        if client:
            try:
                await client.stop()
                logger.info(f"🔌 [{username}] Disconnected from Telegram")
            except Exception as e:
                logger.warning(f"⚠️ [{username}] Error during disconnect: {e}")

# ----- LOOP LOGIC -----
async def main_loop():
    """Main monitoring loop with error handling and graceful shutdown."""
    start_time = time.time()
    loop_count = 0

    logger.info("🚀 Starting Telegram Bot Response Monitor")
    logger.info(f"📋 Configuration: Target: {CONFIG['target_bot_username']}, "
                f"Messages per batch: {CONFIG['message_count']}, "
                f"Duration: {CONFIG['duration_minutes']} minutes, "
                f"Loop: {CONFIG['loop']}")

    try:
        while not shutdown_event.is_set():
            logger.info(f"🌀 Starting batch loop #{loop_count + 1}")

            # Monitor single bot
            slow_responses = await monitor_bot_responses(CONFIG["target_bot_username"])
            
            if slow_responses == -1:
                logger.error("💥 Critical error occurred. Stopping monitoring.")
                break

            logger.info(
                f"📊 [{CONFIG['target_bot_username']}] Batch #{loop_count + 1} Result: "
                f"{slow_responses} slow responses out of {CONFIG['message_count']} messages."
            )

            loop_count += 1

            # Check various exit conditions
            if not CONFIG["loop"]:
                logger.info("🔁 Loop disabled in configuration. Exiting.")
                break

            if os.path.exists(CONFIG["stop_flag_file"]):
                logger.info("🛑 Stop flag file detected. Exiting loop.")
                try:
                    os.remove(CONFIG["stop_flag_file"])
                except OSError as e:
                    logger.warning(f"⚠️ Could not remove stop flag file: {e}")
                break

            elapsed_hours = (time.time() - start_time) / 3600
            if elapsed_hours >= CONFIG["max_runtime_hours"]:
                logger.info(f"⏹️ Max runtime ({CONFIG['max_runtime_hours']} hours) reached. Stopping loop.")
                break

            if shutdown_event.is_set():
                break

            # Wait before next batch
            logger.info(f"😴 Waiting {CONFIG['duration_minutes']} minutes before next batch...")
            
            # Break the sleep into smaller chunks to allow for faster shutdown
            sleep_chunks = CONFIG["duration_minutes"] * 12  # 5-second chunks
            for _ in range(sleep_chunks):
                if shutdown_event.is_set():
                    break
                await asyncio.sleep(5)

    except KeyboardInterrupt:
        logger.info("🛑 Keyboard interrupt received. Shutting down...")
    except Exception as e:
        logger.error(f"💥 Unexpected error in main loop: {e}")
    finally:
        total_runtime = (time.time() - start_time) / 3600
        logger.info(f"🏁 Monitor stopped. Total runtime: {total_runtime:.2f} hours, Completed batches: {loop_count}")

# ----- ENTRY -----
def main():
    """Main entry point with configuration validation and error handling."""
    try:
        # Validate configuration on startup
        logger.info("🔧 Loading configuration...")
        logger.info(f"✅ Configuration loaded successfully")
        logger.info(f"🎯 Target bot: {CONFIG['target_bot_username']}")
        
        # Check if .env file exists
        if not os.path.exists('.env'):
            logger.warning("⚠️ No .env file found. Using environment variables or defaults.")
            logger.info("💡 Create a .env file based on .env.example for easier configuration.")
        
        # Run the main loop
        asyncio.run(main_loop())
        
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.info("💡 Please check your .env file or environment variables.")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("🛑 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
