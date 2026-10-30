# MR.TOM Instagram Growth Bot

A Python CLI for Instagram professional-account connection checks and follow-back analytics. Runs on Kali Linux and Android Termux.

## What it does
- Checks a connected Instagram professional account through Meta's Graph API.
- Compares locally supplied follower/following CSV exports.
- Produces a `non_followers_review.csv` list for manual review.
- Keeps credentials in a local `.env` file (never commit it).

## Important limitations
This project does **not** automate follow/unfollow actions, scrape private follower lists, or collect Instagram passwords. Meta's official Instagram APIs do not provide a general-purpose endpoint for arbitrary follow/unfollow actions or unrestricted follower-list retrieval. Use Instagram's own data-download feature to obtain your account data, then prepare CSV files locally.

## Install: Kali Linux
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
git clone https://github.com/vijay-termux/mr-tom-instagram-growth-bot.git
cd mr-tom-instagram-growth-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Install: Android Termux
Install Termux from its official F-Droid or GitHub distribution, then:
```bash
pkg update && pkg upgrade -y
pkg install -y python git
git clone https://github.com/vijay-termux/mr-tom-instagram-growth-bot.git
cd mr-tom-instagram-growth-bot
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Meta API connection
1. Create/configure a Meta developer app and add the Instagram product/API use case appropriate to your professional account.
2. Complete Meta's required account linking, permissions, and review steps.
3. Obtain an access token using Meta's documented OAuth flow.
4. Copy `.env.example` to `.env`, then fill in your token and Instagram professional account ID:
   ```bash
   cp .env.example .env
   nano .env
   ```
5. Run `python main.py` and choose option 1.

Do not paste your password or access token into chats, issues, or public repositories.

## Follow-back report
Create these files:
- `data/followers.csv`
- `data/following.csv`

Each can be a one-column CSV with header `username`, or a plain text file with one username per line. Put usernames without `@` (the parser also accepts `@`). Run option 2. The generated review file is `data/non_followers_review.csv`.

## GitHub
Repository: https://github.com/vijay-termux/mr-tom-instagram-growth-bot

Never commit `.env` or exported personal account data.
