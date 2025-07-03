# Telegram Bot Response Time Monitor

A **production-ready** Python application for monitoring and measuring response times of Telegram bots. This tool helps you track bot performance, identify slow responses, and maintain quality metrics for your Telegram bot services.

## 🚀 Features

### 🔄 **Session Management**

- **One-Time Authentication**: Login once with phone/code, then run forever
- **Persistent Sessions**: Automatic session storage and reuse
- **Session Tools**: Built-in utilities to manage, list, and clear sessions
- **Secure Storage**: Sessions stored in dedicated directory, excluded from git

### 📊 **Monitoring & Analytics**

- **Real-time Monitoring**: Send messages to bots and measure response times
- **Performance Metrics**: Track fast/slow responses with configurable thresholds
- **Batch Processing**: Monitor bots in configurable batches with intervals
- **Detailed Logging**: Comprehensive logging to both file and console with emojis

### 🛡️ **Robustness & Reliability**

- **Advanced Error Handling**: Handles API rate limits, connection issues, and auth errors
- **Graceful Shutdown**: Proper signal handling (Ctrl+C, SIGTERM) for clean termination
- **Auto Recovery**: Handles network issues and Telegram API errors gracefully
- **Stop Controls**: Multiple ways to stop monitoring (signals, flag files, time limits)

### 🔧 **Developer Experience**

- **Environment Configuration**: Secure credential management with `.env` files
- **Guided Setup**: Interactive setup script for easy configuration
- **Configuration Validation**: Built-in tests to validate setup before running
- **Session Testing**: Utilities to test and validate session management

### 🔒 **Security & Privacy**

- **Credential Protection**: API keys stored in `.env` file (never in code)
- **Session Encryption**: Telegram sessions use encrypted storage
- **Git Safety**: All sensitive files automatically excluded from version control

## 📋 Requirements

- Python 3.7+
- Telegram API credentials (API ID and API Hash)
- Active Telegram account

## 🚀 Quick Start

**Complete setup in 5 steps:**

1. **Clone and setup:**

   ```bash
   git clone <repository-url>
   cd tgbotResponseTest
   pip install -r requirements.txt
   ```

2. **Configure credentials:**

   ```bash
   python setup.py
   # Interactive setup - enter your API credentials
   ```

3. **Validate setup:**

   ```bash
   python test_config.py
   # Confirms everything is ready
   ```

4. **Test session management:**

   ```bash
   python test_session_fix.py
   # Validates session handling
   ```

5. **Start monitoring:**
   ```bash
   python res_bot.py
   # First run: Login with phone + verification code
   # Future runs: Instant startup, no login needed!
   ```

### 🔑 **First Run Experience**

```bash
$ python res_bot.py
🔧 Loading configuration...
✅ Configuration loaded successfully
🎯 Target bot: @your_bot
🔑 No existing session found - first-time login required
📱 You will need to enter your phone number and verification code
🔗 Connecting to Telegram...
Please enter your phone number: +1234567890
Please enter the code: 12345
✅ Successfully connected to Telegram
👤 Authenticated as: Your Name (@your_username)
🚀 Starting monitoring...
```

### ⚡ **Subsequent Runs**

```bash
$ python res_bot.py
🔧 Loading configuration...
💾 Found existing session - no login required
🔄 Using existing session (no login required)
✅ Successfully connected to Telegram
🚀 Starting monitoring...
```

## �🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd tgbotResponseTest
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration**:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration:

   ```env
   # Telegram API Configuration
   API_ID=your_api_id_here
   API_HASH=your_api_hash_here

   # Bot Monitoring Configuration
   TARGET_BOT_USERNAME=@your_bot_username
   DURATION_MINUTES=1
   MESSAGE_COUNT=20
   MAX_RUNTIME_HOURS=24
   RESPONSE_THRESHOLD_SECONDS=5
   ```

## 🔑 Getting Telegram API Credentials

1. Visit [my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your Telegram account
3. Create a new application
4. Copy the `API ID` and `API Hash` to your `.env` file

## ⚙️ Configuration Options

| Variable                     | Description                         | Default | Required |
| ---------------------------- | ----------------------------------- | ------- | -------- |
| `API_ID`                     | Telegram API ID                     | -       | ✅       |
| `API_HASH`                   | Telegram API Hash                   | -       | ✅       |
| `TARGET_BOT_USERNAME`        | Bot username to monitor             | @hwjz   | ✅       |
| `DURATION_MINUTES`           | Duration between monitoring batches | 1       | ❌       |
| `MESSAGE_COUNT`              | Number of messages per batch        | 20      | ❌       |
| `MAX_RUNTIME_HOURS`          | Maximum total runtime               | 24      | ❌       |
| `RESPONSE_THRESHOLD_SECONDS` | Threshold for slow responses        | 5       | ❌       |
| `LOOP`                       | Enable continuous monitoring        | true    | ❌       |

### 📝 **Example Configuration**

```env
# Telegram API Configuration (Required)
API_ID=12345678
API_HASH=abcd1234efgh5678ijkl9012mnop3456

# Bot Monitoring Configuration (Optional)
TARGET_BOT_USERNAME=@your_bot_here
DURATION_MINUTES=2
MESSAGE_COUNT=10
MAX_RUNTIME_HOURS=12
RESPONSE_THRESHOLD_SECONDS=3
LOOP=true
```

## 🚦 Usage

### 🎯 **Primary Usage**

**Start monitoring:**

```bash
python res_bot.py
```

**Stop monitoring:**

- Press `Ctrl+C` (graceful shutdown)
- Create `stop.flag` file in project directory
- Automatic stop after `MAX_RUNTIME_HOURS`

### 🛠️ **Utility Scripts**

**Setup and Configuration:**

```bash
python setup.py           # Interactive setup wizard
python test_config.py     # Validate configuration
python test_session_fix.py # Test session management
```

**Session Management:**

```bash
python manage_sessions.py list              # List all sessions
python manage_sessions.py clear             # Clear all sessions
python manage_sessions.py clear @botname    # Clear specific session
python manage_sessions.py                   # Interactive mode
```

### 🌍 **Environment Variables**

You can also use environment variables instead of `.env` file:

```bash
export API_ID=your_api_id
export API_HASH=your_api_hash
export TARGET_BOT_USERNAME=@your_bot
python res_bot.py
```

### 🔄 **Configuration Options**

**Run with custom settings:**

```bash
# Set custom message count and threshold
export MESSAGE_COUNT=50
export RESPONSE_THRESHOLD_SECONDS=3
python res_bot.py
```

**Single run (no loop):**

```bash
export LOOP=false
python res_bot.py
```

## 📊 Output and Logging

The application provides **enhanced logging** with emojis and detailed information:

### 🎨 **Log Message Types**

- **⚡ Fast Response**: Response received within threshold
- **🐌 Slow Response**: Response took longer than threshold
- **❌ No Response**: No response received within 10 seconds
- **🚦 Rate Limited**: Temporary rate limiting by Telegram
- **🔄 Session Status**: Session creation and reuse information
- **👤 Authentication**: User info and login status
- **📊 Statistics**: Batch results and performance metrics
- **⚠️ Warnings**: Non-critical issues
- **❌ Errors**: Critical errors requiring attention

### 📝 **Enhanced Log Output Example**

```bash
2025-07-03 19:41:52 - INFO - 🔧 Loading configuration...
2025-07-03 19:41:52 - INFO - ✅ Configuration loaded successfully
2025-07-03 19:41:52 - INFO - 🎯 Target bot: @your_bot
2025-07-03 19:41:52 - INFO - � Found existing session - no login required
2025-07-03 19:41:52 - INFO - �🚀 Starting Telegram Bot Response Monitor
2025-07-03 19:41:52 - INFO - 📋 Configuration: Target: @your_bot, Messages per batch: 20, Duration: 1 minutes, Loop: True
2025-07-03 19:41:52 - INFO - 🌀 Starting batch loop #1
2025-07-03 19:41:52 - INFO - 🔄 [@your_bot] Using existing session (no login required)
2025-07-03 19:41:52 - INFO - 🔗 [@your_bot] Connecting to Telegram...
2025-07-03 19:41:53 - INFO - ✅ [@your_bot] Successfully connected to Telegram
2025-07-03 19:41:53 - INFO - 👤 [@your_bot] Authenticated as: Your Name (@your_username)
2025-07-03 19:41:53 - INFO - 🔹 [@your_bot] Sending message #1: aB3kM9pL
2025-07-03 19:41:54 - INFO - ⚡ [@your_bot] Fast response time: 0.85s
2025-07-03 19:41:57 - INFO - 🔹 [@your_bot] Sending message #2: xY7nQ2vF
2025-07-03 19:42:03 - WARNING - 🐌 [@your_bot] Slow response (6.12s) for message 'xY7nQ2vF'
2025-07-03 19:42:15 - INFO - 📊 [@your_bot] Batch #1 Result: 1 slow responses out of 20 messages.
```

### 📁 **Log Files**

- **Console Output**: Real-time monitoring with colors and emojis
- **File Output**: `bot_response_times.log` for permanent records
- **Session Logs**: Stored in `sessions/` directory (auto-managed)

## 🛡️ Error Handling

The application includes comprehensive error handling for:

- **Authentication Errors**: Invalid API credentials
- **Rate Limiting**: Automatic retry with exponential backoff
- **Network Issues**: Connection timeouts and network errors
- **API Errors**: Telegram API-specific errors
- **Configuration Errors**: Invalid or missing configuration values

## 🔄 Session Management

The application now features **persistent session management**, meaning you only need to authenticate once:

### 🔑 **First Run (Authentication Required)**

- On first run, you'll need to provide your phone number and verification code
- Sessions are automatically saved in the `sessions/` directory
- This is a **one-time setup** per account

### 🚀 **Subsequent Runs (No Authentication)**

- Sessions are automatically reused
- No need to re-enter credentials or verification codes
- Instant startup and monitoring

### 🛠️ **Session Management Tools**

**List existing sessions:**

```bash
python manage_sessions.py list
```

**Clear all sessions:**

```bash
python manage_sessions.py clear
```

**Clear specific session:**

```bash
python manage_sessions.py clear @botusername
```

**Interactive management:**

```bash
python manage_sessions.py
```

### 📁 **Session Storage**

- Sessions are stored in `sessions/` directory
- Files are automatically excluded from git
- Safe to delete if you want to re-authenticate
- Each bot gets its own session file

### 💡 **Session Tips**

- Sessions persist across computer restarts
- If authentication fails, clear the session and try again
- Sessions are tied to your Telegram account, not the bot
- You can run multiple bots with the same session

## 📁 Project Structure

```
tgbotResponseTest/
├── res_bot.py              # 🚀 Main monitoring application
├── manage_sessions.py      # 🔧 Session management utility
├── setup.py               # 🎯 Guided setup wizard
├── test_config.py         # ✅ Configuration validator
├── test_session_fix.py    # 🔍 Session management tester
├── requirements.txt        # 📦 Python dependencies
├── .env.example           # 📝 Environment configuration template
├── .env                   # 🔐 Your configuration (not in git)
├── .gitignore            # 🚫 Git ignore rules
├── README.md             # 📚 Documentation (this file)
├── LICENSE               # ⚖️ MIT license
├── PROJECT_SUMMARY.md     # 📋 Project overview
├── SESSION_IMPROVEMENTS.md # 🔄 Session management docs
├── __init__.py           # 📄 Package initialization
├── sessions/             # 💾 Session storage directory (auto-created)
├── bot_response_times.log # 📊 Application logs (generated)
└── .git/                 # 🗂️ Git repository data
```

### 📂 **Directory Breakdown**

**Core Application:**

- `res_bot.py` - Main monitoring application with all features
- `requirements.txt` - Minimal dependencies (pyrogram, python-dotenv)

**Utilities & Setup:**

- `setup.py` - Interactive configuration wizard
- `test_config.py` - Validates setup and dependencies
- `test_session_fix.py` - Tests session management functionality
- `manage_sessions.py` - Session management tools

**Configuration:**

- `.env.example` - Template configuration file
- `.env` - Your actual configuration (excluded from git)
- `.gitignore` - Comprehensive exclusions for Python projects

**Documentation:**

- `README.md` - Complete documentation
- `PROJECT_SUMMARY.md` - High-level project overview
- `SESSION_IMPROVEMENTS.md` - Session management details
- `LICENSE` - MIT license for open source distribution

**Generated Files:**

- `sessions/` - Directory for persistent Telegram sessions
- `bot_response_times.log` - Application logs and monitoring data

## 🐛 Troubleshooting

### Common Issues

1. **"API_ID is required"**

   - Ensure your `.env` file contains valid `API_ID` and `API_HASH`
   - Check that the `.env` file is in the project root directory

2. **"Authentication failed"**

   - Verify your API credentials are correct
   - Delete session files and try again
   - Ensure your Telegram account is active

3. **"Rate limited"**

   - The application handles rate limiting automatically
   - Consider increasing delays between messages if persistent

4. **"No response within 10s"**
   - The target bot might be offline or slow
   - Check if the bot username is correct
   - Verify the bot is responsive manually

### Debug Mode

For additional debugging, you can modify the logging level in the code:

```python
logger.setLevel(logging.DEBUG)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This tool is for legitimate monitoring purposes only. Please respect Telegram's Terms of Service and rate limits. The authors are not responsible for any misuse of this tool.

## 🔗 Links

- [Telegram API Documentation](https://core.telegram.org/api)
- [Pyrogram Documentation](https://docs.pyrogram.org/)
- [Python-dotenv Documentation](https://pypi.org/project/python-dotenv/)

## 📞 Support

If you encounter any issues or have questions, please open an issue in the GitHub repository with:

- Detailed description of the problem
- Steps to reproduce
- Your configuration (without sensitive data)
- Relevant log output
