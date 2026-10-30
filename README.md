# MR.TOM Instagram Growth Agent

An interactive Python CLI for Kali Linux and Android Termux. It connects to an Instagram professional account through Meta's official Graph API (when configured) and analyzes locally exported follower/following lists.

## Menu
- **1 — Connect/check Meta professional account:** checks the connected professional account using a Meta access token obtained through the official OAuth flow.
- **2 — Target audience & follow-back manager:** asks for a target Instagram username, then compares your own locally supplied follower/following lists and creates review reports.
- **3 — View generated reports:** checks whether report files exist.
- **4 — Setup instructions.**

## Important platform limits
This tool does not request or store your Instagram password, scrape private or arbitrary target-account follower lists, or automate follow/unfollow actions. Meta's official Instagram APIs do not provide general-purpose follow/unfollow endpoints or unrestricted follower-list access. The target username is saved as analysis context only; it does not grant access to that account's followers. Review any suggested unfollow manually in Instagram.

## Install on Kali Linux
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

## Install on Android Termux
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

## Use option 2
1. Export/download your own Instagram account information using Instagram's official Accounts Center data-download process.
2. Prepare:
   - `data/followers.csv` — accounts following you.
   - `data/following.csv` — accounts you follow.
3. Each CSV should contain a `username` column (a one-column CSV or plain list of usernames also works).
4. Run `python main.py`, choose option 2, and enter the target username.
5. The tool creates:
   - `data/non_followers_review.csv`
   - `data/mutual_followers.csv`

The non-followers report is a manual review list, not an automated unfollow queue.

## Configure official Meta API access (option 1)
1. Configure a Meta developer app and the Instagram API use case for your professional account.
2. Complete the required account linking and permissions.
3. Obtain an access token through Meta's documented OAuth flow.
4. Copy and edit the environment file:
   ```bash
   cp .env.example .env
   nano .env
   ```
5. Set `META_ACCESS_TOKEN` and `IG_USER_ID`, then run option 1.

Never paste your password or access token into chats, issues, or public repositories. The `.env` file is ignored by Git.

## Repository
https://github.com/vijay-termux/mr-tom-instagram-growth-bot
