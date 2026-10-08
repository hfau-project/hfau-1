"""
CODANDO PELO VIM!

Esse código enviará uma mensagem simples para vocÊs. Ele pegará o json file e enviará para todos nós uma mensagem.

É um tese para o que está por vir

"""

import json
import time
from pathlib import Path

import requests

TOKEN = "8710912164:AAF8Jsar57Y2fg1nGW8fBS0kqJdgqneYdCI"
API = f"https://api.telegram.org/bot{TOKEN}"
OUTPUT_FILE = Path("partners.json")


def load_chat_ids():
    if not OUTPUT_FILE.exists():
        raise SystemExit("partners.json not found. Run the collector first.")
    partners = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
    return list(partners.keys())


def send(chat_id, text):
    try:
        r = requests.post(
            f"{API}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=15,
        )
        r.raise_for_status()
        print(f"Sent to {chat_id}")
    except requests.RequestException as e:
        print(f"Failed to send to {chat_id}: {e}")


def main():
    chat_ids = load_chat_ids()
    if not chat_ids:
        raise SystemExit("No partners registered yet.")
    print(f"Sending 'Hello_World!' to {len(chat_ids)} partner(s)")

    end_time = time.time() + 2
    while time.time() < end_time:
        for chat_id in chat_ids:
            send(chat_id, "Lembrem-se de fazer o 13 no segundo turno")
        time.sleep(1)  # one round per second


if __name__ == "__main__":
    main()
