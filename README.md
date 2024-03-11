# Control Device By Telegram

This Python script allows you to control your computer through a Telegram bot. You can perform various tasks such as taking screenshots, displaying task lists, terminating applications, sending notifications, opening URLs, and initiating shutdown or restart commands remotely via Telegram.

## Getting Started

### Prerequisites

- Python 3.x installed on your computer.
- Required Python packages can be installed using the provided `requirements.txt` file.

### Installation

1. Clone this repository to your local machine using:

```bash
git clone https://github.com/Hungnth/control-device-by-telegram.git
```

2. Navigate to the project directory:

```bash
cd control-device-by-telegram
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Configuration

1. Obtain a Telegram bot API token.
2. Open a file named `apiKey.py` inside the `config` directory.
3. Add your Telegram bot API token to `apiKey.py`:

```python
ACCESS_TOKEN = "YOUR_TELEGRAM_BOT_API_TOKEN"
ID_CHAT = "YOUR_TELEGRAM_CHAT_ID"
```

Replace `"YOUR_TELEGRAM_BOT_API_TOKEN"` with your actual Telegram bot API token and `"YOUR_TELEGRAM_CHAT_ID"` with your Telegram chat ID.

## Usage

1. Run the Python script `main.py`.
2. Start or send a message to your Telegram bot.
3. Use the provided commands to perform various actions:
   - `/help` or `/start`: Display available options.
   - `Screenshot 🖥️`: Take a screenshot of your computer screen.
   - `Tasklist 📑`: Display running applications/tasks.
   - `Stop App ❌`: Terminate a specific application.
   - `Notification 🔔`: Send a notification message.
   - `Open Url 🔗`: Open a URL in the default web browser.
   - `Shutdown 🅾️` or `Restart 🔄`: Initiate shutdown or restart commands (confirmation required).

## Contributing

Contributions are welcome! Please feel free to open a pull request or submit an issue for any improvements or fixes you'd like to make.

## License

This project is licensed under the MIT License.


## Credits

This project is inspired by [DucThinhEXE's Control Device In Telegram](https://github.com/DucThinhEXE/Control-Device-In-Telegram). Special thanks to the original author for their contribution.

Feel free to contribute to this project by submitting bug reports, feature requests, or pull requests. Your contributions are highly appreciated!
"#control-device-by-telegram" 
