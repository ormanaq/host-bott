# HostingKarle Referral Registration Bot

A Python script to automate website registrations for HostingKarle using referral codes with human-like information and proxy rotation.

## Features

- Automatically generates random human-like user information (names, emails, etc.)
- Automatically fetches and rotates free proxies from public sources
- Extracts referral code from the registration URL
- Limits registrations to 500 per day to avoid suspicion
- Saves successful registrations to `accounts.csv`
- Detailed logging in `registration.log`
- Random delays between registrations to mimic human behavior
- User-agent rotation for better anonymity

## Setup

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. No need to add proxies manually - the script automatically fetches them for you!

## Usage

Run the script:
```
python auto_register.py
```

The script is pre-configured with the HostingKarle URL and referral code: `Hz4shhcR`

## Customization

If you want to change the number of registrations, edit the line at the bottom of `auto_register.py`:
```python
bot.run_campaign(num_registrations=200)
```

## Important Note

This script is set up specifically for HostingKarle's registration system. The form fields have been mapped to match their registration form. 