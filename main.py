#!/usr/bin/env python3
"""MR.TOM Instagram Growth Manager - safe analytics and follow-back tracker."""
import csv
import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
load_dotenv(BASE / ".env")


def read_names(path):
    p = Path(path)
    if not p.exists():
        print(f"File not found: {p}")
        return set()

    names = set()
    with p.open(newline="", encoding="utf-8-sig") as f:
        sample = f.read(2048)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
            rows = csv.DictReader(f, dialect=dialect)
            for row in rows:
                value = (
                    row.get("username")
                    or row.get("Username")
                    or row.get("user")
                    or row.get("User")
                    or next(iter(row.values()), "")
                )
                value = (value or "").strip().lstrip("@").lower()
                if value and value not in {"username", "user"}:
                    names.add(value)
        except csv.Error:
            f.seek(0)
            for line in f:
                value = line.strip().lstrip("@").lower()
                if value and value != "username":
                    names.add(value)
    return names


def tracker():
    followers = read_names(DATA / "followers.csv")
    following = read_names(DATA / "following.csv")
    if not followers and not following:
        print("Add exported lists to data/followers.csv and data/following.csv first.")
        return

    mutual = following & followers
    not_following_back = following - followers
    fans_not_followed = followers - following

    print("\nFOLLOW-BACK REPORT")
    print("=" * 48)
    print(f"You follow:                 {len(following)}")
    print(f"They follow you:            {len(followers)}")
    print(f"Mutual follows:             {len(mutual)}")
    print(f"Not following you back:     {len(not_following_back)}")
    print(f"They follow you, you don't: {len(fans_not_followed)}")

    out = DATA / "non_followers_review.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "detected_at_utc", "status"])
        for name in sorted(not_following_back):
            writer.writerow([
                name,
                datetime.now(timezone.utc).isoformat(),
                "REVIEW_MANUALLY",
            ])

    print(f"\nReview list saved: {out.relative_to(BASE)}")
    print("No accounts were followed or unfollowed.")


def graph_api():
    token = os.getenv("META_ACCESS_TOKEN", "").strip()
    ig_id = os.getenv("IG_USER_ID", "").strip()
    version = os.getenv("GRAPH_API_VERSION", "v23.0").strip()

    if not token or not ig_id:
        print("Configure META_ACCESS_TOKEN and IG_USER_ID in .env (never share them).")
        return

    url = f"https://graph.facebook.com/{version}/{ig_id}"
    params = {
        "fields": "username,account_type,media_count",
        "access_token": token,
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        data = response.json()
        if not response.ok:
            print("Meta API error:", json.dumps(data, indent=2))
            return

        print("\nCONNECTED PROFESSIONAL ACCOUNT")
        for key, value in data.items():
            if key != "id":
                print(f"{key}: {value}")
    except requests.RequestException as exc:
        print("Connection error:", exc)


def main():
    while True:
        print("""
========================================
       MR.TOM INSTAGRAM GROWTH BOT
========================================
[1] Connect/check Meta account
[2] Follower / follow-back report
[3] Show setup instructions
[0] Exit
""")
        choice = input("Select option: ").strip()
        if choice == "1":
            graph_api()
        elif choice == "2":
            tracker()
        elif choice == "3":
            print("See README.md. Put CSV exports in data/ and configure .env for Meta API.")
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
