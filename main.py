#!/usr/bin/env python3
"""MR.TOM Instagram Growth Agent: official account check + local audience review."""
import csv
import json
import os
import re
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
load_dotenv(BASE / ".env")


def normalize_username(value):
    value = (value or "").strip()
    if value.startswith("@"):
        value = value[1:]
    return value.lower()


def read_names(path):
    p = Path(path)
    if not p.exists():
        return set()
    names = set()
    with p.open(newline="", encoding="utf-8-sig") as f:
        sample = f.read(2048)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
            rows = csv.DictReader(f, dialect=dialect)
            for row in rows:
                value = (row.get("username") or row.get("Username")
                         or row.get("user") or row.get("User")
                         or next(iter(row.values()), ""))
                value = normalize_username(value)
                if value and value not in {"username", "user"}:
                    names.add(value)
        except csv.Error:
            f.seek(0)
            for line in f:
                value = normalize_username(line)
                if value and value != "username":
                    names.add(value)
    return names


def save_target_context(target):
    (DATA / "last_target.txt").write_text(target + "\n", encoding="utf-8")


def audience_manager():
    print("\nMR.TOM TARGET AUDIENCE MANAGER")
    print("-" * 42)
    target = input("Enter target Instagram username (e.g. @example): ").strip()
    target = normalize_username(target)
    if not re.fullmatch(r"[a-z0-9._]{1,30}", target):
        print("Invalid Instagram username format.")
        return

    save_target_context(target)
    print(f"\nTarget saved: @{target}")
    print("Next, provide your own Instagram data exports in the data folder:")
    print("  data/followers.csv  - accounts following your account")
    print("  data/following.csv  - accounts your account follows")
    print("\nThe official API does not expose arbitrary target-account follower")
    print("lists or general follow/unfollow controls. This tool will not ask")
    print("for your Instagram password or automate restricted actions.")

    followers = read_names(DATA / "followers.csv")
    following = read_names(DATA / "following.csv")
    if not followers and not following:
        print("\nNo account lists found yet. Add the two CSV files and run option 2 again.")
        return

    mutual = following & followers
    not_following_back = following - followers
    followers_not_followed = followers - following
    stamp = datetime.now(timezone.utc).isoformat()

    print("\nFOLLOW-BACK ANALYSIS")
    print("=" * 42)
    print(f"Target username:             @{target}")
    print(f"Accounts you follow:         {len(following)}")
    print(f"Your followers:               {len(followers)}")
    print(f"Mutual follows:               {len(mutual)}")
    print(f"Not following you back:       {len(not_following_back)}")
    print(f"Following you, not followed:  {len(followers_not_followed)}")

    out = DATA / "non_followers_review.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["target_username", "username", "detected_at_utc", "recommended_action"])
        for name in sorted(not_following_back):
            writer.writerow([target, name, stamp, "REVIEW_IN_INSTAGRAM_MANUALLY"])

    mutual_out = DATA / "mutual_followers.csv"
    with mutual_out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username"])
        writer.writerows([[name] for name in sorted(mutual)])

    print(f"\nSaved: {out.relative_to(BASE)}")
    print(f"Saved: {mutual_out.relative_to(BASE)}")
    print("No follow or unfollow actions were performed.")


def graph_api():
    token = os.getenv("META_ACCESS_TOKEN", "").strip()
    ig_id = os.getenv("IG_USER_ID", "").strip()
    version = os.getenv("GRAPH_API_VERSION", "v23.0").strip()
    if not token or not ig_id:
        print("Configure META_ACCESS_TOKEN and IG_USER_ID in .env.")
        print("Use Meta's official OAuth flow. Never enter your Instagram password here.")
        return

    url = f"https://graph.facebook.com/{version}/{ig_id}"
    try:
        response = requests.get(
            url,
            params={"fields": "username,account_type,media_count", "access_token": token},
            timeout=20,
        )
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


def show_reports():
    for filename in ("non_followers_review.csv", "mutual_followers.csv"):
        path = DATA / filename
        print(f"{filename}: {'available' if path.exists() else 'not generated yet'}")


def main():
    while True:
        print("""
========================================
       MR.TOM INSTAGRAM GROWTH AGENT
========================================
[1] Connect/check Meta professional account
[2] Target audience & follow-back manager
[3] View generated reports
[4] Setup instructions
[0] Exit
""")
        choice = input("Select option: ").strip()
        if choice == "1":
            graph_api()
        elif choice == "2":
            audience_manager()
        elif choice == "3":
            show_reports()
        elif choice == "4":
            print("See README.md. Add followers.csv and following.csv in data/.")
            print("Configure official Meta OAuth credentials in .env for option 1.")
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
