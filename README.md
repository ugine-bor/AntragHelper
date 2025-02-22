# Antrag Helper Bot

[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://t.me/Long_name_my_bot)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-green)
![Aiogram](https://img.shields.io/badge/Framework-Aiogram%202.x-orange)

A smart multi-language Telegram bot designed to streamline your document preparation process for official
applications ("Antrag"). Get instant PDF generation or premium-assisted document processing with just a few clicks!

## Features

- **Multi-language Support**  
  Choose between English, Deutsch, Русский, or فارسی interfaces
- **Two Service Packages**
    - **Basic Package**: Instant PDF generation within 1 minute
    - **Premium Package**: Full-service document processing with 3-day turnaround
- **Free Trial Available**  
  Test the bot's capabilities with a complimentary trial
- **User Account Management**  
  Track your active services and account status

## Getting Started

### Prerequisites

- Python 3.8+
- Telegram account
- Aiogram 2.x framework

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ugine-bor/AntragHelper.git
   cd AntragHelper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your Telegram bot token in `config.py`

### Usage

1. Start the bot in Telegram:
   ```
   /start
   ```
2. Choose your preferred language
3. Select your service package:
    - `/basic` for instant PDF generation
    - `/plus` for premium document processing

## Command Reference

| Command   | Description                        |
|-----------|------------------------------------|
| `/start`  | Initialize bot and select language |
| `/help`   | Show help message and command list |
| `/basic`  | Access Basic Package features      |
| `/plus`   | Access Premium Package features    |
| `/info`   | View account information           |
| `/lang`   | Change interface language          |
| `/webapp` | Open integrated web application    |
| `/end`    | Cancel current operation           |

## Supported Languages

- English 🇬🇧
- Deutsch 🇩🇪
- Русский 🇷🇺
- فارسی 🇮🇷

## Technical Overview

- Built with Aiogram asynchronous framework
- State machine for conversation flow
- Multi-language implementation using i18n
- User data storage architecture

---
