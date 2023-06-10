# λ-Calculus Telegram Bot

λ-Calculus Bot is a [Telegram](https://telegram.org/) bot based in a lambda-calculus interpreted creted by [Alonzo Church](https://en.wikipedia.org/wiki/Alonzo_Church).

## Features

- λ-Calculus interpreter
- Prefix and infix macro support
- Telegram Bot
- Graph visualization

## Getting Started

### Method 1: Try telegram bot

You'll need to have telegram installed and an account. For more information, please visit [telegram.org](https://telegram.org/).

You can access the bot through the [@λ-Calculus Bot](https://t.me/lambda_calculus_bot) account.

### Method 2: Build own telegram bot

#### 1. Install dependencies
The following dependencies are required:
- python3       version 3.7 or later
- pip
- antlr4        version 4.10 or later
- graphviz
- telegram

After the installation of those packages, we'll install the following python packages:

´´´bash
pip install antlr4-tools                # version 4.10 or later
pip install antlr4-python3-runtime      # version 4.10 or later
pip install python-telegram-bot         # version 20.0 or later
pip install pydot

´´´

#### 2. Get source code
To get the source code you can simmply download the zip file, or you can clone this repository by typing: 

´´´bash
git clone https://github.com/BernatBC/Lambda-Calculus-Telegram-Bot.git

´´´

#### 3. Setting up a Telegram Bot
Message the Telegram account [@BotFather](https://t.me/botfather) and follow it's instructions to create your own bot.

After that create a file `token.txt` inside the repository directory and paste the token generatedby the [@BotFather](https://t.me/botfather) account.

For more information, please visit the [Telegram Bot Guide](https://core.telegram.org/bots#how-do-i-create-a-bot).

#### 4. Run locally
From the repository directory, run the following command:

´´´bash
python3 achurch.py

´´´
Finally you can chat with the bot created.

### Method 3: Execute from terminal

#### 1. Install dependencies
The following dependencies are required:
- python3
- pip
- antlr4

After the installation of those packages, we'll install the following python packages:

´´´bash
pip install antlr4-tools
pip install antlr4-python3-runtime

´´´

#### 2. Get source code
To get the source code you can simmply download the zip file, or you can clone this repository by typing: 
´´´bash
git clone https://github.com/BernatBC/Lambda-Calculus-Telegram-Bot.git

´´´

#### 3. Run locally
Finally, from the repository directory, run the following command:

´´´bash
python3 achurch.py terminal

´´´