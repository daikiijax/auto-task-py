#
AUTH_TOKEN = "Bearer <ISIKAN TOKENMU DI SINI>"
COOKIES = "<ISIKAN COOKIE DI SINI>"

import random
import time
import requests

BASE_URL = 'https://campaign.cicada.finance/api'
CAMPAIGN_ID = 440

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/137.0.0.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
]

def get_headers():
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.6',
        'authorization': AUTH_TOKEN,
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'user-agent': random.choice(user_agents),
        'cookie': COOKIES,
        'Referer': 'https://campaign.cicada.finance/campaigns/6d70de3a-60ea-4896-b713-276de1bc02c7?code=g1nLayZV',
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }

def fetch_completed_points():
    url = f"{BASE_URL}/points?campaignId={CAMPAIGN_ID}"
    try:
        r = requests.get(url, headers=get_headers(), timeout=15)
        r.raise_for_status()
        return set([item["task_id"] for item in r.json()])
    except Exception as e:
        print(f"Error fetching completed points: {e}")
        return set()

def fetch_completed_gems():
    url = f"{BASE_URL}/gems?campaignId={CAMPAIGN_ID}"
    try:
        r = requests.get(url, headers=get_headers(), timeout=15)
        r.raise_for_status()
        return set([item["task_id"] for item in r.json()])
    except Exception as e:
        print(f"Error fetching completed gems: {e}")
        return set()

def fetch_tasks():
    url = f"{BASE_URL}/campaigns/{CAMPAIGN_ID}/tasks"
    try:
        r = requests.get(url, headers=get_headers(), timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []

def complete_task(task_id, task_title):
    try:
        points = requests.post(
            f"{BASE_URL}/points/add",
            json={"taskId": task_id},
            headers=get_headers(),
            timeout=15
        )
        points.raise_for_status()

        gems = requests.post(
            f"{BASE_URL}/gems/credit",
            json={"transactionType": "TASK", "options": {"taskId": task_id}},
            headers=get_headers(),
            timeout=15
        )
        gems.raise_for_status()

        print(f"Success: {task_title} ({task_id})")
        return True
    except Exception as e:
        print(f"Failed: {task_title} ({task_id}) — {e}")
        return False

def main():
    if not AUTH_TOKEN or not COOKIES:
        print("AUTH_TOKEN atau COOKIES belum diisi!")
        return

    completed_points = fetch_completed_points()
    completed_gems = fetch_completed_gems()

    tasks = fetch_tasks()
    if not tasks:
        print("Tidak ada task.")
        return

    for task in tasks:
        if task["id"] not in completed_points or task["id"] not in completed_gems:
            complete_task(task["id"], task.get("title", "NoTitle"))
            time.sleep(1)
        if "subtasks" in task and task["subtasks"]:
            for sub in task["subtasks"]:
                if sub["id"] not in completed_points or sub["id"] not in completed_gems:
                    complete_task(sub["id"], sub.get("title", "NoTitle"))
                    time.sleep(1)

    print("Selesai semua task.")

main()
  
