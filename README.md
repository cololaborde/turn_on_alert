<h1 align="center">
  turn on alert
</h1>
<br/>

## Description
This script takes a photo using the default camera and sends it along with a message to a Telegram chat. It also retrieves the device's global IP address and includes it in the message. The script is designed to run on both Windows and Linux.

To use this script, follow the instructions below:

- ### Windows
Create an `alert.bat` file and put it in the following directory: `C:\Users\yourUser\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

```bash
# alert.bat
@echo off
start /B pyw C:\Users\path\to\alert.py
```

- ### Linux
Create a `alert.sh` file

```bash
#!/bin/bash
python3 /path/to/alert.py &
```
Save the file and make it executable by running the following command in the terminal:

```bash
#!/bin/bash
chmod +x /path/to/alert.sh
```

To run the script at startup, you can add it to your system's startup applications. The steps to do this may vary depending on your Linux distribution, but here are some general instructions:

1. Open the "Startup Applications" or "Session and Startup" application.
2. Click on the "Add" or "+" button to add a new startup application.
3. Fill in the name and description (e.g., "Turn On Alert").
4. In the "Command" field, enter the path to the alert.sh file (e.g., /path/to/alert.sh).
5. Save the changes and close the application.


## Requirements
Please note that this script requires the following dependencies:

- cv2 (OpenCV)
- requests
- load_environ (a custom module that loads environment variables)

Before running the script, make sure to set the necessary environment variables:

- tlg_api_key: Your Telegram API token.
- chat_id: The ID of the chat where you want to send the message.

To obtain the chat ID, you can send a message to the bot and access the following URL:
https://api.telegram.org/bot{{api_token}}/getUpdates

## Customization

The script also has configurable options that you can adjust according to your needs:

- RETRIES: The number of retries to attempt when retrieving the global IP address in case of a lack of internet connection. Set it to None for infinite retries. Default is None.
- TIME_OUT: The timeout (in seconds) between each retry. Default is 10.

The retries are particularly useful if there is no internet connection available when the script is executed. By setting the RETRIES option, the script will attempt to retrieve the global IP address multiple times until the connection is established. If the RETRIES value is set to None, the script will keep retrying indefinitely.

You can modify these options by changing the values in the script.

Once you have set the environment variables, adjusted the configurable options (if needed), and followed the instructions for your operating system, the script will take a photo, retrieve the global IP address, and send the message along with the photo to the specified Telegram chat.
