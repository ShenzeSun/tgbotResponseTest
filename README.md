# Telegram Bot Response Time Monitor

A robust Python application for monitoring and measuring response times of Telegram bots. This tool helps you track bot performance, identify slow responses, and maintain quality metrics for your Telegram bot services.

## 🚀 Features

- **Real-time Monitoring**: Send messages to bots and measure response times
- **Configurable Thresholds**: Set custom response time thresholds
- **Robust Error Handling**: Handles API rate limits, connection issues, and authentication errors
- **Detailed Logging**: Comprehensive logging to both file and console
- **Graceful Shutdown**: Proper signal handling for clean termination
- **Environment Configuration**: Secure credential management with `.env` files
- **Batch Processing**: Monitor bots in configurable batches with customizable intervals
- **Stop Controls**: Multiple ways to stop monitoring (signals, flag files, time limits)
- **Persistent Sessions**: Automatic session management - login once, run multiple times
- **Session Management**: Built-in tools to manage and clear sessions

## 📋 Requirements

- Python 3.7+
- Telegram API credentials (API ID and API Hash)
- Active Telegram account

## � Quick Start

**For first-time users:**

1. Clone and enter the project:

   ```bash
   git clone <repository-url>
   cd tgbotResponseTest
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the guided setup:

   ```bash
   python setup.py
   ```

4. Test your configuration:

   ```bash
   python test_config.py
   ```

5. Start monitoring:
   ```bash
   python res_bot.py
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

## 🚦 Usage

### Basic Usage

Start monitoring with default settings:

```bash
python res_bot.py
```

### Environment Variables

You can also use environment variables instead of a `.env` file:

```bash
export API_ID=your_api_id
export API_HASH=your_api_hash
export TARGET_BOT_USERNAME=@your_bot
python res_bot.py
```

### Stopping the Monitor

The application can be stopped in several ways:

1. **Keyboard Interrupt**: Press `Ctrl+C`
2. **Stop Flag File**: Create a file named `stop.flag` in the project directory
3. **Time Limit**: Automatically stops after `MAX_RUNTIME_HOURS`
4. **Single Run**: Set `LOOP=false` in configuration

## 📊 Output and Logging

The application provides detailed logging both to the console and to `bot_response_times.log`:

- **✅ Fast Response**: Response received within threshold
- **🐌 Slow Response**: Response took longer than threshold
- **❌ No Response**: No response received within 10 seconds
- **🚦 Rate Limited**: Temporary rate limiting by Telegram
- **⚠️ Warnings**: Non-critical issues
- **❌ Errors**: Critical errors requiring attention

### Sample Log Output

```
2025-07-03 10:30:15 - INFO - 🚀 Starting Telegram Bot Response Monitor
2025-07-03 10:30:15 - INFO - 📋 Configuration: Target: @testbot, Messages per batch: 5, Duration: 1 minutes, Loop: True
2025-07-03 10:30:16 - INFO - ✅ [@testbot] Successfully connected to Telegram
2025-07-03 10:30:16 - INFO - 🔹 [@testbot] Sending message #1: aB3kM9pL
2025-07-03 10:30:17 - INFO - ⚡ [@testbot] Fast response time: 0.85s
2025-07-03 10:30:20 - INFO - 🔹 [@testbot] Sending message #2: xY7nQ2vF
2025-07-03 10:30:26 - WARNING - 🐌 [@testbot] Slow response (6.12s) for message 'xY7nQ2vF'
```

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
├── res_bot.py              # Main application
├── manage_sessions.py      # Session management utility
├── setup.py               # Guided setup script
├── test_config.py         # Configuration validator
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── .env                   # Your configuration (not in git)
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── LICENSE               # MIT license
├── sessions/             # Session storage directory (generated)
├── bot_response_times.log # Application logs (generated)
└── *.session*            # Legacy session files (auto-moved to sessions/)
```

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
