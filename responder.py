#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import sys
import urllib.request
import urllib.parse

BOT_TOKEN = os.environ.get("REPLY_BOT_TOKEN", "").strip()
WEBSITE_URL = os.environ.get("WEBSITE_URL", "https://reclaimx.site.je/").strip()

if not BOT_TOKEN:
    print("ERROR: REPLY_BOT_TOKEN missing")
    sys.exit(1)


def load_state():
    try:
        with open("reply_state.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"offset": 0}


def save_state(state):
    with open("reply_state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_updates(offset):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}&timeout=0"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_welcome(chat_id, first_name):
    welcome = (
        "🎉 أهلاً بيك يا " + first_name + "!\n\n"
        "أنا ReclaimX — منصة الأمن السيبراني والبرمجة 🛡️\n\n"
        "📍 كل اللي تحتاجه هنا:\n"
        "🔗 " + WEBSITE_URL + "\n\n"
        "✨ دورات احترافية\n"
        "🤖 اشتراكات الذكاء الاصطناعي\n"
        "📱 خدمات السوشيال ميديا\n"
        "🔒 استشارات أمنية\n\n"
        "ابدأ رحلتك الآن 🚀"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": welcome,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def main():
    state = load_state()
    offset = state.get("offset", 0)

    try:
        result = get_updates(offset)
    except Exception as e:
        print("getUpdates error: " + str(e))
        return

    if not result.get("ok"):
        print("Telegram returned not ok")
        return

    updates = result.get("result", [])
    if not updates:
        print("No new messages.")
        return

    for update in updates:
        update_id = update.get("update_id", 0)
        state["offset"] = update_id + 1

        message = update.get("message")
        if not message:
            continue

        chat = message.get("chat", {})
        chat_id = chat.get("id")
        chat_type = chat.get("type")
        first_name = chat.get("first_name", "صديقي")

        if chat_type != "private":
            continue

        try:
            send_welcome(chat_id, first_name)
            print("Replied to " + str(chat_id) + " (" + first_name + ")")
        except Exception as e:
            print("send error: " + str(e))

    save_state(state)


if __name__ == "__main__":
    main()