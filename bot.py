#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import hashlib
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
import urllib.request
import urllib.parse

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
CHANNEL_ID = os.environ.get("CHANNEL_ID", "").strip()
TZ_NAME = os.environ.get("TIMEZONE", "Africa/Cairo").strip()

if not BOT_TOKEN or not CHANNEL_ID:
    print("ERROR: BOT_TOKEN or CHANNEL_ID missing")
    sys.exit(1)

TZ = ZoneInfo(TZ_NAME)
START_DATE = datetime(2026, 1, 1, tzinfo=TZ)
MATCH_WINDOW = 8
MATCH_WINDOW_BACK = 150


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            if '"ok":true' in body:
                return True
            print("Unexpected response: " + body[:300])
            return False
    except Exception as e:
        print("Send error: " + str(e))
        return False


def post_key(cycle_day, post):
    h = hashlib.md5(post["text"].encode("utf-8")).hexdigest()[:8]
    return "d" + str(cycle_day) + "_" + post["time"] + "_" + h


def main():
    try:
        data = load_json("posts.json")
    except Exception as e:
        print("Failed to read posts.json: " + str(e))
        sys.exit(1)

    try:
        state = load_json("state.json")
        if "sent" not in state:
            state["sent"] = []
    except Exception:
        state = {"sent": []}

    cycle_days = data.get("cycle_days", 14)
    posts = data.get("posts", [])

    now = datetime.now(TZ)
    days_since = (now.date() - START_DATE.date()).days
    cycle_day = (days_since % cycle_days) + 1
    now_minutes = now.hour * 60 + now.minute

    print("Time: " + now.strftime("%Y-%m-%d %H:%M") + " (" + TZ_NAME + ")")
    print("Cycle day: " + str(cycle_day) + " of " + str(cycle_days))

    matched = []
    for post in posts:
        if post.get("day") != cycle_day:
            continue
        try:
            hh, mm = map(int, post["time"].split(":"))
        except Exception:
            continue
        post_minutes = hh * 60 + mm
        if (now_minutes - MATCH_WINDOW_BACK) <= post_minutes <= (now_minutes + MATCH_WINDOW):
            key = post_key(cycle_day, post)
            if key in state["sent"]:
                print("Already sent: " + post["time"])
                continue
            matched.append((key, post))

    if not matched:
        print("No matching posts right now.")
        save_json("state.json", state)
        return

    for key, post in matched:
        print("Sending post at " + post["time"] + "...")
        if send_telegram(post["text"]):
            state["sent"].append(key)
            print("Sent: " + post["time"])
        else:
            print("Failed: " + post["time"])

    state["sent"] = state["sent"][-800:]
    save_json("state.json", state)


if __name__ == "__main__":
    main()