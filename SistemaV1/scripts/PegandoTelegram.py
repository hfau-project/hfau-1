"""
Collects the Telegram chat IDs of partners who send /start to your bot.

Usage:
    export TELEGRAM_BOT_TOKEN="123456:ABC..."     (Linux / Raspberry Pi)
    $env:TELEGRAM_BOT_TOKEN = "123456:ABC..."     (Windows PowerShell)
    python collect_telegram_ids.py

Each partner opens the bot in Telegram and presses Start (or sends /start).
Press Ctrl+C when everyone is registered.
"""

import json
import os
import sys
import time
from pathlib import Path

import subprocess

# If "requests" is not installed, try to install it automatically
try:
    import requests
except ImportError:
    print("The 'requests' library is missing. Installing it now...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    except subprocess.CalledProcessError:
        # Newer Raspberry Pi OS blocks system-wide pip; try the override
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "requests", "--break-system-packages"]
            )
        except subprocess.CalledProcessError:
            sys.exit(
                "Could not install 'requests' automatically.\n"
                "Try manually: pip install requests\n"
                "(on Raspberry Pi OS: sudo apt install python3-requests)"
            )
    import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    sys.exit("Set the TELEGRAM_BOT_TOKEN environment variable first.")

API = f"https://api.telegram.org/bot{TOKEN}"
OUTPUT_FILE = Path("partners.json")


def load_partners():
    if OUTPUT_FILE.exists():
        return json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
    return {}


def save_partners(partners):
    # Write to a temp file first, then swap, so a crash never corrupts the file
    tmp = OUTPUT_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(partners, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(OUTPUT_FILE)


def send_message(chat_id, text):
    requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=15)


def main():
    partners = load_partners()
    offset = None  # tells Telegram which updates we already processed
    print(f"Listening... {len(partners)} partner(s) already saved. Ctrl+C to stop.")

    while True:
        try:
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset
            resp = requests.get(f"{API}/getUpdates", params=params, timeout=40)
            resp.raise_for_status()
            updates = resp.json().get("result", [])
        except requests.RequestException as err:
            print(f"Network error: {err}. Retrying in 5s...")
            time.sleep(5)
            continue
        except KeyboardInterrupt:
            break

        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message")
            if not message:
                continue

            text = message.get("text", "")
            chat = message["chat"]
            user = message.get("from", {})

            # Only register private chats where the person sent /start
            if chat.get("type") != "private" or not text.startswith("/start"):
                continue

            chat_id = str(chat["id"])
            is_new = chat_id not in partners
            partners[chat_id] = {
                "first_name": user.get("first_name", ""),
                "username": user.get("username", ""),
                "registered_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            save_partners(partners)

            if is_new:
                print(f"New partner: {user.get('first_name')} (chat_id={chat_id})")
                send_message(chat_id, "Registered! You will receive project notifications here.")
            else:
                send_message(chat_id, "You are already registered.")

    print(f"\nDone. {len(partners)} partner(s) saved in {OUTPUT_FILE}.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
