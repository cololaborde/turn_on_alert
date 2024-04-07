# Telegram startup alert && control

This program runs upon system startup and serves as an alert for computer booting. It also offers control options via buttons in a Telegram chat to execute specific actions.

## Features
- #### Startup Alert: 
    Upon system boot, the program sends an alert message to a designated Telegram chat, providing information about the system startup, such as username and IP address.

- #### Control Options: 
    The program allows interaction via buttons in a Telegram chat to perform various actions on the system.

## Telegram Bot Setup
- #### Bot Creation:

    Create a Telegram bot and obtain the API token. You can do this by chatting with the BotFather on Telegram.

- #### Obtaining Chat ID:

    Send a message to your bot and access the URL https://api.telegram.org/bot<API_TOKEN>/getUpdates to retrieve the chat ID. Look for the chat object in the JSON response.

## Configuration
- #### Environment Variables Loader:

    Use the following environment variables loader to configure the necessary variables before running the program:

```bash
# python
import os 

def load_environ():
    os.environ['tlg_api_key'] = ''  # Assign your Telegram bot's API token here
    os.environ['chat_id'] = ''       # Assign your Telegram chat ID here
    os.environ["photo_name"] = ""  # Path to the image for taking photos
```
Make sure to replace the empty strings ('') with the corresponding values for the API token and chat ID.

- #### System Startup Setup:

Configure your system to run this program upon startup. Depending on your operating system, you can achieve this by adding the program to startup applications or using task scheduler.

- #### Dependencies:

Make sure all dependencies required by the program are installed. Refer to the requirements.txt file for details.

## Usage

### 1. Startup Alert:

Upon system boot, the program automatically sends an alert message to the designated Telegram chat, including information about the system startup.

### 2. Control Options:

Interact with the program via buttons in the Telegram chat to perform various actions on the system. Some available options may include:
Was me: Mark the system startup as safe.
Take Photo: Capture a photo using the system camera.
Screenshot: Take a screenshot of the system screen.
Lock Screen: Lock the system screen.
Turn Off: Shut down the system.
You can add more options as needed.


## Notes

Ensure proper configuration of environment variables and Telegram bot settings for seamless operation.
Customize the behavior of the program and control options according to your preferences and system requirements.
It's recommended to run this program in a secure environment and grant necessary permissions only to trusted users.