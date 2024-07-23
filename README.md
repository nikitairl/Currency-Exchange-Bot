# Currency Exchange Bot

This project is a Telegram bot that provides up-to-date currency exchange rates from the Central Bank of Russia. The bot allows users to fetch the latest exchange rates and perform currency conversions directly within Telegram.

## Features

- **Fetch Exchange Rates**: Retrieves the latest exchange rates from the Central Bank of Russia.
- **Currency Conversion**: Converts a specified amount from one currency to another using the latest exchange rates.
- **Interactive Buttons**: Provides easy-to-use buttons for fetching exchange rates and performing currency conversions.

## Technologies Used

- **Python**: The core programming language used for the bot.
- **aiogram v3**: A modern and fully asynchronous framework for Telegram bot development.
- **aiohttp**: An asynchronous HTTP client for fetching the XML file containing the exchange rates.
- **xml.etree.ElementTree**: A built-in Python library for parsing XML data.
- **redis**: A key-value database for storing exchange rates.
- **dotenv**: A module for loading environment variables from a `.env` file.
- **docker-compose**: A tool for defining and running multi-container Docker applications.

## Setup and Installation

### Prerequisites

- Docker and Docker Compose installed on your machine.
- A Telegram bot token from BotFather.
- Redis installed locally or accessible via a network.

### Installation Steps

1. **Clone the repository**:
    ```sh
    git clone https://github.com/nikitairl/Ukolov_test_case.git
    cd currency-exchange-bot
    ```

2. **Create a `.env` file** in the root directory and add your bot token and the Central Bank of Russia URL:
    ```env
    BOT_API_TOKEN=your_telegram_bot_token
    PARSE_URL=https://www.cbr.ru/scripts/XML_daily.asp
    ```

3. **Build and run the application** using Docker Compose:
    ```sh
    docker-compose up --build
    ```

## Usage

1. **Start the Bot**: Ensure the bot is running via Docker Compose.

2. **Interact with the Bot**:
    - Use the `/start` command to receive a welcome message and interactive buttons.
    - Press the `/rates` button to fetch the latest exchange rates.
    - Use the `/exchange USD BYN 10` command to convert 10 USD to BYN (replace with desired currencies and amount).

## Logging

The bot includes detailed logging for monitoring and debugging purposes. Log messages include information about fetching data, parsing XML, and updating Redis. Errors are also logged to help identify and resolve issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
